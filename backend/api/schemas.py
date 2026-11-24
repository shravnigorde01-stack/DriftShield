from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


# Information required to create a project
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


# Information returned when viewing a project
class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    status: str

    model_config = ConfigDict(from_attributes=True)
    # Information required to update a project
class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None