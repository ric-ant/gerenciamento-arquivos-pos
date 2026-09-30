"""
Modelos SQLAlchemy para o sistema de gerenciamento de disciplinas.
Banco de dados: SQLite
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Disciplina(Base):
    """Representa uma disciplina acadêmica."""

    __tablename__ = "disciplinas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    nome: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    codigo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    semestre: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ativa",
    )

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )

    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    # -------------------------------------------------------------- #
    # Relacionamento com arquivos
    # -------------------------------------------------------------- #

    arquivos: Mapped[list["Arquivo"]] = relationship(
        back_populates="disciplina",
        cascade="all, delete-orphan",
        order_by="Arquivo.nome",
    )

    # -------------------------------------------------------------- #
    # Status válidos
    # -------------------------------------------------------------- #

    STATUS_ATIVA = "ativa"
    STATUS_CONCLUIDA = "concluída"
    STATUS_TRANCADA = "trancada"

    STATUS_OPCOES = [
        STATUS_ATIVA,
        STATUS_CONCLUIDA,
        STATUS_TRANCADA,
    ]

    def __repr__(self) -> str:
        return (
            f"<Disciplina "
            f"id={self.id} "
            f"codigo={self.codigo!r} "
            f"nome={self.nome!r}>"
        )


class Arquivo(Base):
    """Representa um arquivo/link associado a uma disciplina."""

    __tablename__ = "arquivos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    disciplina_id: Mapped[int] = mapped_column(
        ForeignKey(
            "disciplinas.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    nome: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    link: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )

    disciplina: Mapped["Disciplina"] = relationship(
        back_populates="arquivos",
    )

    def __repr__(self) -> str:
        return (
            f"<Arquivo "
            f"id={self.id} "
            f"nome={self.nome!r} "
            f"disciplina_id={self.disciplina_id}>"
        )
