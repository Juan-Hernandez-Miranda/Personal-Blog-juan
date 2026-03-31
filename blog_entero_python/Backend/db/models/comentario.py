"""
Docstring for Personal-Blog-juan.blog_entero_python.Backend.db.models.comentario

en este documento voy a hacer el modelo de la tabal de la base de datos de comentario

comentarios

- id (PK)
- post_id (FK a posts)
- nombre_usuario (o nickname, ya que no hay login)
- contenido
- fecha_creacion

"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base



class Comentario(Base):
    __tablename__ = "comentario"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    nombre_usuario = Column(String(80), nullable=True)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("Post", back_populates="comentarios")



#ejemplo de enpoint para contar los comentario 

# @router.get("/posts/{post_id}/comentarios/count", response_model=int)
# def contar_comentarios(post_id: int, db: Session = Depends(get_db)):
#     total = db.query(Comentario).filter_by(post_id=post_id).count()
#     return total