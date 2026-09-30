# plan.md — Plano de Desenvolvimento: Gerenciador de Disciplinas

> **Referência obrigatória:** Todas as decisões de ambiente, dependências e documentação devem seguir o [`SKILL.md`](./SKILL.md) deste projeto.

---

## 1. Visão Geral do Projeto

Sistema web pessoal para **gerenciamento de disciplinas**, com interface para cadastro, edição e visualização de disciplinas, incluindo links para arquivos pessoais no OneDrive.

O banco de dados é um **Oracle Autonomous Database** já provisionado na OCI, acessado via **wallet mTLS** (`wallet_dbdados.zip`).

---

## 2. Decisões de Arquitetura

### 2.1 Stack principal

| Camada          | Tecnologia                  | Justificativa                                                        |
|-----------------|-----------------------------|----------------------------------------------------------------------|
| Frontend / UI   | **Streamlit**               | App web Python puro, sem necessidade de JS/HTML, ideal para uso pessoal |
| Backend / lógica| **Python** (direto no Streamlit) | Projeto pessoal simples, sem necessidade de API separada             |
| ORM / DB Access | **SQLAlchemy** + **python-oracledb** | SQLAlchemy abstrai o SQL; python-oracledb é o driver oficial Oracle  |
| Banco de dados  | **Oracle Autonomous Database** (OCI) | Já provisionado; conexão via wallet mTLS                             |
| Documentação    | **MkDocs Material**         | Conforme SKILL.md                                                    |
| Ambiente Python | **pyenv** + **Poetry**      | Conforme SKILL.md                                                    |

### 2.2 Conexão com o Oracle Autonomous Database

- O arquivo `wallet_dbdados.zip` já está no repositório.
- A conexão usará o driver **`python-oracledb`** em **Thin mode** (sem necessidade de Oracle Instant Client instalado localmente).
- As credenciais de acesso (usuário, senha, DSN) serão armazenadas em variáveis de ambiente via arquivo **`.env`** (nunca commitado).
- O `.env` será carregado pela lib **`python-dotenv`**.
- A wallet será descompactada em um diretório local (ex: `wallet/`) e referenciada pela configuração de conexão.

---

## 3. Estrutura de Diretórios

```
projeto-pessoal-bd/
├── .python-version          ← versão do Python (pyenv)
├── pyproject.toml           ← dependências (Poetry)
├── poetry.lock
├── .env                     ← credenciais DB (NÃO versionar)
├── .env.example             ← template do .env (versionar)
├── .gitignore
├── mkdocs.yml               ← configuração MkDocs Material
│
├── wallet/                  ← wallet descompactada (NÃO versionar)
│   ├── cwallet.sso
│   ├── tnsnames.ora
│   ├── sqlnet.ora
│   └── ...
├── wallet_dbdados.zip       ← wallet original (pode versionar se não contiver segredos)
│
├── app/                     ← código-fonte da aplicação
│   ├── __init__.py
│   ├── main.py              ← ponto de entrada Streamlit
│   ├── database.py          ← configuração da conexão Oracle / SQLAlchemy
│   ├── models.py            ← modelos SQLAlchemy (tabelas)
│   ├── repository.py        ← funções de acesso a dados (CRUD)
│   └── pages/               ← páginas do Streamlit (multipage)
│       ├── cadastro.py      ← cadastro de nova disciplina
│       ├── listagem.py      ← listagem e edição de disciplinas
│       └── detalhes.py      ← detalhes + links OneDrive de uma disciplina
│
├── docs/                    ← documentação MkDocs
│   └── index.md
│
└── site/                    ← build MkDocs (NÃO versionar)
```

---

## 4. Modelo de Dados

### Tabela: `DISCIPLINAS`

| Coluna             | Tipo            | Descrição                                      |
|--------------------|-----------------|------------------------------------------------|
| `id`               | NUMBER (PK)     | Identificador único (sequence + trigger)       |
| `nome`             | VARCHAR2(200)   | Nome da disciplina                             |
| `codigo`           | VARCHAR2(50)    | Código/sigla da disciplina                     |
| `descricao`        | CLOB            | Descrição ou ementa                            |
| `semestre`         | VARCHAR2(20)    | Ex: "2026/1"                                   |
| `status`           | VARCHAR2(20)    | Ex: "ativa", "concluída", "trancada"           |
| `link_onedrive`    | VARCHAR2(2000)  | URL do OneDrive com os arquivos da disciplina  |
| `data_criacao`     | TIMESTAMP       | Data de criação do registro                    |
| `data_atualizacao` | TIMESTAMP       | Data da última atualização                     |

> O script DDL de criação da tabela será armazenado em `docs/` e referenciado na documentação.

---

## 5. Funcionalidades da Aplicação

### 5.1 Cadastro de nova disciplina
- Formulário com todos os campos do modelo.
- Campo `link_onedrive` aceita URL colada pelo usuário.
- Validação básica: `nome` e `codigo` obrigatórios.
- Feedback de sucesso ou erro após salvar.

### 5.2 Listagem de disciplinas
- Tabela com todas as disciplinas cadastradas.
- Filtro por `status` e `semestre`.
- Botão de ação por linha: **Editar** | **Excluir** | **Ver detalhes**.

### 5.3 Edição de disciplina
- Formulário pré-preenchido com os dados atuais.
- Atualiza `data_atualizacao` automaticamente.

