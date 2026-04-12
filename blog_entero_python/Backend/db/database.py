"""
Docstring for Personal-Blog-juan.blog_entero_python.Backend.db.database

lo que tendremos aqui es la conexion a la base de datos 
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Buscar .env relativo a la carpeta Backend (dos niveles arriba de este archivo)
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_BACKEND_DIR, ".env"))

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush= False,
    bind = engine
)

Base = declarative_base()