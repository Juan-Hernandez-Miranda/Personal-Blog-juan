"""FastAPI routes for Comentario operations."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.deps import get_db
from db.models.Comentario import Comentario
from db.models.Post import Post
from schemas import ComentarioCreate, ComentarioRead, ComentarioUpdate

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])


def _ensure_post_exists(db: Session, post_id: int) -> None:
    if not db.get(Post, post_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post no valido")


@router.get("/", response_model=list[ComentarioRead])
def listar_comentarios(db: Session = Depends(get_db)):
    return db.query(Comentario).order_by(Comentario.fecha_creacion.desc()).all()


@router.get("/{comentario_id}", response_model=ComentarioRead)
def obtener_comentario(comentario_id: int, db: Session = Depends(get_db)):
    comentario = db.get(Comentario, comentario_id)
    if not comentario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentario no encontrado")
    return comentario


@router.post("/", response_model=ComentarioRead, status_code=status.HTTP_201_CREATED)
def crear_comentario(payload: ComentarioCreate, db: Session = Depends(get_db)):
    _ensure_post_exists(db, payload.post_id)
    comentario = Comentario(**payload.model_dump())
    db.add(comentario)
    db.commit()
    db.refresh(comentario)
    return comentario


@router.put("/{comentario_id}", response_model=ComentarioRead)
def actualizar_comentario(
    comentario_id: int,
    payload: ComentarioUpdate,
    db: Session = Depends(get_db),
):
    comentario = db.get(Comentario, comentario_id)
    if not comentario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentario no encontrado")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(comentario, field, value)

    db.commit()
    db.refresh(comentario)
    return comentario


@router.delete("/{comentario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_comentario(comentario_id: int, db: Session = Depends(get_db)):
    comentario = db.get(Comentario, comentario_id)
    if not comentario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentario no encontrado")

    db.delete(comentario)
    db.commit()
    return None
