# Releases e alterações

Esta pasta registra mudanças planejadas e aplicadas no Delegation Core antes de sua consolidação no `CHANGELOG.md` e da publicação de uma versão.

## Estrutura

- `CHANGE_TEMPLATE.md`: modelo obrigatório para novas alterações.
- `changes/`: um documento por alteração, nomeado como `YYYY-MM-DD-descricao-curta.md`.

## Fluxo

1. Copiar `CHANGE_TEMPLATE.md` para `changes/YYYY-MM-DD-descricao-curta.md`.
2. Registrar contexto, escopo, riscos, implementação, testes e rollback.
3. Manter o status atualizado: `proposta`, `em andamento`, `aplicada`, `validada` ou `cancelada`.
4. Antes de uma release, revisar as alterações aplicáveis e consolidá-las no `CHANGELOG.md`.
5. Após a publicação, preencher a versão de destino e preservar o documento como histórico técnico.

## Regras

- Uma alteração por arquivo.
- Não registrar segredos, tokens, credenciais ou dados pessoais.
- Informar todos os arquivos modificados.
- Toda mudança destrutiva deve documentar backup e rollback.
- Toda correção deve possuir evidência de validação reproduzível.