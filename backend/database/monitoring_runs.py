from sqlalchemy import Column, Integer, String, DateTime, JSON, func

from backend.database.connection import Base


class MonitoringRun(Base):
    __tablename__ = "monitoring_runs"

    id = Column(Integer, primary_key=True, index=True)

    reference_dataset = Column(String(255), nullable=False)
    incoming_dataset = Column(String(255), nullable=False)

    total_features = Column(Integer, default=0)
    drifted_features = Column(Integer, default=0)
    stable_features = Column(Integer, default=0)

    status = Column(String(50), nullable=False)

    results = Column(JSON, nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.current_timestamp()
    )
    