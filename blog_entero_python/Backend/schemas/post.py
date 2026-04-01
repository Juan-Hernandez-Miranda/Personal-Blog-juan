"""Pydantic schemas for Post resources."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostBase(BaseModel): #este lo que hace es el esquema d ela informacion de los post, es basicamente la informacion que ira en la base de datos
    titulo: str
    descripcion: Optional[str] = None
    contenido: str
    categoria_id: int
    imagen_url: Optional[str] = None


class PostCreate(PostBase):
    """Schema for creating a post."""


class PostUpdate(BaseModel): # esto es por si quieres actualizar un post, todo es opcional por si no quieres cambiar todo slos datos y solo alguno
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    contenido: Optional[str] = None
    categoria_id: Optional[int] = None
    imagen_url: Optional[str] = None


class PostRead(PostBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
