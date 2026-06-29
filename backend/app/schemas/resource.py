from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional
from app.models.resource import ResourceType


class ResourceBase(BaseModel):
    topic_id: int
    type: ResourceType
    title: str
    url: str = ""
    content: str = ""
    metadata_: dict[str, Any] = {}


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    topic_id: Optional[int] = None
    type: Optional[ResourceType] = None
    title: Optional[str] = None
    url: Optional[str] = None
    content: Optional[str] = None
    metadata_: Optional[dict[str, Any]] = None


class ResourceResponse(ResourceBase):
    id: int
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None

    model_config = {"from_attributes": True}


class FacultyUnlockRequest(BaseModel):
    teacher_name: str
    password: str


class FacultyUnlockResponse(BaseModel):
    access_token: str
    teacher_name: str


class FacultyActivityResponse(BaseModel):
    id: int
    teacher_name: str
    action: str
    resource_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
