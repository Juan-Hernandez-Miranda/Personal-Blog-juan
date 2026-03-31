"""Pydantic schemas for Comentario resources."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ComentarioBase(BaseModel):
    post_id: int
    nombre_usuario: Optional[str] = None
    contenido: str


class ComentarioCreate(ComentarioBase):
    """Schema for creating a comment."""


class ComentarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    contenido: Optional[str] = None


class ComentarioRead(ComentarioBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
