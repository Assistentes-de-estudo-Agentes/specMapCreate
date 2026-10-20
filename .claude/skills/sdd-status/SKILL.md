---
name: sdd-status
description: Mostra o estado do projeto SDD (fase, tamanho, contagens, perguntas abertas, artefatos stale) e o próximo passo. Use quando o usuário chamar /sdd-status ou perguntar "em que pé estamos".
---

# /sdd-status

1. Rode `python3 harness/scripts/status.py`.
2. Rode o gate das fases **já concluídas**: `python3 harness/scripts/run_all.py --gate <fase_atual - 1>` (mínimo `--gate 0`) e resuma erros e avisos.
3. Informe de forma curta: fase atual, o que falta para o gate, perguntas bloqueantes, artefatos **stale** e o **próximo comando** recomendado.
Não modifique arquivos.
