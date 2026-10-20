---
name: sdd-evolve
description: Modo evolução do SDD. Transforma um pedido de mudança em um delta de especificação (adicionado/modificado/removido) com análise de impacto, tasks e regressão, preservando IDs. Use quando o usuário chamar /sdd-evolve ou disser "quero adicionar/alterar X" em um sistema já especificado.
---

# /sdd-evolve: mudança como delta

Pré-requisito: baseline confirmada (`/sdd-adopt`) ou spec principal existente. Leia `STATE.md`, `LESSONS.md`, `03-requisitos/spec.md`, `legado/*`, mudanças anteriores. Entrada: `$ARGUMENTS` ou texto do usuário.

## Passos
1. Crie `mudancas/CHG-NNN-<slug>/` copiando `mudancas/_modelo/` (NNN = próximo número). Grave o pedido **bruto** em `intake.md` (imutável).
2. **Discovery da mudança:** o que muda, atores afetados, perguntas abertas (bloqueantes param o fluxo), suposições.
3. **`delta-spec.md`:**
   - **ADICIONADO:** novas US/AC/RN/RNF com IDs **novos**, continuando a numeração da spec principal;
   - **MODIFICADO:** ID existente com ANTES / DEPOIS / motivo (o ID não muda);
   - **REMOVIDO / DEPRECADO:** ID e motivo (**IDs nunca são reutilizados**).
   Use os mesmos formatos (BDD/EARS, um campo por linha).
4. **`impacto.md`:** US, AC, diagramas, contratos, tasks e testes afetados; risco de regressão; **migração de dados**; compatibilidade retroativa; **suíte de regressão alvo**.
5. **`delta-tasks.md`:** tasks da mudança + tasks de **regressão** e de **migração/compatibilidade** quando houver. Respeite limites e formato do `tasks.md`.
6. **Stack:** valide aderência (a mudança cabe na stack atual?). Nova dependência = ADR novo.
7. Gate humano: usuário aprova delta e impacto.
8. **Merge:** só após aprovação, incorpore o delta à `spec.md`/`tasks.md`/diagramas preservando IDs, rode `run_all.py --gate 6` e `stamp.py --all`. Registre a mudança em `STATE.md`.
9. Exporte somente o delta com `/sdd-export`.

## Regras
- Nunca renumere, reutilize nem apague IDs. Remoção = `deprecado` na spec com o motivo.
- Toda mudança em AC existente gera revisão dos casos de teste que o cobrem.
