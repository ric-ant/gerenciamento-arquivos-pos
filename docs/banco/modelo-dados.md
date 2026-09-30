# Modelo de Dados

## Tabela DISCIPLINAS

Única tabela do sistema. Armazena todas as disciplinas acadêmicas gerenciadas.

| Coluna             | Tipo Oracle       | Nullable | Descrição                                        |
|--------------------|-------------------|----------|--------------------------------------------------|
| `id`               | NUMBER (PK)       | NÃO      | Identificador único — gerado por sequence        |
| `nome`             | VARCHAR2(200)     | NÃO      | Nome completo da disciplina                      |
| `codigo`           | VARCHAR2(50)      | NÃO      | Código ou sigla (único)                          |
| `descricao`        | CLOB              | SIM      | Descrição ou ementa                              |
| `semestre`         | VARCHAR2(20)      | SIM      | Semestre de referência. Ex: `2026/1`             |
| `status`           | VARCHAR2(20)      | NÃO      | `ativa` \| `concluída` \| `trancada`             |
| `link_onedrive`    | VARCHAR2(2000)    | SIM      | URL do OneDrive com os arquivos da disciplina    |
| `data_criacao`     | TIMESTAMP         | NÃO      | Preenchido automaticamente na inserção           |
| `data_atualizacao` | TIMESTAMP         | NÃO      | Atualizado automaticamente pelo trigger          |

## Constraints

- `pk_disciplinas` — chave primária em `id`
- `uq_disciplinas_codigo` — unicidade do código
- `ck_disciplinas_status` — check: `status IN ('ativa', 'concluída', 'trancada')`

## Objetos de suporte

| Objeto                        | Tipo     | Finalidade                                    |
|-------------------------------|----------|-----------------------------------------------|
| `disciplinas_seq`             | SEQUENCE | Geração do ID                                 |
| `trg_disciplinas_atualizacao` | TRIGGER  | Atualiza `data_atualizacao` a cada UPDATE     |

## Diagrama

```
┌─────────────────────────────────────────┐
│              DISCIPLINAS                │
├────────────────────┬────────────────────┤
│ id          NUMBER │ PK / NOT NULL       │
│ nome        VC(200)│ NOT NULL            │
│ codigo      VC(50) │ NOT NULL / UNIQUE   │
│ descricao   CLOB   │                     │
│ semestre    VC(20) │                     │
│ status      VC(20) │ NOT NULL / CHECK    │
│ link_onedrive VC(2000)│                  │
│ data_criacao TIMESTAMP│ NOT NULL         │
│ data_atualizacao TIMESTAMP│ NOT NULL     │
└─────────────────────────────────────────┘
```