### 5.4 Detalhes da disciplina
- Exibe todos os campos.
- Link clicável para o OneDrive.

### 5.5 Exclusão de disciplina
- Confirmação antes de excluir.
- **Exclusão física** — o registro é removido permanentemente do banco (`DELETE`).

---

## 6. Dependências Python

### Produção

```bash
poetry add streamlit
poetry add sqlalchemy
poetry add python-oracledb
poetry add python-dotenv
```

### Desenvolvimento

```bash
poetry add --group dev mkdocs-material
poetry add --group dev pytest
poetry add --group dev ruff
```

> Antes de executar, verifique se o `pyproject.toml` já existe. Se não existir, execute `poetry init` primeiro (ver SKILL.md seção 4.2).

---

## 7. Configuração do Ambiente

### 7.1 Setup inicial (do zero)

```bash
# 1. Definir versão do Python (3.14.5 — última estável em setembro/2026)
pyenv install 3.14.5       # instalar se ainda não disponível localmente
pyenv local 3.14.5         # cria o arquivo .python-version na raiz do projeto

# 2. Inicializar Poetry
poetry init                # apenas se pyproject.toml não existir

# 3. Instalar dependências
poetry install

# 4. Descompactar a wallet
# Descompactar wallet_dbdados.zip para o diretório wallet/
# (fazer manualmente ou via script)

# 5. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com as credenciais reais do Oracle ADB
```

### 7.2 Template do arquivo `.env`

```env
# Oracle Autonomous Database
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=nome_do_servico_no_tnsnames   # ex: dbdados_high
ORACLE_WALLET_DIR=./wallet
```

### 7.3 Executar a aplicação

```bash
poetry run streamlit run app/main.py
```

---

## 8. Configuração da Conexão Oracle

O arquivo `app/database.py` deverá:

1. Carregar as variáveis do `.env` via `python-dotenv`.
2. Conectar ao Oracle ADB em **Thin mode** usando `python-oracledb`, apontando para a wallet descompactada.
3. Criar o engine do SQLAlchemy com o dialect Oracle.

Referência oficial: [Connect Python Applications with a Wallet (mTLS)](https://docs.oracle.com/iaas/autonomous-database-serverless/doc/connecting-python-mtls.html)

---

## 9. Configuração do .gitignore

O `.gitignore` deve conter ao menos:

```
# Ambiente
.env
__pycache__/
*.pyc
*.pyo
.python-version

# Oracle Wallet (contém credenciais)
wallet/

# MkDocs build
site/

# Poetry
.venv/
```

> **Atenção:** O diretório `wallet/` contém arquivos de credenciais mTLS e **nunca deve ser versionado**. Apenas o `wallet_dbdados.zip` original pode ser mantido no repositório se o projeto for privado — avalie o risco antes de commitar.

---

## 10. Documentação (MkDocs Material)

### Setup

```bash
# Instalar MkDocs Material (se não instalado)
poetry add --group dev mkdocs-material

# Inicializar (apenas se mkdocs.yml não existir)
poetry run mkdocs new .
```

### Configuração mínima do `mkdocs.yml`

```yaml
site_name: Gerenciador de Disciplinas
theme:
  name: material

nav:
  - Início: index.md
  - Modelo de Dados: modelo-dados.md
  - Como Executar: executar.md
```

### Executar localmente

```bash
poetry run mkdocs serve
```

### Build estático

```bash
poetry run mkdocs build
```

---

## 11. Tarefas de Implementação (ordem sugerida)

- [ ] **T01** — Setup do ambiente: pyenv, Poetry, `.python-version`, `pyproject.toml`
- [ ] **T02** — Criar `.gitignore` com todas as exclusões necessárias
- [ ] **T03** — Criar `.env.example` com o template de variáveis
- [ ] **T04** — Descompactar wallet e validar conexão com Oracle ADB
- [ ] **T05** — Implementar `app/database.py` (conexão SQLAlchemy + python-oracledb)
- [ ] **T06** — Criar DDL da tabela `DISCIPLINAS` no Oracle ADB
- [ ] **T07** — Implementar `app/models.py` (modelo SQLAlchemy)
- [ ] **T08** — Implementar `app/repository.py` (funções CRUD)
- [ ] **T09** — Implementar página de cadastro (`app/pages/cadastro.py`)
- [ ] **T10** — Implementar página de listagem (`app/pages/listagem.py`)
- [ ] **T11** — Implementar página de detalhes (`app/pages/detalhes.py`)
- [ ] **T12** — Implementar `app/main.py` (roteamento multipage Streamlit)
- [ ] **T13** — Configurar MkDocs Material e escrever documentação base
- [ ] **T14** — Testes básicos com pytest

---

## 12. Pontos de Atenção

- A versão do Python definida para o projeto é **3.14.5** (última estável). O agente deve executar `pyenv install 3.14.5 && pyenv local 3.14.5` para criar o `.python-version` caso ele não exista.
- O `pyproject.toml` ainda **não existe**. Executar `poetry init` antes de qualquer `poetry add`.
- A wallet `wallet_dbdados.zip` está presente no repositório, mas o diretório `wallet/` descompactado ainda não existe e deve ser criado manualmente ou via script.
- O link do OneDrive por disciplina é uma URL simples (string). Não há integração com a API do OneDrive nesta versão — o usuário cola o link manualmente.
- Todas as decisões de stack listadas neste plano seguem as restrições do `SKILL.md`. Qualquer alteração deve ser justificada explicitamente.
