"""
Página: Detalhes da Disciplina
"""

import streamlit as st

from app.database import get_session
from app.models import Disciplina
from app.repository import (
    adicionar_arquivo,
    atualizar_arquivo,
    atualizar_disciplina,
    buscar_por_id,
    excluir_arquivo,
    listar_arquivos,
)


# ================================================================== #
# CONFIGURAÇÃO
# ================================================================== #

st.set_page_config(
    page_title="Detalhes da Disciplina",
    page_icon="📚",
    layout="wide",
)


# ================================================================== #
# OBTER ID DA DISCIPLINA
# ================================================================== #

param_id = st.query_params.get("id")

if not param_id:
    st.error("Nenhuma disciplina foi selecionada.")

    if st.button("← Voltar para disciplinas"):
        st.switch_page("pages/listagem.py")

    st.stop()

try:
    disciplina_id = int(param_id)
except ValueError:
    st.error("ID da disciplina inválido.")
    st.stop()


# ================================================================== #
# CARREGAR DISCIPLINA E ARQUIVOS
# ================================================================== #

with get_session() as session:

    disciplina = buscar_por_id(
        session,
        disciplina_id,
    )

    if disciplina is None:
        st.error("Disciplina não encontrada.")
        st.stop()

    nome_disciplina = disciplina.nome
    codigo_disciplina = disciplina.codigo
    descricao_disciplina = disciplina.descricao
    semestre_disciplina = disciplina.semestre
    status_disciplina = disciplina.status

    arquivos = listar_arquivos(
        session,
        disciplina_id,
    )

    arquivos_data = [
        {
            "id": arquivo.id,
            "nome": arquivo.nome,
            "link": arquivo.link,
        }
        for arquivo in arquivos
    ]


# ================================================================== #
# CABEÇALHO
# ================================================================== #

if st.button("← Voltar para disciplinas"):
    st.switch_page("pages/listagem.py")

st.title(f"📚 {nome_disciplina}")

st.caption(
    f"Código: {codigo_disciplina}"
)


# ================================================================== #
# INFORMAÇÕES
# ================================================================== #

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Código",
        codigo_disciplina,
    )

with col2:
    st.metric(
        "Semestre",
        semestre_disciplina or "Não informado",
    )

with col3:

    if status_disciplina == Disciplina.STATUS_ATIVA:
        st.success("🟢 Ativa")

    elif status_disciplina == Disciplina.STATUS_CONCLUIDA:
        st.info("✅ Concluída")

    elif status_disciplina == Disciplina.STATUS_TRANCADA:
        st.error("🔴 Trancada")

    else:
        st.warning(status_disciplina)


# ================================================================== #
# DESCRIÇÃO
# ================================================================== #

if descricao_disciplina:

    st.markdown("### 📝 Descrição")

    st.write(
        descricao_disciplina
    )


st.divider()


# ================================================================== #
# ARQUIVOS
# ================================================================== #




st.markdown("### 📎 Arquivos")




if not arquivos_data:

    st.info(
        "Nenhum arquivo cadastrado para esta disciplina."
    )

