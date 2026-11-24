from sqlalchemy import Column, Integer, String, DateTime, func

from backend.database.connection import Base


class Project(Base):

    __tablename__ = "projects"

    # Unique project ID
    id = Column(Integer, primary_key=True, index=True)

    # Project information
    name = Column(String(100), nullable=False)

    description = Column(String(500), nullable=True)

    # Project creation date
    created_at = Column(
        DateTime,
        server_default=func.current_timestamp()
    )

    # Project status
    status = Column(String(20), default="Active")