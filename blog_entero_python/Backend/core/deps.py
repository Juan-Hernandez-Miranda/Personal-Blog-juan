"""Reusable FastAPI dependencies."""

from collections.abc import Generator
from sqlalchemy.orm import Session

from db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield a transactional SQLAlchemy session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
