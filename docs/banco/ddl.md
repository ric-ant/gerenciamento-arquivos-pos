# DDL — Script de Criação

Execute o script abaixo no Oracle Autonomous Database antes de rodar a aplicação pela primeira vez.

Você pode executá-lo via:

- **Oracle Cloud Console** → SQL Worksheet
- **SQL Developer** (conectado ao ADB com a wallet)
- **SQL*Plus**: `sqlplus user/password@dbdados_high @docs/ddl.sql`

## Script completo

```sql
--8<-- "ddl.sql"
```

!!! tip "Arquivo fonte"
    O script original está em `docs/ddl.sql` na raiz do projeto.

## O que o script cria

1. **`disciplinas_seq`** — sequence que gera os IDs da tabela
2. **`DISCIPLINAS`** — tabela principal com todos os campos, constraints e defaults
3. **`trg_disciplinas_atualizacao`** — trigger que atualiza automaticamente o campo
   `data_atualizacao` a cada `UPDATE`
