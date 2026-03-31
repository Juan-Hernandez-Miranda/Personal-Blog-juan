
"""
Docstring for Backend.models.Post

en este archivo lo que voy a hacer es modelar la que es posibelemente la tabla mas importante para la pagina web 
que son los psot los cuales es donde se va a guardar la informacion de los post no el contenido
si no todo la informacion que rodea a los post 

posts

id (PK)
titulo
contenido
fecha_creacion
categoria_id (FK a categorias)
likes (opcional, contador)
dislikes (opcional, contador)
imagen_url (opcional)
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    imagen_url = Column(String(200), nullable=True)
    categoria = relationship("Categoria", back_populates="posts")
    comentarios = relationship(
        "Comentario",
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=False,
    )
    reacciones = relationship(
        "Reaccion",
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=False,
    )