"""Reusable FastAPI dependencies."""

from collections.abc import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db.models.User import User
from core.security import decode_token

security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    """Yield a transactional SQLAlchemy session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    credentials = Depends(security),
) -> User:
    """
    Obtiene el usuario actual del token JWT.
    Si el token es inválido o no existe, lanza una excepción 401.
    
    Args:
        db: Sesión de base de datos
        credentials: Credenciales HTTP (Bearer token)
        
    Returns:
        Usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    token = credentials.credentials
    
    token_data = decode_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    return user


def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Verifica que el usuario actual sea administrador.
    Solo admins pueden crear, editar y eliminar posts.
    
    Args:
        current_user: Usuario autenticado
        
    Returns:
        Usuario si es admin
        
    Raises:
        HTTPException: Si el usuario no es admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permiso denegado. Solo administradores pueden realizar esta acción.",
        )
    
    return current_user

