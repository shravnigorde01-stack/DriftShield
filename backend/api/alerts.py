from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.alerts import Alert


router = APIRouter(
    prefix="/alerts",
    tags=["Alert Management"]
)


# Get all alerts
@router.get("/")
def get_all_alerts(db: Session = Depends(get_db)):

    alerts = (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .all()
    )

    return {
        "total_alerts": len(alerts),
        "alerts": alerts
    }


# Get alerts for a particular monitoring run
@router.get("/run/{run_id}")
def get_run_alerts(
    run_id: int,
    db: Session = Depends(get_db)
):

    alerts = (
        db.query(Alert)
        .filter(Alert.run_id == run_id)
        .all()
    )

    return {
        "run_id": run_id,
        "total_alerts": len(alerts),
        "alerts": alerts
    }


# Get one alert by ID
@router.get("/{alert_id}")
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found."
        )

    return alert


# Acknowledge an alert
@router.patch("/{alert_id}/acknowledge")
def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found."
        )

    alert.status = "Acknowledged"

    db.commit()
    db.refresh(alert)

    return {
        "message": "Alert acknowledged successfully.",
        "alert_id": alert.id,
        "status": alert.status
    }