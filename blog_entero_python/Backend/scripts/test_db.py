"""Quick connectivity check against the configured database."""
from pathlib import Path
import sys

from sqlalchemy import text

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from db.database import SessionLocal


def test_connection() -> None:
    session = SessionLocal()
    try:
        session.execute(text("SELECT 1"))
        print("Conexion exitosa a la base de datos.")
    except Exception as exc:  # pragma: no cover - diagnostic helper
        print("Error de conexion:", exc)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    test_connection()
