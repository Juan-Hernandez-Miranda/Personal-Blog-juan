
"""


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
autor_id (FK a users) - quien creó el post
estado (draft, published, archived)
"""

from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base
import enum


class EstadoPost(str, enum.Enum):
    """Estados posibles de un post."""
    DRAFT = "draft"  # Borrador
    PUBLISHED = "published"  # Publicado
    ARCHIVED = "archived"  # Archivado


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    imagen_url = Column(String(200), nullable=True)
    
    # Nuevo: autor del post (quién lo creó)
    autor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Nuevo: estado del post (draft, published, archived)
    estado = Column(Enum(EstadoPost), default=EstadoPost.DRAFT, nullable=False)

    # Destacado: aparece en "Best in the Month"
    destacado = Column(Boolean, default=False, nullable=False, server_default='0')
    
    # Relaciones
    categoria = relationship("Categoria", back_populates="posts")
    autor = relationship("User", back_populates="posts", foreign_keys=[autor_id])
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