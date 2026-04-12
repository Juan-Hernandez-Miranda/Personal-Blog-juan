"""FastAPI routes for image uploads."""

import os
import uuid

from fastapi import APIRouter, HTTPException, UploadFile, File, status

router = APIRouter(prefix="/uploads", tags=["Uploads"])

# Carpeta donde se guardan las imágenes subidas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "imagenes", "posts")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_SIZE_MB = 5


@router.get("/imagenes")
def listar_imagenes():
    """Devuelve la lista de imágenes disponibles en el servidor."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    archivos = []
    for nombre in sorted(os.listdir(UPLOAD_DIR)):
        ext = os.path.splitext(nombre)[1].lower()
        if ext in ALLOWED_EXTENSIONS:
            archivos.append({
                "nombre": nombre,
                "imagen_url": f"/static/imagenes/posts/{nombre}",
            })
    return archivos


@router.post("/imagen", status_code=status.HTTP_201_CREATED)
async def subir_imagen(file: UploadFile = File(...)):
    # Validar extensión
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato no permitido. Usa: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Leer contenido y validar tamaño
    contenido = await file.read()
    if len(contenido) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La imagen supera el limite de {MAX_SIZE_MB} MB",
        )

    # Generar nombre único para evitar colisiones
    nombre_archivo = f"{uuid.uuid4().hex}{ext}"
    ruta_destino = os.path.join(UPLOAD_DIR, nombre_archivo)

    # Crear carpeta si no existe
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Guardar archivo
    with open(ruta_destino, "wb") as f:
        f.write(contenido)

    # Devolver la URL relativa que el frontend puede usar
    imagen_url = f"/static/imagenes/posts/{nombre_archivo}"
    return {"imagen_url": imagen_url, "nombre": nombre_archivo}
