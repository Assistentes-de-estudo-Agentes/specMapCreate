---
name: sdd-run
description: Orquestra o pipeline SDD completo (intake até export), parando em cada gate para aprovação humana. Use quando o usuário chamar /sdd-run com a descrição de um sistema, ou pedir para "fazer todo o fluxo" de especificação.
---

# /sdd-run: pipeline completo

Entrada: `$ARGUMENTS` (descrição livre do sistema ou da mudança).

## Procedimento
1. Se não existir `.sdd/`, execute `/sdd-init`. Se existir, rode `/sdd-status` e **retome da fase atual** (não recomece).
2. Execute em ordem, **uma fase por vez**:
   - greenfield: `/sdd-intake` → `/sdd-discover` → `/sdd-stack` → `/sdd-spec` → `/sdd-design` → `/sdd-plan` → `/sdd-quality` → `/sdd-export` → `/sdd-docs` (opcional)
   - evolução: `/sdd-adopt` (se não houver baseline) → `/sdd-evolve` → `/sdd-quality` (regressão) → `/sdd-export` (delta)
3. **Em cada gate:** rode `run_all.py --gate N`, resuma o resultado em poucas linhas e **peça aprovação explícita** antes de avançar. Se o usuário pedir mudanças, corrija e revalide; se voltar de fase, use `/sdd-back`.
4. **Pare obrigatoriamente** quando houver pergunta bloqueante, escolha de stack ou aprovação de ADR; essas decisões são do usuário.
5. No fim, entregue um resumo: artefatos gerados, contagens, pendências, pontos de risco e como importar o backlog.

## Regras
- Nunca pule validadores nem aprove gates pelo usuário.
- Mantenha `STATE.md` atualizado a cada fase.
- Sem implementação de código de aplicação: o produto é a especificação e o backlog.
