from pydantic import BaseModel
from typing import Optional, Any
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


class ResourceResponse(ResourceBase):
    id: int

    model_config = {"from_attributes": True}
