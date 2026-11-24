from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func
)

from backend.database.connection import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    run_id = Column(
        Integer,
        ForeignKey("monitoring_runs.id"),
        nullable=False
    )

    feature_name = Column(String(100), nullable=False)

    severity = Column(String(20), default="High")

    message = Column(String(500), nullable=False)

    status = Column(String(20), default="New")

    created_at = Column(
        DateTime,
        server_default=func.current_timestamp()
    )