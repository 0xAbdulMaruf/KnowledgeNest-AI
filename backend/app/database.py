from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./academic_platform.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def ensure_resource_soft_delete_columns() -> None:
    if not DATABASE_URL.startswith("sqlite"):
        return

    with engine.begin() as connection:
        columns = connection.execute(text("PRAGMA table_info(resources)")).fetchall()
        existing = {column[1] for column in columns}

        if "deleted_at" not in existing:
            connection.execute(text("ALTER TABLE resources ADD COLUMN deleted_at DATETIME"))
        if "deleted_by" not in existing:
            connection.execute(text("ALTER TABLE resources ADD COLUMN deleted_by VARCHAR"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
