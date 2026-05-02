"""Expose schema classes for convenient imports."""

from .categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate
from .post import PostCreate, PostRead, PostUpdate
from .comentario import ComentarioCreate, ComentarioRead, ComentarioUpdate
from .reaccion import ReaccionCreate, ReaccionRead
from .user import UserCreate, UserLogin, UserRead, Token, TokenData

__all__ = [
    "CategoriaCreate",
    "CategoriaRead",
    "CategoriaUpdate",
    "PostCreate",
    "PostRead",
    "PostUpdate",
    "ComentarioCreate",
    "ComentarioRead",
    "ComentarioUpdate",
    "ReaccionCreate",
    "ReaccionRead",
    "UserCreate",
    "UserLogin",
    "UserRead",
    "Token",
    "TokenData",
]
