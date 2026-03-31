"""
Docstring for Personal-Blog-juan.blog_entero_python.Backend.db.models.proyectos

en este documento vamos hacer el modelo de la base de datos de proyectos

proyectos (para el portfolio)

id (PK)
nombre
descripcion
url_repo (enlace al repositorio)
imagen_url (opcional)

"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from db.database import Base


class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(120), nullable=False)
    descripcion = Column(String(300), nullable=False)
    url_repo = Column(String(255), nullable=False)
    imagen_url = Column(String(255), nullable=True)

    @validates("url_repo")
    def validar_url(self, key, value):
        if not value or not value.startswith("http"):
            raise ValueError("url_repo debe ser una URL válida")
        return value


