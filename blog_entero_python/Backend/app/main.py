"""
codigo fuente de el blog en el cual estare trabajando en mis vacaciones y 
tengo que terminar antes de que entre otra vez a clases este en donde va converger todo
"""


# para iniciar el entorno virtual debes usar el sigueinte comando "   . "C:/Users/miran/.virtualenvs/blog-backend/Scripts/Activate.ps1"  "
# tener en cuenta que si quiero activar el entorno virtual debe ser en la carpeta "backend"

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from db.database import Base, engine
from routers import register_routers


import os

app = FastAPI()
@app.on_event("startup")
def startup_event():
    """Ensure all SQLAlchemy models create their tables on boot."""
    Base.metadata.create_all(bind=engine)

# para activar el servidor debo escribir: uvicorn main:app --reload
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Static assets viven en Backend/static, subimos un nivel para apuntar bien.
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")
# El frontend vive fuera de Backend, por eso subimos dos niveles.
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "..", "frontend")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static") ## esto es para que el servidor detecte que estos directorios necesitan
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
register_routers(app)


@app.get("/")
async def root(): ## esto lo que nos dice es que incia la pagina en index y ade ahi se va a las otras paginas
    return RedirectResponse(url="/frontend/index.html")
