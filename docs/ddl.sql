-- =============================================================
-- DDL — Tabela DISCIPLINAS
-- Oracle Autonomous Database — projeto-pessoal-bd
-- =============================================================
-- Execute este script conectado ao Oracle ADB antes de rodar
-- a aplicação pela primeira vez.
-- =============================================================

-- Sequence para geração do ID (Oracle 12c+: IDENTITY é preferido,
-- mas a sequence explícita é mais portável entre versões do ADB)
CREATE SEQUENCE disciplinas_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Tabela principal
CREATE TABLE DISCIPLINAS (
    id               NUMBER          DEFAULT disciplinas_seq.NEXTVAL
                                     CONSTRAINT pk_disciplinas PRIMARY KEY,
    nome             VARCHAR2(200)   NOT NULL,
    codigo           VARCHAR2(50)    NOT NULL
                                     CONSTRAINT uq_disciplinas_codigo UNIQUE,
    descricao        CLOB,
    semestre         VARCHAR2(20),
    status           VARCHAR2(20)    DEFAULT 'ativa' NOT NULL
                                     CONSTRAINT ck_disciplinas_status
                                         CHECK (status IN ('ativa', 'concluída', 'trancada')),
    link_onedrive    VARCHAR2(2000),
    data_criacao     TIMESTAMP       DEFAULT CURRENT_TIMESTAMP NOT NULL,
    data_atualizacao TIMESTAMP       DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Comentários nas colunas
COMMENT ON TABLE  DISCIPLINAS                    IS 'Disciplinas acadêmicas gerenciadas pelo sistema';
COMMENT ON COLUMN DISCIPLINAS.id                 IS 'Identificador único (gerado pela sequence disciplinas_seq)';
COMMENT ON COLUMN DISCIPLINAS.nome               IS 'Nome completo da disciplina';
COMMENT ON COLUMN DISCIPLINAS.codigo             IS 'Código ou sigla da disciplina (único)';
COMMENT ON COLUMN DISCIPLINAS.descricao          IS 'Descrição ou ementa da disciplina';
COMMENT ON COLUMN DISCIPLINAS.semestre           IS 'Semestre de referência, ex: 2026/1';
COMMENT ON COLUMN DISCIPLINAS.status             IS 'Status: ativa | concluída | trancada';
COMMENT ON COLUMN DISCIPLINAS.link_onedrive      IS 'URL do OneDrive com os arquivos da disciplina';
COMMENT ON COLUMN DISCIPLINAS.data_criacao       IS 'Data e hora de criação do registro';
COMMENT ON COLUMN DISCIPLINAS.data_atualizacao   IS 'Data e hora da última atualização';

-- Trigger para atualizar data_atualizacao automaticamente
CREATE OR REPLACE TRIGGER trg_disciplinas_atualizacao
    BEFORE UPDATE ON DISCIPLINAS
    FOR EACH ROW
BEGIN
    :NEW.data_atualizacao := CURRENT_TIMESTAMP;
END;
/

COMMIT;
