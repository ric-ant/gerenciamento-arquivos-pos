"""
Repositório — funções de acesso a dados.

Todas as funções recebem uma Session SQLAlchemy como primeiro argumento.
"""

from sqlalchemy import distinct, select
from sqlalchemy.orm import Session

from app.models import Arquivo, Disciplina


# ================================================================== #
# DISCIPLINAS — CREATE
# ================================================================== #

def criar_disciplina(
    session: Session,
    *,
    nome: str,
    codigo: str,
    descricao: str | None = None,
    semestre: str | None = None,
    status: str = Disciplina.STATUS_ATIVA,
) -> Disciplina:
    """Cria uma nova disciplina."""

    disciplina = Disciplina(
        nome=nome,
        codigo=codigo,
        descricao=descricao,
        semestre=semestre,
        status=status,
    )

    session.add(disciplina)
    session.flush()
    session.refresh(disciplina)

    return disciplina


# ================================================================== #
# DISCIPLINAS — READ
# ================================================================== #

def listar_disciplinas(
    session: Session,
    *,
    status: str | None = None,
    semestre: str | None = None,
) -> list[Disciplina]:
    """Lista disciplinas com filtros opcionais."""

    stmt = (
        select(Disciplina)
        .order_by(Disciplina.id)
    )

    if status:
        stmt = stmt.where(
            Disciplina.status == status
        )

    if semestre:
        stmt = stmt.where(
            Disciplina.semestre == semestre
        )

    return list(
        session.scalars(stmt).all()
    )


def buscar_por_id(
    session: Session,
    disciplina_id: int,
) -> Disciplina | None:
    """Busca uma disciplina pelo ID."""

    return session.get(
        Disciplina,
        disciplina_id,
    )


def buscar_por_codigo(
    session: Session,
    codigo: str,
) -> Disciplina | None:
    """Busca uma disciplina pelo código."""

    stmt = (
        select(Disciplina)
        .where(Disciplina.codigo == codigo)
    )

    return session.scalars(stmt).first()


def listar_semestres(
    session: Session,
) -> list[str]:
    """Lista os semestres distintos."""

    stmt = (
        select(distinct(Disciplina.semestre))
        .where(Disciplina.semestre.is_not(None))
        .order_by(Disciplina.semestre)
    )

    return [
        semestre
        for semestre in session.scalars(stmt).all()
        if semestre
    ]


# ================================================================== #
# DISCIPLINAS — UPDATE
# ================================================================== #

def atualizar_disciplina(
    session: Session,
    disciplina_id: int,
    *,
    nome: str | None = None,
    codigo: str | None = None,
    descricao: str | None = None,
    semestre: str | None = None,
    status: str | None = None,
) -> Disciplina:
    """Atualiza uma disciplina existente."""

    disciplina = buscar_por_id(
        session,
        disciplina_id,
    )

    if disciplina is None:
        raise ValueError(
            f"Disciplina com id={disciplina_id} "
            "não encontrada."
        )

    if nome is not None:
        disciplina.nome = nome

    if codigo is not None:
        disciplina.codigo = codigo

    if descricao is not None:
        disciplina.descricao = descricao

    if semestre is not None:
        disciplina.semestre = semestre

    if status is not None:
        disciplina.status = status

    session.flush()
    session.refresh(disciplina)

    return disciplina


# ================================================================== #
# DISCIPLINAS — DELETE
# ================================================================== #

def excluir_disciplina(
    session: Session,
    disciplina_id: int,
) -> None:
    """Exclui uma disciplina e seus arquivos."""

    disciplina = buscar_por_id(
        session,
        disciplina_id,
    )

    if disciplina is None:
        raise ValueError(
            f"Disciplina com id={disciplina_id} "
            "não encontrada."
        )

    session.delete(disciplina)
    session.flush()


# ================================================================== #
# ARQUIVOS — CREATE
# ================================================================== #

def adicionar_arquivo(
    session: Session,
    *,
    disciplina_id: int,
    nome: str,
    link: str,
) -> Arquivo:
    """Adiciona um arquivo a uma disciplina."""

    disciplina = buscar_por_id(
        session,
        disciplina_id,
    )

    if disciplina is None:
        raise ValueError(
            f"Disciplina com id={disciplina_id} "
            "não encontrada."
        )

    arquivo = Arquivo(
        disciplina_id=disciplina_id,
        nome=nome,
        link=link,
    )

    session.add(arquivo)
    session.flush()
    session.refresh(arquivo)

    return arquivo


# ================================================================== #
# ARQUIVOS — READ
# ================================================================== #

def listar_arquivos(
    session: Session,
    disciplina_id: int,
) -> list[Arquivo]:
    """Lista os arquivos de uma disciplina."""

    stmt = (
        select(Arquivo)
        .where(
            Arquivo.disciplina_id == disciplina_id
        )
        .order_by(Arquivo.nome)
    )

    return list(
        session.scalars(stmt).all()
    )


def buscar_arquivo_por_id(
    session: Session,
    arquivo_id: int,
) -> Arquivo | None:
    """Busca um arquivo pelo ID."""

    return session.get(
        Arquivo,
        arquivo_id,
    )


# ================================================================== #
# ARQUIVOS — UPDATE
# ================================================================== #

def atualizar_arquivo(
    session: Session,
    arquivo_id: int,
    *,
    nome: str | None = None,
    link: str | None = None,
) -> Arquivo:
    """Atualiza um arquivo."""

    arquivo = buscar_arquivo_por_id(
        session,
        arquivo_id,
    )

    if arquivo is None:
        raise ValueError(
            f"Arquivo com id={arquivo_id} "
            "não encontrado."
        )

    if nome is not None:
        arquivo.nome = nome

    if link is not None:
        arquivo.link = link

    session.flush()
    session.refresh(arquivo)

    return arquivo


# ================================================================== #
# ARQUIVOS — DELETE
# ================================================================== #

def excluir_arquivo(
    session: Session,
    arquivo_id: int,
) -> None:
    """Exclui um arquivo."""

    arquivo = buscar_arquivo_por_id(
        session,
        arquivo_id,
    )

    if arquivo is None:
        raise ValueError(
            f"Arquivo com id={arquivo_id} "
            "não encontrado."
        )

    session.delete(arquivo)
    session.flush()
