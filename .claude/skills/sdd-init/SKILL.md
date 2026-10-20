---
name: sdd-init
description: Inicializa um projeto SDD (cria a pasta .sdd/ e o project.yaml). Use quando o usuário pedir /sdd-init, "iniciar projeto SDD" ou "criar a estrutura de especificação".
---

# /sdd-init: iniciar projeto

Cria a estrutura `.sdd/` e registra a configuração do projeto. Não gera requisitos.

## Passos
1. Se `.sdd/` já existir, mostre `python3 harness/scripts/status.py` e pergunte se é para continuar o existente. **Nunca sobrescreva** sem confirmação explícita.
2. Colete, no máximo em uma rodada de perguntas curtas (use ferramenta de múltipla escolha quando disponível):
   - **Nome** do projeto.
   - **Modo:** `greenfield` (sistema novo) ou `evolucao` (sistema existente).
   - **Metodologia:** `scrum` (sprints e pontos) ou `kanban` (fluxo, WIP, dias).
   - **Perfil da equipe:** nº de pessoas, senioridade (junior/pleno/senior/misto), stacks que o time domina, velocidade ou throughput conhecido (se houver).
3. Execute:
   `python3 harness/scripts/init_project.py --nome "<nome>" --modo <modo> --metodologia <metodologia> --equipe-tamanho <n>`
4. Preencha `equipe:` em `.sdd/project.yaml` com o que o usuário informou (stacks_dominadas, senioridade, velocidade). Para kanban, ajuste `limites.max_tarefa` para `2` (dias).
5. Se `modo: evolucao`, avise que o próximo passo é `/sdd-adopt` (antes do intake da mudança).
6. Atualize `.sdd/STATE.md` (situação atual e próxima ação). Rode `python3 harness/scripts/run_all.py --gate 0`.

## Próximo passo
- greenfield: `/sdd-intake`
- evolucao: `/sdd-adopt`
