"""Pydantic schemas for Categoria resources."""

from typing import Optional
from pydantic import BaseModel


class CategoriaBase(BaseModel):
    nombre: str


class CategoriaCreate(CategoriaBase):
    """Schema for creating a category."""


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None


class CategoriaRead(CategoriaBase):
    id: int

    class Config:
        from_attributes = True
