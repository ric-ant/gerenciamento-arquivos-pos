"""
Ponto de entrada da aplicação Streamlit.

Execute com:
    poetry run streamlit run app/main.py

Estrutura multipage:
    main.py          ← Página inicial / dashboard
    pages/cadastro.py
    pages/listagem.py
    pages/detalhes.py
"""




import streamlit as st

from app.database import verificar_conexao
from app.database import get_session
from app.repository import listar_disciplinas
from app.models import Disciplina


import streamlit as st

from app.database import (
    criar_tabelas,
    get_session,
    verificar_conexao,
)
from app.repository import listar_disciplinas
from app.models import Disciplina


criar_tabelas()


st.set_page_config(
    page_title="Gerenciador de Disciplinas",
    page_icon="🎓",
    layout="wide",
)




# ------------------------------------------------------------------ #
# Configuração global da página                                        #
# ------------------------------------------------------------------ #
st.set_page_config(
    page_title="Gerenciador de Disciplinas",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------ #
# Sidebar — navegação                                                  #
# ------------------------------------------------------------------ #
with st.sidebar:
    st.title("🎓 Disciplinas")
    st.markdown("---")
    st.page_link("main.py", label="🏠 Início", icon=None)
    st.page_link("pages/cadastro.py", label="➕ Nova Disciplina", icon=None)
    st.page_link("pages/listagem.py", label="📋 Listar Disciplinas", icon=None)
    st.markdown("---")
    st.caption("Oracle Autonomous Database · Vinhedo (OCI)")

# ------------------------------------------------------------------ #
# Corpo principal — Dashboard                                          #
# ------------------------------------------------------------------ #
st.title("🎓 Gerenciador de Disciplinas")
st.markdown("Bem-vindo ao seu sistema pessoal de gerenciamento de disciplinas.")

# Status da conexão
st.markdown("### 🔌 Status da Conexão")
with st.spinner("Verificando conexão com o Oracle ADB..."):
    conectado = verificar_conexao()

if conectado:
    st.success("✅ Conectado ao Oracle Autonomous Database")
else:
    st.error(
        "❌ Não foi possível conectar ao Oracle Autonomous Database. "
        "Verifique o arquivo `.env` e a wallet em `wallet/`."
    )
    st.stop()

st.divider()

# ------------------------------------------------------------------ #
# Métricas resumidas                                                   #
# ------------------------------------------------------------------ #
st.markdown("### 📊 Resumo")

try:
    with next(get_session()) as session:
        todas = listar_disciplinas(session)
        total = len(todas)
        ativas = sum(1 for d in todas if d.status == Disciplina.STATUS_ATIVA)
        concluidas = sum(1 for d in todas if d.status == Disciplina.STATUS_CONCLUIDA)
        trancadas = sum(1 for d in todas if d.status == Disciplina.STATUS_TRANCADA)
except Exception as exc:
    st.error(f"Erro ao carregar métricas: {exc}")
    total = ativas = concluidas = trancadas = 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Disciplinas", total)
col2.metric("🟢 Ativas", ativas)
col3.metric("✅ Concluídas", concluidas)
col4.metric("🔴 Trancadas", trancadas)

st.divider()

# ------------------------------------------------------------------ #
# Ações rápidas                                                        #
# ------------------------------------------------------------------ #
st.markdown("### ⚡ Ações Rápidas")
col_a, col_b = st.columns(2)

with col_a:
    if st.button("➕ Cadastrar Nova Disciplina", use_container_width=True):
        st.switch_page("pages/cadastro.py")

with col_b:
    if st.button("📋 Ver Todas as Disciplinas", use_container_width=True):
        st.switch_page("pages/listagem.py")
