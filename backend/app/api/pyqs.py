from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.pyq import PYQ
from app.models.subject import Subject
from app.models.unit import Unit
from app.models.topic import Topic
from app.schemas.pyq import PYQCreate, PYQResponse, PYQListResponse, PYQSessionResponse

router = APIRouter(prefix="/api/pyqs", tags=["pyqs"])


@router.get("/", response_model=list[PYQListResponse])
def list_pyqs(
    subject_id: int = Query(None),
    unit_id: int = Query(None),
    topic_id: int = Query(None),
    year: int = Query(None),
    session: str = Query(None),
    question_type: str = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(PYQ)
    
    if subject_id:
        query = query.filter(PYQ.subject_id == subject_id)
    if unit_id:
        query = query.filter(PYQ.unit_id == unit_id)
    if topic_id:
        query = query.filter(PYQ.topic_id == topic_id)
    if year:
        query = query.filter(PYQ.year == year)
    if session:
        query = query.filter(PYQ.session.ilike(f"%{session}%"))
    if question_type:
        query = query.filter(PYQ.question_type == question_type)
    
    pyqs = query.order_by(PYQ.year.desc(), PYQ.session.desc()).limit(limit).all()
    
    result = []
    for pyq in pyqs:
        unit_name = None
        topic_name = None
        if pyq.unit_id:
            unit = db.query(Unit).filter(Unit.id == pyq.unit_id).first()
            unit_name = unit.name if unit else None
        if pyq.topic_id:
            topic = db.query(Topic).filter(Topic.id == pyq.topic_id).first()
            topic_name = topic.name if topic else None
        
        result.append(PYQListResponse(
            id=pyq.id,
            session=pyq.session,
            year=pyq.year,
            paper_code=pyq.paper_code or "",
            paper_title=pyq.paper_title or "",
            question_id=pyq.question_id or "",
            question_text=pyq.question_text,
            question_type=pyq.question_type,
            marks=pyq.marks or "",
            unit_name=unit_name,
            topic_name=topic_name
        ))
    
    return result


@router.get("/sessions", response_model=list[PYQSessionResponse])
def list_pyq_sessions(
    subject_id: int = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(
        PYQ.session,
        PYQ.year,
        PYQ.paper_code,
        PYQ.paper_title,
        func.count(PYQ.id).label("question_count")
    )
    
    if subject_id:
        query = query.filter(PYQ.subject_id == subject_id)
    
    results = query.group_by(PYQ.session, PYQ.year, PYQ.paper_code, PYQ.paper_title)\
                   .order_by(PYQ.year.desc())\
                   .all()
    
    return [
        PYQSessionResponse(
            session=r.session,
            year=r.year,
            paper_code=r.paper_code or "",
            paper_title=r.paper_title or "",
            question_count=r.question_count
        )
        for r in results
    ]


@router.get("/years", response_model=list[int])
def list_pyq_years(
    subject_id: int = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(PYQ.year).distinct()
    if subject_id:
        query = query.filter(PYQ.subject_id == subject_id)
    years = query.order_by(PYQ.year.desc()).all()
    return [y[0] for y in years]


@router.get("/{pyq_id}", response_model=PYQResponse)
def get_pyq(pyq_id: int, db: Session = Depends(get_db)):
    pyq = db.query(PYQ).filter(PYQ.id == pyq_id).first()
    if not pyq:
        raise HTTPException(status_code=404, detail="PYQ not found")
    return pyq


@router.post("/", response_model=PYQResponse)
def create_pyq(pyq_data: PYQCreate, db: Session = Depends(get_db)):
    pyq = PYQ(**pyq_data.model_dump())
    db.add(pyq)
    db.commit()
    db.refresh(pyq)
    return pyq


@router.get("/search/", response_model=list[PYQListResponse])
def search_pyqs(
    q: str = Query(..., min_length=1),
    subject_id: int = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    pattern = f"%{q}%"
    query = db.query(PYQ).filter(
        PYQ.question_text.ilike(pattern)
    )
    
    if subject_id:
        query = query.filter(PYQ.subject_id == subject_id)
    
    pyqs = query.limit(limit).all()
    
    result = []
    for pyq in pyqs:
        unit_name = None
        topic_name = None
        if pyq.unit_id:
            unit = db.query(Unit).filter(Unit.id == pyq.unit_id).first()
            unit_name = unit.name if unit else None
        if pyq.topic_id:
            topic = db.query(Topic).filter(Topic.id == pyq.topic_id).first()
            topic_name = topic.name if topic else None
        
        result.append(PYQListResponse(
            id=pyq.id,
            session=pyq.session,
            year=pyq.year,
            paper_code=pyq.paper_code or "",
            paper_title=pyq.paper_title or "",
            question_id=pyq.question_id or "",
            question_text=pyq.question_text,
            question_type=pyq.question_type,
            marks=pyq.marks or "",
            unit_name=unit_name,
            topic_name=topic_name
        ))
    
    return result
