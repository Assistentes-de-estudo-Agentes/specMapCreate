---
name: sdd-quality
description: Fase 6 do SDD. Gera o plano de testes (casos especificados por AC), a matriz de rastreabilidade e a revisão independente da especificação. Use quando o usuário chamar /sdd-quality ou pedir auditoria, plano de testes ou rastreabilidade.
---

# /sdd-quality: qualidade e auditoria

Leia antes: `STATE.md`, `LESSONS.md`, tudo em `03-`, `04-`, `05-`. Estratégia em `references/plano-testes.md`.

## Passos
1. **Plano de testes** em `06-qualidade/plano-de-testes.md`: **no mínimo um caso por AC**, formato `### CT001.1.1: título` com `Cobre: AC001.1`, nível, pré-condições, passos, resultado esperado, dados. Derive casos negativos dos ACs EARS "Se...então" e casos de borda dos limites. Nada é executado aqui: são casos **especificados** para o time automatizar.
2. Atualize o campo `Casos de teste` das tasks (IDs CT) para fechar o vínculo task ↔ teste.
3. **Rastreabilidade:** `python3 harness/scripts/validate_traceability.py --write` (gera `rastreabilidade.md`). Corrija ACs sem task/teste, tasks órfãs e US sem task.
4. **Revisão independente** (autor ≠ verificador): invoque o subagente **spec-reviewer** (contexto limpo, somente leitura). Ele produz o relatório em memória; **você** grava em `06-qualidade/relatorio-revisao.md` e corrige o que for apontado. Se ele apontar problema de ambiguidade, rode também **ambiguity-adversary**.
5. Para projeto **grande**, inclua roteiro de **UAT** por épico (responsável, passos, critério de aceite do negócio).
6. Registre lições com `lessons.py` para cada padrão recorrente de falha.
7. Execute `python3 harness/scripts/run_all.py --gate 6`; depois `stamp.py 06-qualidade/plano-de-testes.md`. Revise também cenários aplicáveis de `evals/validators/` para garantir que o harness detecta referências quebradas e casos incompletos. Os validadores verificam consistência estrutural, não provam a correção semântica dos requisitos.

## Gate (fase 6 → 7)
Sem erros nos validadores, sem achados **críticos** no relatório do revisor, aprovação do usuário → `fase_atual: 7`.

## Modo evolução
Inclua a **suíte de regressão alvo**: o que existe e precisa continuar funcionando.
