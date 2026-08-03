from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

# Load configuration before importing modules that initialize the database or services.
# Support both the repository-level .env and backend/.env regardless of launch directory.
backend_dir = Path(__file__).resolve().parents[1]
project_env = backend_dir.parent / ".env"
load_dotenv(project_env)
load_dotenv(backend_dir / ".env", override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base, ensure_resource_soft_delete_columns
from app.models import Semester, Subject, Unit, Topic, Resource, PYQ  # noqa: F401
from app.api import semesters, subjects, units, topics, search, recommendations, faculty, ai


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    ensure_resource_soft_delete_columns()
    yield


app = FastAPI(title="Academic Recommendation Platform", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(semesters.router)
app.include_router(subjects.router)
app.include_router(units.router)
app.include_router(topics.router)
app.include_router(search.router)
app.include_router(recommendations.router)
app.include_router(faculty.router)
app.include_router(ai.router)


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
