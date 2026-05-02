"""FastAPI routes for authentication."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.deps import get_db
from core.security import hash_password, verify_password, create_access_token
from db.models.User import User
from schemas.user import UserCreate, UserLogin, UserRead, Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario.
    NOTA: En producción, este endpoint debería estar protegido o deshabilitado.
    Solo deberías crear admins manualmente a través de la base de datos.
    
    Args:
        payload: Datos del nuevo usuario (username, email, password)
        db: Sesión de base de datos
        
    Returns:
        Datos del usuario creado
        
    Raises:
        HTTPException: Si el usuario o email ya existen
    """
    # Verificar que el usuario no exista
    existing_user = db.query(User).filter(
        (User.username == payload.username) | (User.email == payload.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario o email ya existen",
        )
    
    # Crear nuevo usuario
    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        is_active=True,
        is_admin=False,  # Los nuevos usuarios NO son admins por defecto
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Inicia sesión y retorna un JWT token.
    
    Args:
        payload: Credenciales (username, password)
        db: Sesión de base de datos
        
    Returns:
        Token de acceso y datos del usuario
        
    Raises:
        HTTPException: Si las credenciales son inválidas
    """
    # Buscar usuario por username
    user = db.query(User).filter(User.username == payload.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    
    # Verificar contraseña
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    
    # Verificar que el usuario esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    # Crear token JWT
    access_token = create_access_token(
        data={"user_id": user.id, "username": user.username}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }


@router.post("/logout")
def logout():
    """
    Endpoint de logout (logout se maneja en el frontend eliminando el token).
    Este endpoint existe solo por simetría con lo que espera el frontend.
    
    Returns:
        Mensaje de logout
    """
    return {"message": "Logout exitoso"}
