from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.subject import Subject
from app.models.unit import Unit
from app.schemas.subject import SubjectResponse
from app.schemas.unit import UnitResponse

router = APIRouter(prefix="/api/subjects", tags=["subjects"])


@router.get("/", response_model=list[SubjectResponse])
def list_subjects(semester_id: int | None = Query(None), db: Session = Depends(get_db)):
    query = db.query(Subject)
    if semester_id is not None:
        query = query.filter(Subject.semester_id == semester_id)
    subjects = query.order_by(Subject.name).all()
    result = []
    for s in subjects:
        subj = SubjectResponse.model_validate(s)
        subj.units_count = len(s.units)
        result.append(subj)
    return result


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    subj = SubjectResponse.model_validate(subject)
    subj.units_count = len(subject.units)
    return subj


@router.get("/{subject_id}/units", response_model=list[UnitResponse])
def get_subject_units(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    units = db.query(Unit).filter(Unit.subject_id == subject_id).order_by(Unit.number).all()
    result = []
    for u in units:
        unit_resp = UnitResponse.model_validate(u)
        unit_resp.topics = [{"id": t.id, "name": t.name, "importance_score": t.importance_score} for t in u.topics]
        unit_resp.topics_count = len(u.topics)
        result.append(unit_resp)
    return result
