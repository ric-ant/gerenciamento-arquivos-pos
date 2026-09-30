"""
Configuração do banco de dados SQLite usando SQLAlchemy.
"""

from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# ------------------------------------------------------------------ #
# Caminho do banco
# ------------------------------------------------------------------ #

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# ------------------------------------------------------------------ #
# Engine
# ------------------------------------------------------------------ #

engine = create_engine(
    DATABASE_URL,
    echo=False,
)


# ------------------------------------------------------------------ #
# Base dos modelos
# ------------------------------------------------------------------ #

class Base(DeclarativeBase):
    pass


# ------------------------------------------------------------------ #
# Sessão
# ------------------------------------------------------------------ #

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_session():
    """Retorna uma sessão do banco."""
    return SessionLocal()


# ------------------------------------------------------------------ #
# Verificação da conexão
# ------------------------------------------------------------------ #

def verificar_conexao() -> bool:
    """Verifica se o SQLite está funcionando."""

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except Exception:
        return False


# ------------------------------------------------------------------ #
# Criação das tabelas
# ------------------------------------------------------------------ #

def criar_tabelas():
    """Cria as tabelas dos modelos."""

    Base.metadata.create_all(bind=engine)
