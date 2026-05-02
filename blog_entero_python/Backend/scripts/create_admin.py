#!/usr/bin/env python
"""
Script para crear el primer usuario admin en la base de datos.
Uso: python create_admin.py
"""

import sys
import os
from pathlib import Path

# Agregar el directorio Backend al path para importar módulos locales
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from core.security import hash_password
from db.database import engine, SessionLocal, Base
from db.models import User
from sqlalchemy.orm import Session

def create_admin_user(db: Session, username: str, email: str, password: str):
    """
    Crea un usuario admin en la base de datos.
    
    Args:
        db: Session de base de datos
        username: Nombre de usuario (ej: "admin")
        email: Email del admin
        password: Contraseña sin hash (será hasheada)
    
    Returns:
        User creado o None si ya existe
    """
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        print(f"❌ Error: El usuario '{username}' o email '{email}' ya existe.")
        return None
    
    # Crear nuevo usuario admin
    hashed_pwd = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_pwd,
        is_active=True,
        is_admin=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"✅ Usuario admin '{username}' creado exitosamente.")
    print(f"   Email: {email}")
    print(f"   ID: {new_user.id}")
    
    return new_user

def main():
    """Función principal del script."""
    print("=" * 60)
    print("Crear usuario ADMIN para el blog")
    print("=" * 60)
    
    # Crear todas las tablas (User table se crea aquí si no existe)
    Base.metadata.create_all(bind=engine)
    
    # Obtener sesión de base de datos
    db = SessionLocal()
    
    try:
        # Solicitar datos al usuario
        print("\nIngresa los datos para el nuevo usuario admin:")
        
        username = input("Nombre de usuario (ej: admin): ").strip()
        if not username:
            username = "admin"
        
        email = input("Email (ej: admin@blog.com): ").strip()
        if not email:
            email = "admin@blog.com"
        
        password = input("Contraseña: ").strip()
        if not password:
            password = "admin123"
        
        # Validar longitud mínima
        if len(password) < 6:
            print("❌ Error: La contraseña debe tener al menos 6 caracteres.")
            return
        
        # Crear el admin
        user = create_admin_user(db, username, email, password)
        
        if user:
            print("\n✅ El usuario admin ha sido creado correctamente.")
            print("   Puedes usar estas credenciales en /frontend/login.html")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
