# Pré-requisitos

Antes de configurar o projeto, certifique-se de ter instalado:

## pyenv

Gerenciador de versões Python. Necessário para fixar a versão `3.14.5` usada pelo projeto.

- Instalação: [github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)
- Windows: use [pyenv-win](https://github.com/pyenv-win/pyenv-win)

Verificar instalação:

```bash
pyenv --version
```

## Poetry

Gerenciador de dependências e ambiente virtual Python.

- Instalação: [python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

Verificar instalação:

```bash
poetry --version
```

## Oracle Autonomous Database

O banco de dados já deve estar provisionado na OCI e a wallet baixada.

- A wallet (`wallet_dbdados.zip`) deve estar presente na raiz do projeto
- O diretório `wallet/` (descompactado) **não deve ser versionado**

## Acesso à internet (para o Oracle ADB)

A aplicação conecta ao host `adb.sa-vinhedo-1.oraclecloud.com` na porta `1522` via protocolo TCPS.
Certifique-se de que a rede permite essa saída.
