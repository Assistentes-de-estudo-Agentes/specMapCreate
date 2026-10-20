---
name: sdd-plan
description: Fase 5 do SDD. Decompõe a spec em tasks atômicas com dependências, estimativas, spikes, riscos e plano Scrum (sprints) ou Kanban (WIP, classes de serviço). Use quando o usuário chamar /sdd-plan ou pedir backlog, tasks ou plano de sprints.
---

# /sdd-plan: planejamento

Leia antes: `STATE.md`, `LESSONS.md`, `project.yaml` (metodologia, equipe, limites), `03-requisitos/spec.md`, `04-design/*`, `02-stack/analise.md`. Metodologias em `references/scrum-kanban.md`.

## Passos
1. **Tasks de fundação** a partir do pack da stack (`tasks_fundacao` em `harness/stacks/<pack>/pack.json`) e dos ADRs: repositório, CI/CD, ambientes, segredos, observabilidade, backup, hardening. Referencie ADR e/ou RNF em `Refs`.
2. **Tasks por US** em **fatias verticais** (entrega valor ponta a ponta) sempre que possível. Cada task é **atômica** e traz: `Refs` (US/AC/RN/RNF/ADR), `Tipo`, `Estimativa`, `Confiança`, `Depende de`, `Descrição`, `Definition of Done` (checklist) e `Casos de teste`. Formato exato no template `05-planejamento/tasks.md`.
3. **Limite de tamanho:** Scrum ≤ 5 pontos (Fibonacci); Kanban ≤ 2 dias. Acima disso, quebre. Estime com a equipe do `project.yaml` em mente.
4. **Spikes** (`SPK001`, Tipo `spike`) para incerteza técnica ou confiança **baixa**: timebox e a pergunta a responder.
5. **Dependências** entre tasks e dependências externas (`dependencias.md`). Rode `graph_deps.py` (ciclos e caminho crítico).
6. **Riscos** (`riscos.md`, `**RSK001**: ...`) com probabilidade, impacto, mitigação e dono.
7. **Plano da metodologia:**
   - `scrum`: `plano-scrum.md` com capacidade (velocidade × duração), Sprint 0 (fundação), meta de cada sprint, tasks e pontos; respeita o MVP primeiro.
   - `kanban`: `plano-kanban.md` com colunas e políticas, **limites de WIP** (regra de partida: ~ nº de pessoas + 1 em andamento), classes de serviço, ondas de entrega.
8. `python3 harness/scripts/run_all.py --gate 5`; depois `stamp.py 05-planejamento/tasks.md`.
9. Apresente ao usuário: nº de tasks, pontos totais, caminho crítico, MVP em quantas sprints/ondas, riscos principais.

## Gate (fase 5 → 6)
Sem erros → `fase_atual: 6`.

## Modo evolução
Escreva em `mudancas/CHG-NNN/delta-tasks.md`, incluindo tasks de **regressão** e **migração/compatibilidade**.
