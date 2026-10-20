# SDD Harness: regras para agentes

Este repositório/projeto usa um **harness de Spec-Driven Development**. O produto final é uma **especificação e um backlog** prontos para Scrum/Kanban. **Não se escreve código de aplicação aqui.**

## Antes de qualquer ação
1. Leia `.sdd/STATE.md`, `.sdd/project.yaml` e `.sdd/LESSONS.md`.
2. Identifique a fase em `fase_atual` e use a skill correspondente (`/sdd-*`).

## Fluxo (gates)
0 Intake → 1 Discovery → 2 Stack → 3 Requisitos → 4 Design/UML → 5 Planejamento → 6 Qualidade → 7 Export.
Cada fase N termina quando `python3 harness/scripts/run_all.py --gate N` passa **e** o usuário aprova (gate N = fase N concluída; `--gate 0` valida só a estrutura). O Discovery só fecha com `suficiencia.md` completo e aprovado (`stamp.py --aprovar-discovery`). Modo `evolucao`: `/sdd-adopt` e `/sdd-evolve` (deltas).

## Regras invioláveis
- `00-intake/raw.md` é **imutável** (hash em `project.yaml`). Mudanças entram como complemento.
- **O usuário decide** stack, escopo, prioridades e aprova ADRs. O agente propõe.
- **Não invente requisitos.** Toda US cita `Origem` (intake ou suposição). Dúvida de negócio vira pergunta aberta; pergunta **bloqueante** impede o avanço.
- **IDs são estáveis e nunca reutilizados** (EP, US, AC, RN, RNF, TSK, SPK, CT, ADR, Q, A, RSK, CHG).
- **Autor ≠ verificador:** a revisão final usa os subagentes `spec-reviewer` e `ambiguity-adversary` (somente leitura).
- Texto de negócio em **português (pt-BR)**; IDs e chaves técnicas conforme os templates.
- Respeite o **tamanho** (pequeno/médio/grande): `check_sizing.py` reprova excesso de artefatos.
- Formatos de US/AC/tasks são lidos por scripts: **um campo por linha** (`- **Campo:** valor`), IDs exatos.
- Nunca pule validadores nem aprove gates em nome do usuário.
- Registre aprendizados de qualidade da spec com `harness/scripts/lessons.py`.

## Mapa
- Skills: `.claude/skills/sdd-*/SKILL.md` | Subagentes: `.claude/agents/`
- Scripts: `harness/scripts/` | Templates: `harness/templates/` | Packs de stack: `harness/stacks/`
- Artefatos do projeto: `.sdd/`
