"""Convenience helpers to mount routers."""

from fastapi import FastAPI

from . import categorias, comentarios, posts, reacciones


def register_routers(app: FastAPI) -> None:
	"""Attach every router to the FastAPI app."""
	app.include_router(categorias.router)
	app.include_router(posts.router)
	app.include_router(comentarios.router)
	app.include_router(reacciones.router)


__all__ = ["register_routers"]