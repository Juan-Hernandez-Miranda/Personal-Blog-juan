"""FastAPI routes for Reaccion operations."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.deps import get_db
from db.models.Post import Post
from db.models.Reacciones import Reaccion
from schemas import ReaccionCreate, ReaccionRead

router = APIRouter(prefix="/reacciones", tags=["Reacciones"])


def _ensure_post_exists(db: Session, post_id: int) -> None:
    if not db.get(Post, post_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post no valido")


@router.get("/", response_model=list[ReaccionRead])
def listar_reacciones(db: Session = Depends(get_db)):
    return db.query(Reaccion).order_by(Reaccion.fecha_creacion.desc()).all()


@router.get("/{reaccion_id}", response_model=ReaccionRead)
def obtener_reaccion(reaccion_id: int, db: Session = Depends(get_db)):
    reaccion = db.get(Reaccion, reaccion_id)
    if not reaccion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reaccion no encontrada")
    return reaccion


@router.post("/", response_model=ReaccionRead, status_code=status.HTTP_201_CREATED)
def crear_reaccion(payload: ReaccionCreate, db: Session = Depends(get_db)):
    _ensure_post_exists(db, payload.post_id)
    reaccion = Reaccion(**payload.model_dump())
    db.add(reaccion)
    db.commit()
    db.refresh(reaccion)
    return reaccion


@router.delete("/{reaccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_reaccion(reaccion_id: int, db: Session = Depends(get_db)):
    reaccion = db.get(Reaccion, reaccion_id)
    if not reaccion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reaccion no encontrada")

    db.delete(reaccion)
    db.commit()
    return None
