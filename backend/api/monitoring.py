from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.monitoring_runs import MonitoringRun
from backend.services.monitoring_service import run_file_monitoring


router = APIRouter(
    prefix="/monitoring",
    tags=["Model Monitoring"]
)


class MonitoringRequest(BaseModel):
    reference_filename: str
    current_filename: str


@router.post("/run")
def start_monitoring(request: MonitoringRequest):

    try:
        return run_file_monitoring(
            reference_filename=request.reference_filename,
            current_filename=request.current_filename
        )

    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Monitoring failed: {str(error)}"
        )


# Retrieve all previous monitoring runs
@router.get("/history")
def get_monitoring_history(db: Session = Depends(get_db)):

    records = (
        db.query(MonitoringRun)
        .order_by(MonitoringRun.created_at.desc())
        .all()
    )

    return {
        "total_runs": len(records),
        "history": [
            {
                "run_id": record.id,
                "reference_dataset": record.reference_dataset,
                "incoming_dataset": record.incoming_dataset,
                "total_features": record.total_features,
                "drifted_features": record.drifted_features,
                "stable_features": record.stable_features,
                "status": record.status,
                "created_at": record.created_at
            }
            for record in records
        ]
    }


# Retrieve one monitoring run by ID
@router.get("/history/{run_id}")
def get_monitoring_run(
    run_id: int,
    db: Session = Depends(get_db)
):

    record = (
        db.query(MonitoringRun)
        .filter(MonitoringRun.id == run_id)
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Monitoring run not found."
        )

    return {
        "run_id": record.id,
        "reference_dataset": record.reference_dataset,
        "incoming_dataset": record.incoming_dataset,
        "total_features": record.total_features,
        "drifted_features": record.drifted_features,
        "stable_features": record.stable_features,
        "status": record.status,
        "results": record.results,
        "created_at": record.created_at
    }