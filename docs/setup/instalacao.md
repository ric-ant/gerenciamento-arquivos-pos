# Instalação

## 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd projeto-pessoal-bd
```

## 2. Definir a versão do Python

```bash
pyenv install 3.14.5
pyenv local 3.14.5
python --version   # deve exibir Python 3.14.5
```

## 3. Instalar dependências com Poetry

```bash
poetry install
```

Isso cria o ambiente virtual e instala todas as dependências de produção e desenvolvimento
declaradas no `pyproject.toml`.

## 4. Configurar a wallet Oracle

Descompacte a wallet na raiz do projeto:

```bash
# Linux/macOS
unzip wallet_dbdados.zip -d wallet/

# Windows (PowerShell)
Expand-Archive -Path wallet_dbdados.zip -DestinationPath wallet
```

!!! warning "Segurança"
    O diretório `wallet/` contém certificados mTLS e **nunca deve ser commitado**.
    Ele está listado no `.gitignore`.

## 5. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=dbdados_high
ORACLE_WALLET_DIR=./wallet
```

Serviços disponíveis para `ORACLE_DSN`:

| Serviço           | Uso indicado                      |
|-------------------|-----------------------------------|
| `dbdados_high`    | Uso geral (recomendado)           |
| `dbdados_medium`  | Prioridade média                  |
| `dbdados_low`     | Consultas longas ou batch         |
| `dbdados_tp`      | Transaction processing            |
| `dbdados_tpurgent`| Transaction processing urgente    |

## 6. Criar a tabela no banco

Execute o script DDL no Oracle ADB (via SQL*Plus, SQL Developer ou Oracle Cloud Console):

```sql
-- Conteúdo disponível em docs/ddl.sql
```

Veja o script completo em [DDL](../banco/ddl.md).

## 7. Executar a aplicação

```bash
poetry run streamlit run app/main.py
```

A aplicação estará disponível em: [http://localhost:8501](http://localhost:8501)
