# Executar a Aplicação

## Pré-condições

- [ ] Dependências instaladas (`poetry install`)
- [ ] Arquivo `.env` configurado com credenciais do Oracle ADB
- [ ] Wallet descompactada em `wallet/`
- [ ] Tabela `DISCIPLINAS` criada no banco (ver [DDL](../banco/ddl.md))

## Comando

```bash
poetry run streamlit run app/main.py
```

A aplicação estará disponível em: [http://localhost:8501](http://localhost:8501)

## Documentação local (MkDocs)

```bash
poetry run mkdocs serve
```

Documentação disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Build estático da documentação

```bash
poetry run mkdocs build
```

Os arquivos estáticos são gerados em `site/` (não versionado).

## Outros comandos úteis

```bash
# Verificar ambiente virtual em uso
poetry env info

# Listar dependências instaladas
poetry show

# Linting com ruff
poetry run ruff check app/

# Testes
poetry run pytest
```
