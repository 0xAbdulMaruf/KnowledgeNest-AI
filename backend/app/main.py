from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.models import Semester, Subject, Unit, Topic, Resource  # noqa: F401
from app.api import semesters, subjects, units, topics, search, recommendations, faculty, ai


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
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
