"""Pydantic schemas for Reaccion resources."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReaccionBase(BaseModel):
    post_id: int
    es_like: bool
    nombre_usuario: Optional[str] = None
    ip_usuario: Optional[str] = None


class ReaccionCreate(ReaccionBase):
    """Schema for creating a reaction."""


class ReaccionRead(ReaccionBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
