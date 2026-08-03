import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.resource import Resource
from app.models.faculty_activity import FacultyActivity
from app.schemas.resource import (
    FacultyActivityResponse,
    FacultyUnlockRequest,
    FacultyUnlockResponse,
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)

router = APIRouter(prefix="/api/faculty", tags=["faculty"])
FACULTY_SESSION_SECRET = os.getenv("FACULTY_SESSION_SECRET", "change-me")
FACULTY_TOKEN_TTL_HOURS = int(os.getenv("FACULTY_TOKEN_TTL_HOURS", "12"))


def _sign_teacher_name(teacher_name: str) -> str:
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=FACULTY_TOKEN_TTL_HOURS)).isoformat()
    payload = json.dumps(
        {"teacher_name": teacher_name.strip(), "exp": expires_at}, separators=(",", ":")
    ).encode("utf-8")
    signature = hmac.new(FACULTY_SESSION_SECRET.encode("utf-8"), payload, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(payload + b"." + signature).decode("utf-8")


def _verify_teacher_token(token: str | None) -> str:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Faculty unlock required")
    try:
        decoded = base64.urlsafe_b64decode(token.encode("utf-8"))
        payload_bytes, signature = decoded.rsplit(b".", 1)
        expected = hmac.new(FACULTY_SESSION_SECRET.encode("utf-8"), payload_bytes, hashlib.sha256).digest()
        if not hmac.compare_digest(signature, expected):
            raise ValueError
        payload = json.loads(payload_bytes.decode("utf-8"))
        teacher_name = str(payload.get("teacher_name", "")).strip()
        if not teacher_name:
            raise ValueError
        exp_str = str(payload.get("exp", ""))
        if exp_str:
            exp_time = datetime.fromisoformat(exp_str)
            if datetime.now(timezone.utc) > exp_time:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Faculty session expired")
        return teacher_name
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid faculty session") from exc


def _require_teacher(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Faculty unlock required")
    return _verify_teacher_token(authorization.removeprefix("Bearer ").strip())


def _resource_to_response(resource: Resource) -> ResourceResponse:
    return ResourceResponse.model_validate(resource)


@router.post("/unlock", response_model=FacultyUnlockResponse)
def unlock_faculty(payload: FacultyUnlockRequest):
    expected_password = os.getenv("FACULTY_TEACHER_PASSWORD", "")
    if not expected_password or not hmac.compare_digest(payload.password.encode("utf-8"), expected_password.encode("utf-8")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid teacher password")
    teacher_name = payload.teacher_name.strip()
    if not teacher_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Teacher name is required")
    return FacultyUnlockResponse(access_token=_sign_teacher_name(teacher_name), teacher_name=teacher_name)


def log_activity(db: Session, teacher_name: str, action: str, resource_id: int) -> None:
    db.add(
        FacultyActivity(
            teacher_name=teacher_name,
            action=action,
            resource_id=resource_id,
            created_at=datetime.now(timezone.utc),
        )
    )


@router.get("/resources", response_model=list[ResourceResponse])
def list_resources(
    db: Session = Depends(get_db),
    topic_id: int | None = Query(default=None),
    include_deleted: bool = Query(default=True),
    teacher_name: str = Depends(_require_teacher),
):
    query = db.query(Resource)
    if not include_deleted:
        query = query.filter(Resource.deleted_at.is_(None))
    if topic_id is not None:
        query = query.filter(Resource.topic_id == topic_id)
    resources = query.order_by(Resource.id.desc()).all()
    return [_resource_to_response(r) for r in resources]


@router.get("/activities", response_model=list[FacultyActivityResponse])
def list_activities(db: Session = Depends(get_db), teacher_name: str = Depends(_require_teacher)):
    _ = teacher_name
    return db.query(FacultyActivity).order_by(FacultyActivity.created_at.desc(), FacultyActivity.id.desc()).limit(20).all()


@router.post("/resources", response_model=ResourceResponse)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db), teacher_name: str = Depends(_require_teacher)):
    db_resource = Resource(
        topic_id=resource.topic_id,
        type=resource.type,
        title=resource.title,
        url=resource.url,
        content=resource.content,
        metadata_=resource.metadata_,
    )
    db.add(db_resource)
    db.flush()
    log_activity(db, teacher_name=teacher_name, action="create", resource_id=db_resource.id)
    db.commit()
    db.refresh(db_resource)
    return _resource_to_response(db_resource)


@router.put("/resources/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: int, resource: ResourceUpdate, db: Session = Depends(get_db), teacher_name: str = Depends(_require_teacher)):
    db_resource = db.query(Resource).filter(Resource.id == resource_id, Resource.deleted_at.is_(None)).first()
    if not db_resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    if resource.topic_id is not None:
        db_resource.topic_id = resource.topic_id
    if resource.type is not None:
        db_resource.type = resource.type
    if resource.title is not None:
        db_resource.title = resource.title
    if resource.url is not None:
        db_resource.url = resource.url
    if resource.content is not None:
        db_resource.content = resource.content
    if resource.metadata_ is not None:
        db_resource.metadata_ = resource.metadata_

    log_activity(db, teacher_name=teacher_name, action="update", resource_id=db_resource.id)
    db.commit()
    db.refresh(db_resource)
    return _resource_to_response(db_resource)


@router.delete("/resources/{resource_id}", response_model=ResourceResponse)
def delete_resource(resource_id: int, db: Session = Depends(get_db), teacher_name: str = Depends(_require_teacher)):
    resource = db.query(Resource).filter(Resource.id == resource_id, Resource.deleted_at.is_(None)).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    resource.deleted_at = datetime.now(timezone.utc)
    resource.deleted_by = teacher_name
    log_activity(db, teacher_name=teacher_name, action="delete", resource_id=resource.id)
    db.commit()
    db.refresh(resource)
    return _resource_to_response(resource)


@router.post("/resources/{resource_id}/restore", response_model=ResourceResponse)
def restore_resource(resource_id: int, db: Session = Depends(get_db), teacher_name: str = Depends(_require_teacher)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    if resource.deleted_at is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource is already active")

    resource.deleted_at = None
    resource.deleted_by = None
    log_activity(db, teacher_name=teacher_name, action="restore", resource_id=resource.id)
    db.commit()
    db.refresh(resource)
    return _resource_to_response(resource)
