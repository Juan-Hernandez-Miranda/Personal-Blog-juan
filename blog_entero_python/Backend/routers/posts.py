"""FastAPI routes for Post operations."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.deps import get_db
from db.models.Categoria import Categoria
from db.models.Comentario import Comentario
from db.models.Post import Post
from schemas import ComentarioRead, PostCreate, PostRead, PostUpdate

router = APIRouter(prefix="/posts", tags=["Posts"])


def _ensure_categoria_exists(db: Session, categoria_id: int) -> None:
    if not db.get(Categoria, categoria_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria no valida")


@router.get("/", response_model=list[PostRead])
def listar_posts(db: Session = Depends(get_db)):
    return db.query(Post).order_by(Post.fecha_creacion.desc()).all()


@router.get("/search", response_model=list[PostRead])
def buscar_posts(
    q: str = Query(..., min_length=1, description="Texto a buscar en el titulo del post"), ## este es el bucador de los post, es decir por si quieres aber cial es es    
    db: Session = Depends(get_db),
):
    termino = f"%{q.strip()}%"
    return (
        db.query(Post)
        .filter(Post.titulo.ilike(termino))
        .order_by(Post.fecha_creacion.desc())
        .all()
    )


@router.get("/{post_id}", response_model=PostRead)
def obtener_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")
    return post


@router.get("/{post_id}/comentarios", response_model=list[ComentarioRead])
def listar_comentarios_del_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    return (
        db.query(Comentario)
        .filter(Comentario.post_id == post_id)
        .order_by(Comentario.fecha_creacion.desc())
        .all()
    )


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def crear_post(payload: PostCreate, db: Session = Depends(get_db)):
    _ensure_categoria_exists(db, payload.categoria_id)
    post = Post(**payload.model_dump()) # "**" esto es para empaquetar los datos con clave valor
    db.add(post)
    db.commit() #aqui si se ejecuta el INSERT en la base de datos.
    db.refresh(post) # como se puede ver es uy obvio que lo que hace aqui es qactialia
    return post


@router.put("/{post_id}", response_model=PostRead)
def actualizar_post(post_id: int, payload: PostUpdate, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post: # si el post no existe es que lanza una exepcion ya qu eno se peude actualizar algo que no existe
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    update_data = payload.model_dump(exclude_unset=True) #lo que incluye aqui es los datos especificos de la actualizacion evitando los que no fueron cambiados
    if "categoria_id" in update_data:
        _ensure_categoria_exists(db, update_data["categoria_id"]) #lo que analiza este if es que si quieres cambiar la categoria si es asi anlaiza si esa categoria existe o no, porque si no exitr
    
    for field, value in update_data.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    db.delete(post)
    db.commit()
    return None
