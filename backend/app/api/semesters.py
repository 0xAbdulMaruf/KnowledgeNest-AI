from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.semester import Semester
from app.models.subject import Subject
from app.schemas.semester import SemesterResponse
from app.schemas.subject import SubjectResponse

router = APIRouter(prefix="/api/semesters", tags=["semesters"])


@router.get("/", response_model=list[SemesterResponse])
def list_semesters(db: Session = Depends(get_db)):
    semesters = db.query(Semester).order_by(Semester.number).all()
    return semesters


@router.get("/{semester_id}", response_model=SemesterResponse)
def get_semester(semester_id: int, db: Session = Depends(get_db)):
    semester = db.query(Semester).filter(Semester.id == semester_id).first()
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    return semester


@router.get("/{semester_id}/subjects", response_model=list[SubjectResponse])
def get_semester_subjects(semester_id: int, db: Session = Depends(get_db)):
    semester = db.query(Semester).filter(Semester.id == semester_id).first()
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    subjects = db.query(Subject).filter(Subject.semester_id == semester_id).all()
    result = []
    for s in subjects:
        subj = SubjectResponse.model_validate(s)
        subj.units_count = len(s.units)
        result.append(subj)
    return result
