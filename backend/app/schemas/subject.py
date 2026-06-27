from pydantic import BaseModel


class SubjectBase(BaseModel):
    name: str
    code: str
    semester_id: int
    description: str = ""
    tags: list[str] = []


class SubjectCreate(SubjectBase):
    pass


class SubjectResponse(SubjectBase):
    id: int
    units_count: int = 0

    model_config = {"from_attributes": True}
