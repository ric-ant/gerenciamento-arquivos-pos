# Gerenciador de Disciplinas

Sistema pessoal para gerenciamento de disciplinas acadêmicas, com interface web construída em
**Streamlit** e banco de dados **Oracle Autonomous Database** (OCI).

## Funcionalidades

- **Cadastro** de novas disciplinas com nome, código, semestre, status e link do OneDrive
- **Listagem** com filtros por status e semestre
- **Edição** inline de qualquer disciplina
- **Exclusão** permanente com confirmação
- **Detalhes** de cada disciplina com link clicável para os arquivos no OneDrive

## Stack

| Componente      | Tecnologia                        |
|-----------------|-----------------------------------|
| Interface       | Streamlit                         |
| Banco de dados  | Oracle Autonomous Database (OCI)  |
| Driver Oracle   | python-oracledb (Thin mode, mTLS) |
| ORM             | SQLAlchemy 2.x                    |
| Env Python      | pyenv + Poetry                    |
| Documentação    | MkDocs Material                   |

## Início Rápido

```bash
# 1. Instalar dependências
poetry install

# 2. Configurar credenciais
cp .env.example .env
# Edite .env com usuário, senha e DSN do Oracle ADB

# 3. Executar
poetry run streamlit run app/main.py
```

Consulte a seção [Instalação](setup/instalacao.md) para o guia completo.
