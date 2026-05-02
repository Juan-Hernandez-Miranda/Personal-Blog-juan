# Permite que models sea tratado como un paquete Python
from .User import User
from .Post import Post
from .Categoria import Categoria
from .Comentario import Comentario
from .Reacciones import Reaccion
from .Proyectos import Proyecto

__all__ = ["User", "Post", "Categoria", "Comentario", "Reaccion", "Proyecto"]