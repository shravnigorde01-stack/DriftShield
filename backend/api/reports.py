from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from backend.database.connection import get_db
from backend.database.monitoring_runs import MonitoringRun
from backend.database.alerts import Alert


router = APIRouter(
    prefix="/reports",
    tags=["Report Generation"]
)


def get_report_data(run_id, db):

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

    alerts = (
        db.query(Alert)
        .filter(Alert.run_id == run_id)
        .all()
    )

    return record, alerts


# Download JSON report
@router.get("/{run_id}")
def generate_json_report(
    run_id: int,
    db: Session = Depends(get_db)
):

    record, alerts = get_report_data(run_id, db)

    report = {
        "report_title": "DriftShield Monitoring Report",
        "run_id": record.id,
        "created_at": str(record.created_at),
        "datasets": {
            "reference": record.reference_dataset,
            "incoming": record.incoming_dataset
        },
        "summary": {
            "total_features": record.total_features,
            "drifted_features": record.drifted_features,
            "stable_features": record.stable_features,
            "overall_status": record.status
        },
        "monitoring_results": record.results,
        "alerts": [
            {
                "alert_id": alert.id,
                "feature_name": alert.feature_name,
                "severity": alert.severity,
                "message": alert.message,
                "status": alert.status,
                "created_at": str(alert.created_at)
            }
            for alert in alerts
        ],
        "performance_status": record.results.get(
            "performance_status",
            "Unavailable"
        )
    }

    import json

    return Response(
        content=json.dumps(report, indent=4),
        media_type="application/json",
        headers={
            "Content-Disposition":
            f'attachment; filename="driftshield_report_{run_id}.json"'
        }
    )


# Download PDF report
@router.get("/pdf/{run_id}")
def generate_pdf_report(
    run_id: int,
    db: Session = Depends(get_db)
):

    record, alerts = get_report_data(run_id, db)

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    content = []

    content.append(
        Paragraph("DRIFTSHIELD", styles["Title"])
    )

    content.append(
        Paragraph(
            "Detect the Drift. Protect the Performance.",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph("MONITORING REPORT", styles["Heading1"])
    )

    content.append(Spacer(1, 12))

    summary_data = [
        ["Monitoring Run", str(record.id)],
        ["Generated At", str(record.created_at)],
        ["Reference Dataset", escape(record.reference_dataset)],
        ["Incoming Dataset", escape(record.incoming_dataset)],
        ["Overall Status", record.status],
        ["Total Features", str(record.total_features)],
        ["Drifted Features", str(record.drifted_features)],
        ["Stable Features", str(record.stable_features)]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[180, 300]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EEEEEE")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    content.append(summary_table)
    content.append(Spacer(1, 20))

    content.append(
        Paragraph("FEATURE-LEVEL DRIFT RESULTS", styles["Heading2"])
    )

    feature_data = [
        ["Feature", "PSI", "KS Statistic", "KS P-Value", "Status"]
    ]

    feature_results = record.results.get(
        "data_drift", {}
    ).get("feature_results", {})

    for feature, result in feature_results.items():

        feature_data.append([
            escape(str(feature)),
            str(result.get("psi_score", "N/A")),
            str(result.get("ks_statistic", "N/A")),
            str(result.get("ks_p_value", "N/A")),
            str(result.get("status", "N/A"))
        ])

    feature_table = Table(
        feature_data,
        repeatRows=1
    )

    feature_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("FONTSIZE", (0, 0), (-1, -1), 8)
    ]))

    content.append(feature_table)
    content.append(Spacer(1, 20))

    content.append(
        Paragraph("GENERATED ALERTS", styles["Heading2"])
    )

    alert_data = [
        ["ID", "Feature", "Severity", "Status"]
    ]

    for alert in alerts:
        alert_data.append([
            str(alert.id),
            escape(alert.feature_name),
            escape(alert.severity),
            escape(alert.status)
        ])

    if not alerts:
        alert_data.append(["-", "No alerts", "-", "-"])

    alert_table = Table(alert_data)

    alert_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 7)
    ]))

    content.append(alert_table)
    content.append(Spacer(1, 20))

    performance_status = record.results.get(
        "performance_status",
        "Unavailable"
    )

    content.append(
        Paragraph(
            "PERFORMANCE STATUS",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            escape(str(performance_status)),
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 25))

    content.append(
        Paragraph(
            "Generated by DriftShield Monitoring Platform",
            styles["Italic"]
        )
    )

    document.build(content)

    pdf_data = buffer.getvalue()
    buffer.close()

    return Response(
        content=pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            f'attachment; filename="driftshield_report_{run_id}.pdf"'
        }
    )