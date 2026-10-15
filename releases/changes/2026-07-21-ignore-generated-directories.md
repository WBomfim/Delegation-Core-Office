# Ignorar diretórios gerados na ingestão externa

- Data: 2026-07-21
- Status: aplicada; validação MCP pendente após reconexão
- Versão de destino: próxima versão após 0.6.4
- Responsável: Codex, por solicitação do usuário

## Contexto

A ingestão recursiva de `C:\Users\willi\Projetos` percorreu `node_modules` e adicionou milhares de READMEs, licenças e changelogs de dependências ao índice semântico. Isso aumentou o tempo da operação e contaminou resultados de busca com conteúdo de terceiros.

## Decisão

Excluir da descoberta de candidatos todos os arquivos localizados dentro de diretórios gerados, vendorizados ou de controle de versão.

## Escopo

### Incluído

- `node_modules`
- `.git`
- `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache` e `.tox`
- `.venv` e `venv`
- `dist`, `build` e `coverage`
- Limpeza das entradas de `node_modules` já presentes no ChromaDB

### Fora do escopo

- Filtros configuráveis pelo usuário.
- Cancelamento de jobs em execução.
- Exclusão física de arquivos dos projetos.

## Arquivos afetados

- `src/delegation_core/ingest.py`
- Instalação ativa: `C:\Users\willi\.delegation_core\venv\Lib\site-packages\delegation_core\ingest.py`
- Índice: `C:\Users\willi\Documents\Delegation_Vault\.chroma_bge`

## Implementação

1. Adicionada a constante `_IGNORED_DIRS`.
2. Adicionada a função `_is_ignored(path, source)`.
3. Aplicado o filtro na lista de candidatos antes da extração e indexação.
4. Criados backups `.bak` dos dois arquivos alterados.
5. Removidos do índice apenas os IDs cuja metadata `path` continha o segmento exato `node_modules`.
6. Reiniciados os processos `python -m delegation_core run` para carregar o código novo.

## Riscos e compatibilidade

- Diretórios legítimos chamados `build` ou `dist` deixam de ser ingeridos; mitigação futura: tornar a lista configurável.
- A limpeza foi feita diretamente no ChromaDB; os documentos são recuperáveis por nova ingestão porque os originais não foram removidos.
- O cliente MCP da sessão não reconectou automaticamente após o reinício e requer reinício do Codex.

## Validação

- [x] Sintaxe e importação
- [x] Teste unitário direto do predicado de exclusão
- [x] Limpeza seletiva do índice
- [x] Confirmação de zero entradas de `node_modules`
- [ ] Busca funcional via MCP após reinício do Codex
- [ ] Teste de nova ingestão recursiva completa

### Evidências

```text
filter tests passed
deleted=5151
remaining=746
filter_loaded=true
indexed_total=746
node_modules_entries=0
```

## Migração ou limpeza de dados

Foram removidas 5.151 entradas de chunks/arquivos provenientes de `node_modules`. O índice permaneceu com 746 registros. Nenhum arquivo original foi alterado ou excluído.

## Rollback

1. Restaurar `ingest.py.bak` no código-fonte e na instalação ativa.
2. Reiniciar o servidor MCP.
3. Se necessário, reexecutar a ingestão externa para restaurar documentos anteriormente removidos do índice.

## Pendências

- Reiniciar o Codex e validar `heartbeat` e `search_vault`.
- Considerar configuração de exclusões em `config.json`.
- Considerar suporte a cancelamento de jobs de ingestão.
- Adicionar testes automatizados ao repositório.