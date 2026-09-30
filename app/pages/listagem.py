"""
Página: Listagem de Disciplinas
"""

import streamlit as st

from app.database import get_session
from app.models import Disciplina
from app.repository import (
    adicionar_arquivo,
    atualizar_arquivo,
    excluir_arquivo,
    listar_arquivos,
    listar_disciplinas,
    listar_semestres,
)


st.set_page_config(
    page_title="Listar Disciplinas",
    page_icon="📋",
    layout="wide",
)


st.title("📋 Disciplinas")

st.markdown(
    "Consulte, filtre e acesse as disciplinas cadastradas."
)


# ================================================================== #
# FILTROS
# ================================================================== #

with get_session() as session:
    semestres = listar_semestres(session)


col1, col2 = st.columns(2)


with col1:

    filtro_status = st.selectbox(
        "Status",
        options=["Todos"] + Disciplina.STATUS_OPCOES,
    )


with col2:

    filtro_semestre = st.selectbox(
        "Semestre",
        options=["Todos"] + semestres,
    )


status = (
    None
    if filtro_status == "Todos"
    else filtro_status
)


semestre = (
    None
    if filtro_semestre == "Todos"
    else filtro_semestre
)


# ================================================================== #
# DISCIPLINAS
# ================================================================== #

with get_session() as session:

    disciplinas = listar_disciplinas(
        session,
        status=status,
        semestre=semestre,
    )

    st.divider()

    if not disciplinas:

        st.info(
            "Nenhuma disciplina encontrada."
        )

    else:

        st.write(
            f"**{len(disciplinas)} disciplina(s) encontrada(s).**"
        )

        # ========================================================== #
        # LOOP DAS DISCIPLINAS
        # ========================================================== #

        for disciplina in disciplinas:

            # ------------------------------------------------------ #
            # Buscar arquivos da disciplina
            # ------------------------------------------------------ #

            arquivos = listar_arquivos(
                session,
                disciplina.id,
            )

            # ====================================================== #
            # CONTAINER DA DISCIPLINA
            # ====================================================== #

            with st.container(border=True):

                col_info, col_status, col_acoes = st.columns(
                    [4, 2, 2]
                )

                # ================================================== #
                # INFORMAÇÕES
                # ================================================== #

                with col_info:

                    st.subheader(
                        f"📚 {disciplina.nome}"
                    )

                    st.write(
                        f"**Código:** {disciplina.codigo}"
                    )

                    if disciplina.semestre:

                        st.write(
                            f"**Semestre:** "
                            f"{disciplina.semestre}"
                        )

                # ================================================== #
                # STATUS
                # ================================================== #

                with col_status:

                    if (
                        disciplina.status
                        == Disciplina.STATUS_ATIVA
                    ):

                        st.success("🟢 Ativa")

                    elif (
                        disciplina.status
                        == Disciplina.STATUS_CONCLUIDA
                    ):

                        st.info("✅ Concluída")

                    elif (
                        disciplina.status
                        == Disciplina.STATUS_TRANCADA
                    ):

                        st.error("🔴 Trancada")

                    else:

                        st.warning(
                            disciplina.status
                        )

                    st.caption(
                        f"📎 {len(arquivos)} arquivo(s)"
                    )

                # ================================================== #
                # AÇÕES DA DISCIPLINA
                # ================================================== #

                with col_acoes:

                    if st.button(
                        "👁️ Detalhes",
                        key=f"detalhes_disciplina_{disciplina.id}",
                        use_container_width=True,
                    ):

                        st.session_state[
                            "disciplina_id"
                        ] = disciplina.id

                        st.switch_page(
                            "pages/detalhes.py"
                        )

            # ====================================================== #
            # ARQUIVOS
            # ====================================================== #

            if arquivos:

                with st.expander(
                    f"📎 Arquivos de {disciplina.nome}"
                ):

                    for arquivo in arquivos:

                        arquivo_id = arquivo.id

                        chave_edicao = (
                            f"editando_arquivo_{arquivo_id}"
                        )

                        # -------------------------------------------------- #
                        # Inicializar estado de edição
                        # -------------------------------------------------- #

                        if chave_edicao not in st.session_state:

                            st.session_state[
                                chave_edicao
                            ] = False

                        # ================================================== #
                        # NOME DO ARQUIVO
                        # ================================================== #

                        st.markdown(
                            f"### 📄 {arquivo.nome}"
                        )

                        # ================================================== #
                        # MODO VISUALIZAÇÃO
                        # ================================================== #

                        if not st.session_state[
                            chave_edicao
                        ]:

                            st.caption(
                                arquivo.link
                            )

                            col_abrir, col_editar, col_excluir = st.columns(
                                3
                            )

                            # ---------------------------------------------- #
                            # ABRIR
                            # ---------------------------------------------- #

                            with col_abrir:

                                st.link_button(
                                    "🔗 Abrir arquivo",
                                    arquivo.link,
                                    use_container_width=True,
                                )

                            # ---------------------------------------------- #
                            # EDITAR
                            # ---------------------------------------------- #

                            with col_editar:

                                if st.button(
                                    "✏️ Editar",
                                    key=f"editar_arquivo_{arquivo_id}",
                                    use_container_width=True,
                                ):

                                    st.session_state[
                                        chave_edicao
                                    ] = True

                                    st.rerun()

                            # ---------------------------------------------- #
                            # EXCLUIR
                            # ---------------------------------------------- #

                            with col_excluir:

                                if st.button(
                                    "🗑️ Excluir",
                                    key=f"excluir_arquivo_{arquivo_id}",
                                    use_container_width=True,
                                ):

                                    try:

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

                        # ================================================== #
                        # MODO EDIÇÃO
                        # ================================================== #

                        else:

                            st.markdown(
                                "#### ✏️ Editar arquivo"
                            )

                            with st.form(
                                key=f"form_editar_arquivo_{arquivo_id}"
                            ):

                                novo_nome = st.text_input(
                                    "Nome do arquivo",
                                    value=arquivo.nome,
                                )

                                novo_link = st.text_input(
                                    "🔗 Link do arquivo",
                                    value=arquivo.link,
                                )

                                col_salvar, col_cancelar = st.columns(
                                    2
                                )

                                with col_salvar:

                                    salvar = st.form_submit_button(
                                        "💾 Salvar alterações",
                                        use_container_width=True,
                                    )

                                with col_cancelar:

                                    cancelar = st.form_submit_button(
                                        "❌ Cancelar",
                                        use_container_width=True,
                                    )

                            # ---------------------------------------------- #
                            # SALVAR ALTERAÇÕES
                            # ---------------------------------------------- #

                            if salvar:

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

                                        atualizar_arquivo(
                                            session,
                                            arquivo_id,
                                            nome=novo_nome,
                                            link=novo_link,
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

                            # ---------------------------------------------- #
                            # CANCELAR
                            # ---------------------------------------------- #

                            if cancelar:

                                st.session_state[
                                    chave_edicao
                                ] = False

                                st.rerun()

                        st.divider()

            else:

                st.caption(
                    "📎 Nenhum arquivo cadastrado para esta disciplina."
                )

            # ====================================================== #
            # ADICIONAR NOVO ARQUIVO
            # ====================================================== #

            chave_adicionar = (
                f"adicionando_arquivo_{disciplina.id}"
            )

            if chave_adicionar not in st.session_state:

                st.session_state[
                    chave_adicionar
                ] = False

            # ------------------------------------------------------ #
            # BOTÃO ADICIONAR
            # ------------------------------------------------------ #

            if st.button(
                "➕ Adicionar arquivo",
                key=f"adicionar_arquivo_{disciplina.id}",
                use_container_width=True,
            ):

                st.session_state[
                    chave_adicionar
                ] = True

                st.rerun()

            # ====================================================== #
            # FORMULÁRIO NOVO ARQUIVO
            # ====================================================== #

            if st.session_state[
                chave_adicionar
            ]:

                st.markdown(
                    "#### 📎 Novo arquivo"
                )

                with st.form(
                    key=f"form_novo_arquivo_{disciplina.id}"
                ):

                    novo_nome_arquivo = st.text_input(
                        "Nome do arquivo",
                        placeholder="Ex: Apostila - Aula 01",
                    )

                    novo_link_arquivo = st.text_input(
                        "🔗 Link do arquivo",
                        placeholder="https://...",
                    )

                    col_salvar_novo, col_cancelar_novo = st.columns(
                        2
                    )

                    with col_salvar_novo:

                        salvar_novo = st.form_submit_button(
                            "💾 Salvar arquivo",
                            use_container_width=True,
                        )

                    with col_cancelar_novo:

                        cancelar_novo = st.form_submit_button(
                            "❌ Cancelar",
                            use_container_width=True,
                        )

                # ================================================== #
                # SALVAR NOVO ARQUIVO
                # ================================================== #

                if salvar_novo:

                    novo_nome_arquivo = (
                        novo_nome_arquivo.strip()
                    )

                    novo_link_arquivo = (
                        novo_link_arquivo.strip()
                    )

                    if not novo_nome_arquivo:

                        st.error(
                            "O nome do arquivo é obrigatório."
                        )

                    elif not novo_link_arquivo:

                        st.error(
                            "O link do arquivo é obrigatório."
                        )

                    else:

                        try:

                            adicionar_arquivo(
                                session,
                                disciplina_id=disciplina.id,
                                nome=novo_nome_arquivo,
                                link=novo_link_arquivo,
                            )

                            session.commit()

                            st.session_state[
                                chave_adicionar
                            ] = False

                            st.success(
                                "✅ Arquivo adicionado com sucesso!"
                            )

                            st.rerun()

                        except Exception as exc:

                            st.error(
                                f"❌ Erro ao adicionar arquivo: {exc}"
                            )

                # ================================================== #
                # CANCELAR NOVO ARQUIVO
                # ================================================== #

                if cancelar_novo:

                    st.session_state[
                        chave_adicionar
                    ] = False

                    st.rerun()
