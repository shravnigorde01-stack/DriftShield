from pathlib import Path
import pandas as pd

from config.settings import REFERENCE_DATA_DIR, INCOMING_DATA_DIR
from monitoring.monitoring_engine import run_monitoring

from backend.database.connection import SessionLocal
from backend.database.monitoring_runs import MonitoringRun
from backend.database.alerts import Alert


def run_file_monitoring(reference_filename, current_filename):

    if Path(reference_filename).name != reference_filename:
        raise ValueError("Invalid reference filename.")

    if Path(current_filename).name != current_filename:
        raise ValueError("Invalid incoming filename.")

    reference_path = REFERENCE_DATA_DIR / reference_filename
    current_path = INCOMING_DATA_DIR / current_filename

    if not reference_path.is_file():
        raise FileNotFoundError("Reference dataset not found.")

    if not current_path.is_file():
        raise FileNotFoundError("Incoming dataset not found.")

    reference_df = pd.read_csv(reference_path)
    current_df = pd.read_csv(current_path)

    results = run_monitoring(
        reference_df=reference_df,
        current_df=current_df
    )

    drift_results = results["data_drift"]

    total_features = drift_results["total_features"]
    drifted_features = drift_results["drifted_features"]
    stable_features = drift_results["stable_features"]

    status = "Drift Detected" if drifted_features > 0 else "Stable"

    db = SessionLocal()

    try:
        # Save monitoring run
        monitoring_record = MonitoringRun(
            reference_dataset=reference_filename,
            incoming_dataset=current_filename,
            total_features=total_features,
            drifted_features=drifted_features,
            stable_features=stable_features,
            status=status,
            results=results
        )

        db.add(monitoring_record)
        db.flush()

        # Generate alerts for drifted features
        generated_alerts = []

        feature_results = drift_results["feature_results"]

        for feature_name, feature_result in feature_results.items():

            if feature_result.get("drift_detected") is True:

                alert = Alert(
                    run_id=monitoring_record.id,
                    feature_name=feature_name,
                    severity="Warning",
                    message=f"Data drift detected in feature '{feature_name}'.",
                    status="New"
                )

                db.add(alert)

                generated_alerts.append({
                    "feature_name": feature_name,
                    "severity": "Warning",
                    "status": "New"
                })

        db.commit()
        db.refresh(monitoring_record)

        return {
            "message": "Monitoring completed successfully.",
            "run_id": monitoring_record.id,
            "reference_dataset": reference_filename,
            "incoming_dataset": current_filename,
            "monitoring_results": results,
            "alerts_generated": len(generated_alerts),
            "alerts": generated_alerts
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()