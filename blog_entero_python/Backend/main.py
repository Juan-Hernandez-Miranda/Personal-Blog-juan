"""
codigo fuente de el blog en el cual estare trabajando en mis vacaciones y 
tengo que terminar antes de que entre otra vez a clases este en donde va converger todo
"""

#tener en cuenta que si quiero activar el entorno virtual debe ser en la carpeta "backend"

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel


import os

app = FastAPI()

# para activar el servidor debo escribir: uvicorn main:app --reload
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


@app.get("/")
async def root():
    return RedirectResponse(url="/frontend/index.html")
