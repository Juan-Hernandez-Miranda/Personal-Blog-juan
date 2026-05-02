"""FastAPI routes for Post operations."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.deps import get_db, get_admin_user
from db.models.Categoria import Categoria
from db.models.Comentario import Comentario
from db.models.Post import Post
from db.models.User import User
from schemas import ComentarioRead, PostCreate, PostRead, PostUpdate

router = APIRouter(prefix="/posts", tags=["Posts"])


def _ensure_categoria_exists(db: Session, categoria_id: int) -> None:
    if not db.get(Categoria, categoria_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria no valida")


@router.get("/", response_model=list[PostRead])
def listar_posts(db: Session = Depends(get_db)):
    """
    Lista todos los posts publicados (PÚBLICAMENTE VISIBLE).
    Los visitantes solo ven posts con estado 'published'.
    """
    return db.query(Post).filter(
        Post.estado == "published"
    ).order_by(Post.fecha_creacion.desc()).all()


@router.get("/admin/all", response_model=list[PostRead])
def listar_todos_posts_admin(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Lista TODOS los posts (draft, published, archived) - solo para ADMINS.
    
    Args:
        admin: Usuario autenticado como admin
        db: Sesión de base de datos
        
    Returns:
        Lista de todos los posts
    """
    return db.query(Post).order_by(Post.fecha_creacion.desc()).all()


@router.get("/search", response_model=list[PostRead])
def buscar_posts(
    q: str = Query(..., min_length=1, description="Texto a buscar en el titulo del post"),
    db: Session = Depends(get_db),
):
    """
    Busca posts publicados por título (PÚBLICAMENTE VISIBLE).
    """
    termino = f"%{q.strip()}%"
    return (
        db.query(Post)
        .filter(
            (Post.titulo.ilike(termino)) &
            (Post.estado == "published")
        )
        .order_by(Post.fecha_creacion.desc())
        .all()
    )


@router.get("/{post_id}", response_model=PostRead)
def obtener_post(post_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un post específico.
    Solo muestra posts publicados a usuarios públicos.
    """
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")
    
    # Si el post está en draft o archivado, solo el admin puede verlo
    if post.estado != "published":
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
def crear_post(
    payload: PostCreate,
    admin: User = Depends(get_admin_user),  # Solo admins pueden crear
    db: Session = Depends(get_db)
):
    """
    PROTEGIDO: Crea un nuevo post.
    Solo ADMINISTRADORES pueden crear posts.
    El nuevo post se crea en estado 'draft' por defecto.
    
    Args:
        payload: Datos del post (título, contenido, etc)
        admin: Usuario autenticado como admin
        db: Sesión de base de datos
        
    Returns:
        Post creado
        
    Raises:
        HTTPException 403: Si el usuario no es admin
    """
    _ensure_categoria_exists(db, payload.categoria_id)
    
    post = Post(
        **payload.model_dump(),
        autor_id=admin.id,  # Asignar el admin como autor
        estado="draft"  # Los posts nuevos empiezan en draft
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=PostRead)
def actualizar_post(
    post_id: int,
    payload: PostUpdate,
    admin: User = Depends(get_admin_user),  # Solo admins pueden editar
    db: Session = Depends(get_db)
):
    """
    PROTEGIDO: Actualiza un post existente.
    Solo ADMINISTRADORES pueden editar posts.
    
    Args:
        post_id: ID del post a actualizar
        payload: Datos a actualizar
        admin: Usuario autenticado como admin
        db: Sesión de base de datos
        
    Returns:
        Post actualizado
        
    Raises:
        HTTPException 403: Si el usuario no es admin
        HTTPException 404: Si el post no existe
    """
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    update_data = payload.model_dump(exclude_unset=True)
    if "categoria_id" in update_data:
        _ensure_categoria_exists(db, update_data["categoria_id"])
    
    for field, value in update_data.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_post(
    post_id: int,
    admin: User = Depends(get_admin_user),  # Solo admins pueden eliminar
    db: Session = Depends(get_db)
):
    """
    PROTEGIDO: Elimina un post.
    Solo ADMINISTRADORES pueden eliminar posts.
    
    Args:
        post_id: ID del post a eliminar
        admin: Usuario autenticado como admin
        db: Sesión de base de datos
        
    Raises:
        HTTPException 403: Si el usuario no es admin
        HTTPException 404: Si el post no existe
    """
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")

    db.delete(post)
    db.commit()
    return None

