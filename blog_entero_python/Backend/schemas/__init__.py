"""Expose schema classes for convenient imports."""

from .categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate
from .post import PostCreate, PostRead, PostUpdate
from .comentario import ComentarioCreate, ComentarioRead, ComentarioUpdate
from .reaccion import ReaccionCreate, ReaccionRead

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
]
