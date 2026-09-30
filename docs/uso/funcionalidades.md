# Funcionalidades

## Página Inicial (Dashboard)

Exibida ao abrir a aplicação (`app/main.py`).

- Verifica e exibe o status da conexão com o Oracle ADB
- Mostra métricas resumidas: total de disciplinas, ativas, concluídas e trancadas
- Botões de ação rápida para cadastro e listagem

## Cadastro de Nova Disciplina

Caminho: menu lateral → **➕ Nova Disciplina**

- Formulário com os campos: nome, código, semestre, status, link OneDrive e descrição
- Campos obrigatórios: **nome** e **código**
- O código é normalizado para maiúsculas automaticamente
- Verifica duplicidade de código antes de salvar
- Feedback de sucesso ou erro após submissão

## Listagem de Disciplinas

Caminho: menu lateral → **📋 Listar Disciplinas**

- Exibe todas as disciplinas em cards individuais
- Filtros por **status** e **semestre**
- Cada card exibe: nome, código, semestre, status e link OneDrive (se cadastrado)
- Ações disponíveis por disciplina:
    - **✏️ Editar** — abre formulário inline para edição
    - **🗑️ Excluir** — pede confirmação e remove permanentemente
    - **🔍 Detalhes** — navega para a página de detalhes

## Edição de Disciplina

Disponível diretamente na listagem (formulário inline).

- Todos os campos são editáveis
- O campo `data_atualizacao` é atualizado automaticamente pelo trigger do banco
- Validação dos campos obrigatórios antes de salvar

## Exclusão de Disciplina

- **Exclusão física** (DELETE permanente no banco)
- Requer confirmação explícita antes de executar
- A listagem é atualizada automaticamente após a exclusão

## Detalhes da Disciplina

Caminho: botão **🔍 Detalhes** na listagem

- Exibe todos os campos da disciplina
- Link do OneDrive renderizado como botão clicável
- Datas de criação e atualização formatadas
- Botão para voltar à listagem
