# SKILL.md — Instruções Operacionais para Agentes de IA

Este documento define as práticas obrigatórias para qualquer agente de IA ou desenvolvedor que trabalhe neste projeto. Siga estas instruções rigorosamente antes de executar qualquer comando ou modificar o ambiente.

---

## 1. Princípios Obrigatórios

Antes de qualquer ação, todo agente deve respeitar as seguintes regras:

- **Sempre** utilize `pyenv` para gerenciar a versão do Python do projeto.
- **Sempre** utilize `Poetry` para instalar e gerenciar dependências e o ambiente virtual.
- **Nunca** instale dependências Python globalmente com `pip`.
- **Nunca** crie ou utilize ambientes virtuais Python fora do gerenciado pelo Poetry.
- **Nunca** introduza outra ferramenta de gerenciamento de dependências (conda, pipenv, venv manual etc.) sem justificativa explícita e aprovação.
- **Sempre** utilize `MkDocs Material` para qualquer documentação do projeto.
- **Nunca** introduza outro framework de documentação sem justificativa explícita e aprovação.
- **Sempre** execute comandos Python dentro do ambiente virtual do Poetry (`poetry run` ou `poetry shell`).
- **Sempre** mantenha o `pyproject.toml` como a fonte oficial de dependências.
- **Sempre** verifique a configuração real do projeto antes de assumir versões ou estruturas de diretórios.
- Se uma configuração necessária estiver ausente, **identifique a ausência e proponha a criação** em vez de assumir que ela existe.

---

## 2. Verificação de Configurações Existentes

Antes de executar qualquer setup, verifique o estado atual do projeto:

```bash
# Verificar se o arquivo .python-version existe
cat .python-version

# Verificar se o pyproject.toml existe
cat pyproject.toml

# Verificar se o mkdocs.yml existe
cat mkdocs.yml

# Verificar o ambiente virtual ativo do Poetry
poetry env info
```

Se qualquer um desses arquivos estiver ausente, siga as instruções das seções correspondentes para criá-los.

---

## 3. Gerenciamento da Versão Python com pyenv

### 3.1 Verificar a versão definida para o projeto

```bash
cat .python-version
```

Se o arquivo `.python-version` não existir, o agente deve identificar a ausência e propor a versão adequada antes de prosseguir.

### 3.2 Listar versões disponíveis do Python

```bash
pyenv install --list
```

### 3.3 Instalar a versão do Python definida no projeto

```bash
# Substitua <versao> pela versão registrada em .python-version
pyenv install <versao>
```

### 3.4 Definir a versão do Python para o projeto (cria ou atualiza .python-version)

```bash
# Substitua <versao> pela versão escolhida
pyenv local <versao>
```

Este comando cria o arquivo `.python-version` na raiz do projeto. Esse arquivo deve ser versionado no repositório.

### 3.5 Verificar a versão ativa

```bash
python --version
pyenv version
```

---

## 4. Gerenciamento de Dependências com Poetry

### 4.1 Verificar se o Poetry está instalado

```bash
poetry --version
```

Se não estiver instalado, consulte a documentação oficial: https://python-poetry.org/docs/#installation

### 4.2 Inicializar o projeto com Poetry (apenas se pyproject.toml não existir)

```bash
poetry init
```

Siga o assistente interativo. O `pyproject.toml` gerado é a fonte oficial de todas as dependências.

### 4.3 Instalar todas as dependências do projeto

```bash
poetry install
```

Esse comando instala todas as dependências declaradas no `pyproject.toml` (produção e desenvolvimento) dentro do ambiente virtual gerenciado pelo Poetry.

### 4.4 Adicionar uma dependência de produção

```bash
poetry add <nome-do-pacote>
```

Exemplo:
```bash
poetry add requests
```

### 4.5 Adicionar uma dependência de desenvolvimento

```bash
poetry add --group dev <nome-do-pacote>
```

Exemplo:
```bash
poetry add --group dev pytest
```

### 4.6 Atualizar dependências

