"""
Docstring for Personal-Blog-juan.blog_entero_python.Backend.db.models.reacciones

este es el modelo de la base de datos para las reacciones 

reacciones

- id (PK)
- post_id (FK a posts)
- tipo ('like' o 'dislike')
- ip_usuario (opcional, para control básico)

"""




from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class Reaccion(Base):
    __tablename__ = "reacciones"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    es_like = Column(Boolean, nullable=False)
    nombre_usuario = Column(String(80), nullable=True)
    ip_usuario = Column(String(100), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("Post", back_populates="reacciones")
