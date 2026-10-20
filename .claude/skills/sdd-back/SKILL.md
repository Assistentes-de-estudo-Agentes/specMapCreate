---
name: sdd-back
description: Volta o projeto SDD para uma fase anterior sem perder trabalho, registrando o motivo e identificando artefatos que ficarão stale. Use quando o usuário chamar /sdd-back <fase> ou disser que precisa rever escopo, stack, requisitos ou design.
---

# /sdd-back <fase>

Argumento: número da fase destino (1 Discovery, 2 Stack, 3 Requisitos, 4 Design, 5 Planejamento, 6 Qualidade). `$ARGUMENTS`.

## Passos
1. Pergunte o **motivo** se não foi dito.
2. Registre: `python3 harness/scripts/status.py --set-fase <fase> --motivo "<motivo>"` (atualiza `project.yaml` e `STATE.md`).
3. Explique o efeito: nada é apagado. Ao editar um artefato, os que dependem dele ficam **STALE** (detecção por hash em `validate_stale.py`). Mostre o mapa: spec → design → tasks → plano de testes → rastreabilidade → backlog.
4. Liste o que provavelmente precisará ser revisto (ex.: voltar a 3 afeta design, tasks, testes, rastreabilidade e export).
5. Execute a skill da fase destino. Ao concluir, regere/revalide cada artefato stale e rode `stamp.py` nele; `run_all.py --gate <fase>` precisa passar de novo.

Nunca edite `00-intake/raw.md` ao voltar; mudanças de intenção entram como complemento (ver `/sdd-intake`).