```bash
# Atualizar todas as dependências
poetry update

# Atualizar um pacote específico
poetry update <nome-do-pacote>
```

### 4.7 Executar um comando dentro do ambiente virtual do Poetry

```bash
poetry run <comando>
```

Exemplos:
```bash
poetry run python meu_script.py
poetry run pytest
poetry run python -m meu_modulo
```

### 4.8 Ativar o shell do ambiente virtual

```bash
poetry shell
```

Dentro do shell ativado, todos os comandos Python utilizam automaticamente o ambiente do Poetry. Para sair:

```bash
exit
```

### 4.9 Verificar o ambiente virtual em uso

```bash
poetry env info
```

Este comando exibe o caminho do ambiente virtual, a versão do Python e outras informações relevantes.

### 4.10 Listar dependências instaladas

```bash
poetry show
```

---

## 5. Documentação com MkDocs Material

O framework oficial de documentação deste projeto é o **MkDocs Material**. Nenhum outro framework de documentação deve ser introduzido sem aprovação explícita.

### 5.1 Instalar o MkDocs Material como dependência de desenvolvimento

```bash
poetry add --group dev mkdocs-material
```

### 5.2 Inicializar a configuração do MkDocs (apenas se mkdocs.yml não existir)

```bash
poetry run mkdocs new .
```

Esse comando cria o arquivo `mkdocs.yml` na raiz do projeto e o diretório `docs/` com um arquivo inicial `index.md`.

### 5.3 Estrutura de diretórios da documentação

```
projeto-pessoal-bd/
├── docs/               ← Todos os arquivos .md da documentação ficam aqui
│   └── index.md        ← Página inicial da documentação
├── mkdocs.yml          ← Arquivo de configuração do MkDocs (raiz do projeto)
└── pyproject.toml
```

### 5.4 Configurar o tema MkDocs Material no mkdocs.yml

O `mkdocs.yml` deve conter ao menos a seguinte configuração de tema:

```yaml
site_name: Nome do Projeto
theme:
  name: material
```

Antes de criar ou sobrescrever o `mkdocs.yml`, verifique se ele já existe e preserve as configurações existentes.

### 5.5 Executar a documentação localmente

```bash
poetry run mkdocs serve
```

A documentação ficará disponível em: http://127.0.0.1:8000

### 5.6 Gerar o build estático da documentação

```bash
poetry run mkdocs build
```

Os arquivos estáticos serão gerados no diretório `site/`. Esse diretório deve ser adicionado ao `.gitignore`.

### 5.7 Adicionar site/ ao .gitignore

O diretório `site/` gerado pelo build não deve ser versionado. Certifique-se de que o `.gitignore` contenha:

```
site/
```

---

## 6. Checklist de Configurações Ausentes

Ao iniciar o trabalho no projeto, o agente deve verificar e, se necessário, propor a criação dos seguintes itens:

| Arquivo / Configuração       | Ação se ausente                                                      |
|------------------------------|----------------------------------------------------------------------|
| `.python-version`            | Identificar versão adequada e executar `pyenv local <versao>`        |
| `pyproject.toml`             | Executar `poetry init` para inicializar o projeto                    |
| `poetry.lock`                | Executar `poetry install` para gerar o lockfile                      |
| `mkdocs.yml`                 | Executar `poetry run mkdocs new .` após instalar mkdocs-material     |
| `docs/`                      | Criado automaticamente pelo `mkdocs new .`                           |
| `mkdocs-material` em dev deps| Executar `poetry add --group dev mkdocs-material`                    |
| `.gitignore`                 | Criar e incluir ao menos `site/` e `.python-version` se necessário   |

> **Nota:** Este projeto está atualmente sem configuração inicial. Todos os itens acima precisam ser criados. Não assuma que qualquer um deles existe sem verificar primeiro.

---

## 7. Referências

- pyenv: https://github.com/pyenv/pyenv
- Poetry: https://python-poetry.org/docs/
- MkDocs Material: https://squidfunk.github.io/mkdocs-material/