else:

    for arquivo in arquivos_data:

        arquivo_id = arquivo["id"]

        chave_edicao = f"editando_arquivo_{arquivo_id}"

        if chave_edicao not in st.session_state:
            st.session_state[chave_edicao] = False

        with st.container(border=True):

            # ====================================================== #
            # MODO DE EDIÇÃO
            # ====================================================== #

            if st.session_state[chave_edicao]:

                st.markdown("#### ✏️ Editando arquivo")

                with st.form(
                    key=f"form_editar_arquivo_{arquivo_id}"
                ):

                    nome_editado = st.text_input(
                        "Nome do arquivo",
                        value=arquivo["nome"],
                    )

                    link_editado = st.text_input(
                        "🔗 Link do arquivo",
                        value=arquivo["link"],
                        help="Altere aqui o endereço do arquivo.",
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        salvar = st.form_submit_button(
                            "💾 Salvar alterações",
                            use_container_width=True,
                        )

                    with col2:
                        cancelar = st.form_submit_button(
                            "❌ Cancelar",
                            use_container_width=True,
                        )

                # ================================================== #
                # SALVAR ALTERAÇÕES
                # ================================================== #

                if salvar:

                    nome_editado = nome_editado.strip()
                    link_editado = link_editado.strip()

                    if not nome_editado:

                        st.error(
                            "O nome do arquivo é obrigatório."
                        )

                    elif not link_editado:

                        st.error(
                            "O link do arquivo é obrigatório."
                        )

                    else:

                        try:

                            with get_session() as session:

                                atualizar_arquivo(
                                    session,
                                    arquivo_id,
                                    nome=nome_editado,
                                    link=link_editado,
                                )

                                session.commit()

                            st.session_state[
                                chave_edicao
                            ] = False

                            st.success(
                                "✅ Arquivo atualizado com sucesso!"
                            )

                            st.rerun()

                        except Exception as exc:

                            st.error(
                                f"❌ Erro ao atualizar arquivo: {exc}"
                            )

                # ================================================== #
                # CANCELAR
                # ================================================== #

                if cancelar:

                    st.session_state[
                        chave_edicao
                    ] = False

                    st.rerun()

            # ====================================================== #
            # MODO DE VISUALIZAÇÃO
            # ====================================================== #

            else:

                st.markdown(
                    f"#### 📄 {arquivo['nome']}"
                )

                st.caption(
                    arquivo["link"]
                )

                col1, col2, col3 = st.columns(3)

                # -------------------------------------------------- #
                # ABRIR
                # -------------------------------------------------- #

                with col1:

                    st.link_button(
                        "🔗 Abrir arquivo",
                        arquivo["link"],
                        use_container_width=True,
                    )

                # -------------------------------------------------- #
                # EDITAR
                # -------------------------------------------------- #

                with col2:

                    if st.button(
                        "✏️ Editar",
                        key=f"editar_{arquivo_id}",
                        use_container_width=True,
                    ):

                        st.session_state[
                            chave_edicao
                        ] = True

                        st.rerun()

                # -------------------------------------------------- #
                # EXCLUIR
                # -------------------------------------------------- #

                with col3:

                    if st.button(
                        "🗑️ Excluir",
                        key=f"excluir_{arquivo_id}",
                        use_container_width=True,
                    ):

                        try:

                            with get_session() as session:

                                excluir_arquivo(
                                    session,
                                    arquivo_id,
                                )

                                session.commit()

                            st.success(
                                "🗑️ Arquivo excluído com sucesso!"
                            )

                            st.rerun()

                        except Exception as exc:

                            st.error(
                                f"❌ Erro ao excluir arquivo: {exc}"
                            )


# ================================================================== #
# ADICIONAR NOVO ARQUIVO
# ================================================================== #

st.divider()

st.markdown("### ➕ Adicionar arquivo")


with st.form("form_adicionar_arquivo"):

    novo_nome = st.text_input(
        "Nome do arquivo",
        placeholder="Ex: Lista de exercícios 01",
    )

    novo_link = st.text_input(
        "🔗 Link do arquivo",
        placeholder="https://...",
    )

    adicionar = st.form_submit_button(
        "📎 Adicionar arquivo",
        use_container_width=True,
    )


if adicionar:

    novo_nome = novo_nome.strip()
    novo_link = novo_link.strip()

    if not novo_nome:

        st.error(
            "O nome do arquivo é obrigatório."
        )

    elif not novo_link:

        st.error(
            "O link do arquivo é obrigatório."
        )

    else:

        try:

            with get_session() as session:

                adicionar_arquivo(
                    session,
                    disciplina_id=disciplina_id,
                    nome=novo_nome,
                    link=novo_link,
                )

                session.commit()

            st.success(
                "✅ Arquivo adicionado com sucesso!"
            )

            st.rerun()

        except Exception as exc:

            st.error(
                f"❌ Erro ao adicionar arquivo: {exc}"
            )


# ================================================================== #
# EDITAR DISCIPLINA
# ================================================================== #

st.divider()

with st.expander("✏️ Editar dados da disciplina"):

    with st.form("form_editar_disciplina"):

        novo_nome = st.text_input(
            "Nome",
            value=nome_disciplina,
        )

        novo_codigo = st.text_input(
            "Código",
            value=codigo_disciplina,
        )

        novo_semestre = st.text_input(
            "Semestre",
            value=semestre_disciplina or "",
        )

        novo_status = st.selectbox(
            "Status",
            options=Disciplina.STATUS_OPCOES,
            index=Disciplina.STATUS_OPCOES.index(
                status_disciplina
            ),
        )

        nova_descricao = st.text_area(
            "Descrição",
            value=descricao_disciplina or "",
        )

        salvar_disciplina = st.form_submit_button(
            "💾 Salvar disciplina",
            use_container_width=True,
        )

    if salvar_disciplina:

        novo_nome = novo_nome.strip()
        novo_codigo = novo_codigo.strip().upper()
        novo_semestre = novo_semestre.strip()
        nova_descricao = nova_descricao.strip()

        if not novo_nome:

            st.error(
                "O nome da disciplina é obrigatório."
            )

        elif not novo_codigo:

            st.error(
                "O código da disciplina é obrigatório."
            )

        else:

            try:

                with get_session() as session:

                    atualizar_disciplina(
                        session,
                        disciplina_id,
                        nome=novo_nome,
                        codigo=novo_codigo,
                        semestre=novo_semestre or None,
                        status=novo_status,
                        descricao=nova_descricao or None,
                    )

                    session.commit()

                st.success(
                    "✅ Disciplina atualizada com sucesso!"
                )

                st.rerun()

            except Exception as exc:

                st.error(
                    f"❌ Erro ao atualizar disciplina: {exc}"
                )
