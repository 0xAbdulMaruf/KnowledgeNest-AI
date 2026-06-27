from pydantic import BaseModel


class UnitBase(BaseModel):
    name: str
    number: int
    subject_id: int
    description: str = ""


class UnitCreate(UnitBase):
    pass


class TopicBrief(BaseModel):
    id: int
    name: str
    importance_score: float = 0.0

    model_config = {"from_attributes": True}


class UnitResponse(UnitBase):
    id: int
    topics: list[TopicBrief] = []
    topics_count: int = 0

    model_config = {"from_attributes": True}
