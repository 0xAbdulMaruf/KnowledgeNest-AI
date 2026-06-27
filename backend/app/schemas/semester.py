from pydantic import BaseModel
from typing import Optional


class SemesterBase(BaseModel):
    name: str
    number: int


class SemesterCreate(SemesterBase):
    pass


class SubjectBrief(BaseModel):
    id: int
    name: str
    code: str

    model_config = {"from_attributes": True}


class SemesterResponse(SemesterBase):
    id: int
    subjects: list[SubjectBrief] = []

    model_config = {"from_attributes": True}
