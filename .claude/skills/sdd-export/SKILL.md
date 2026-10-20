---
name: sdd-export
description: Fase 7 do SDD. Gera backlog.json canônico e exporta para Jira, Linear, Trello, GitHub Issues ou CSV genérico. Use quando o usuário chamar /sdd-export ou pedir para levar as histórias e tasks ao quadro Scrum/Kanban.
---

# /sdd-export: exportar para o quadro

## Passos
1. Garanta que o gate 6 passou: `python3 harness/scripts/run_all.py --gate 6`. Não exporte com erros.
2. Gere o canônico: `python3 harness/scripts/export/build_backlog.py`.
3. Valide: `python3 harness/scripts/run_all.py --gate 7`.
4. Pergunte o destino (jira, linear, trello, github, generic) e mostre uma prévia: `python3 harness/scripts/export/convert.py --alvo <alvo> --dry-run`.
5. Após confirmação: `python3 harness/scripts/export/convert.py --alvo <alvo>`. Saídas em `.sdd/07-export/`.
   - **github:** gera `github-issues.json` e `github-issues.sh` (requer `gh auth login`). **Nunca execute o script sem o usuário pedir.**
   - **jira/linear/trello/generic:** CSV. Avise que o mapeamento de colunas é um ponto de partida e pode exigir ajuste na importação.
6. Registre no `STATE.md` data, destino e versão do backlog. Se o quadro virar a fonte de execução, lembre: a **spec e a rastreabilidade continuam em `.sdd/`**; sincronize só status.

## Documentação
Para entregar um documento (Markdown/PDF) com requisitos, casos de uso e UML, use `/sdd-docs`.

## Evolução
Para mudanças (`CHG-NNN`), exporte somente o delta (novas US/tasks), mantendo os IDs.


## Limite de integração
Os conversores geram arquivos de importação ou scripts auxiliares. Não afirme que itens foram criados remotamente a menos que uma integração autenticada com a API da ferramenta tenha sido executada e confirmado o resultado. Informe o formato gerado, o que exige configuração manual e quais campos podem precisar de mapeamento.
