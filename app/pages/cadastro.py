"""
Página: Cadastro de Nova Disciplina
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st

from app.database import get_session
from app.models import Disciplina
from app.repository import (
    adicionar_arquivo,
    buscar_por_codigo,
    criar_disciplina,
)


st.set_page_config(
    page_title="Cadastro de Disciplina",
    page_icon="📚",
)


# ================================================================== #
# Inicialização
# ================================================================== #

if "arquivos_cadastro" not in st.session_state:
    st.session_state.arquivos_cadastro = []


# ================================================================== #
# Funções auxiliares
# ================================================================== #

def adicionar_arquivo_formulario():
    """Adiciona um arquivo à lista temporária."""

    nome = st.session_state.arquivo_nome.strip()
    link = st.session_state.arquivo_link.strip()

    if not nome:
        st.warning("Informe o nome do arquivo.")
        return

    if not link:
        st.warning("Informe o link do arquivo.")
        return

    st.session_state.arquivos_cadastro.append(
        {
            "nome": nome,
            "link": link,
        }
    )

    st.session_state.arquivo_nome = ""
    st.session_state.arquivo_link = ""


def remover_arquivo_formulario(index: int):
    """Remove um arquivo da lista temporária."""

    st.session_state.arquivos_cadastro.pop(index)


# ================================================================== #
# Interface
# ================================================================== #

st.title("📚 Cadastro de Nova Disciplina")

st.markdown(
    "Preencha os campos abaixo para registrar "
    "uma nova disciplina."
)


with st.form(
    "form_cadastro",
    clear_on_submit=False,
):

    st.markdown("### 📖 Dados da Disciplina")

    col1, col2 = st.columns(2)

    with col1:

        nome = st.text_input(
            "Nome da disciplina *",
            placeholder="Ex: Cálculo I",
            max_chars=200,
        )

        codigo = st.text_input(
            "Código / Sigla *",
            placeholder="Ex: MAT101",
            max_chars=50,
        )

        semestre = st.text_input(
            "Semestre",
            placeholder="Ex: 2026/1",
            max_chars=20,
        )

    with col2:

        status = st.selectbox(
            "Status",
            options=Disciplina.STATUS_OPCOES,
            index=0,
        )

    descricao = st.text_area(
        "Descrição / Ementa",
        placeholder=(
            "Descreva o conteúdo ou ementa "
            "da disciplina..."
        ),
        height=120,
    )

    st.markdown("### 📎 Arquivos")

    st.caption(
        "Adicione os arquivos ou materiais relacionados "
        "à disciplina."
    )

    arquivo_col1, arquivo_col2 = st.columns(
        [1, 1]
    )

    with arquivo_col1:

        st.text_input(
            "Nome do arquivo",
            placeholder="Ex: Apostila de Cálculo",
            key="arquivo_nome",
        )

    with arquivo_col2:

        st.text_input(
            "Link do arquivo",
            placeholder="https://...",
            key="arquivo_link",
        )

    st.form_submit_button(
        "➕ Adicionar arquivo",
        on_click=adicionar_arquivo_formulario,
    )

    st.markdown("#### Arquivos adicionados")

    if st.session_state.arquivos_cadastro:

        for index, arquivo in enumerate(
            st.session_state.arquivos_cadastro
        ):

            col_nome, col_link, col_remover = (
                st.columns([2, 3, 1])
            )

            with col_nome:
                st.write(
                    f"📄 **{arquivo['nome']}**"
                )

            with col_link:
                st.write(arquivo["link"])

            with col_remover:

                st.form_submit_button(
                    "🗑️",
                    key=f"remover_{index}",
                    on_click=remover_arquivo_formulario,
                    args=(index,),
                )

    else:

        st.info(
            "Nenhum arquivo adicionado."
        )

    st.markdown("---")

    salvar = st.form_submit_button(
        "💾 Salvar disciplina",
        use_container_width=True,
        type="primary",
    )


# ================================================================== #
# Salvamento
# ================================================================== #

if salvar:

    erros = []

    if not nome.strip():
        erros.append(
            "O campo **Nome da disciplina** "
            "é obrigatório."
        )

    if not codigo.strip():
        erros.append(
            "O campo **Código / Sigla** "
            "é obrigatório."
        )

    if erros:

        for erro in erros:
            st.error(erro)

    else:

        session = get_session()

        try:

            codigo_formatado = (
                codigo.strip().upper()
            )

            # ------------------------------------------------------ #
            # Verificar código duplicado
            # ------------------------------------------------------ #

            existente = buscar_por_codigo(
                session,
                codigo_formatado,
            )

            if existente:

                st.error(
                    f"Já existe uma disciplina com o "
                    f"código **{codigo_formatado}** "
                    f"(ID {existente.id} — "
                    f"{existente.nome})."
                )

            else:

                # -------------------------------------------------- #
                # Criar disciplina
                # -------------------------------------------------- #

                disciplina = criar_disciplina(
                    session,
                    nome=nome.strip(),
                    codigo=codigo_formatado,
                    descricao=(
                        descricao.strip()
                        or None
                    ),
                    semestre=(
                        semestre.strip()
                        or None
                    ),
                    status=status,
                )

                # -------------------------------------------------- #
                # Criar arquivos
                # -------------------------------------------------- #

                for arquivo in (
                    st.session_state.arquivos_cadastro
                ):

                    adicionar_arquivo(
                        session,
                        disciplina_id=disciplina.id,
                        nome=arquivo["nome"],
                        link=arquivo["link"],
                    )

                # -------------------------------------------------- #
                # Commit
                # -------------------------------------------------- #

                session.commit()

                st.success(
                    f"✅ Disciplina **{disciplina.nome}** "
                    f"cadastrada com sucesso!"
                )

                if st.session_state.arquivos_cadastro:

                    st.info(
                        f"📎 "
                        f"{len(st.session_state.arquivos_cadastro)} "
                        f"arquivo(s) associado(s) à disciplina."
                    )

                # Limpar arquivos temporários
                st.session_state.arquivos_cadastro = []

        except Exception as exc:

            session.rollback()

            st.error(
                f"❌ Erro ao salvar no banco de dados: "
                f"{exc}"
            )

        finally:

            session.close()
