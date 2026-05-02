"""
Modelo de Usuario para autenticación del blog.
Solo el administrador puede crear, editar y eliminar posts.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  # Solo admins pueden crear/editar/eliminar posts
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con posts que ha creado
    posts = relationship(
        "Post",
        back_populates="autor",
        foreign_keys="Post.autor_id",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, is_admin={self.is_admin})>"
