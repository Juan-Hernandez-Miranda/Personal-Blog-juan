"""
Docstring for Personal-Blog-juan.blog_entero_python.Backend.db.models.categoria

en este vamos a ver la tabla de las categorias de los  post

categorias

id (PK)
nombre
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60), nullable=False, unique=True)
    posts = relationship("Post", back_populates="categoria")