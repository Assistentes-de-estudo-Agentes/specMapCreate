---
name: sdd-design
description: Fase 4 do SDD. Gera UML em Mermaid, modelo de dados, contratos de API (esboço OpenAPI), design.md e ADRs arquiteturais. Use quando o usuário chamar /sdd-design ou pedir diagramas/UML da especificação.
---

# /sdd-design: design e UML

Leia antes: `STATE.md`, `LESSONS.md`, `project.yaml`, `03-requisitos/spec.md`, `02-stack/analise.md`. Guia de diagramas em `references/uml-guia.md`.

## Passos
1. Decida o conjunto de diagramas **pelo tamanho** (limites validados por `check_sizing.py`):
   - **pequeno:** até 2 (normalmente ER + 1 sequência crítica);
   - **médio:** até 8 (casos de uso, ER/classes, sequência dos fluxos críticos, estados das entidades com ciclo de vida);
   - **grande:** conjunto completo (+ componentes/C4, implantação, atividade).
2. Escreva cada diagrama em `04-design/diagramas/<nome>.mmd` (Mermaid puro, sem cercas de código). **Primeira linha não comentada = tipo do diagrama** e **obrigatório** o cabeçalho `%% refs: US001, RN002` com os IDs da spec que ele cobre.
3. `04-design/modelo-de-dados.md`: entidades, atributos, relacionamentos, dados pessoais e retenção (cada entidade deve aparecer no ER).
4. `04-design/contratos-api.md`: endpoints, entradas/saídas, erros, autenticação, ligados às US/AC (`Refs`). Esboço OpenAPI opcional em bloco de código.
5. `04-design/design.md`: visão arquitetural, componentes, integrações, restrições, itens **proibidos** (constituição), links para ADRs e para cada diagrama.
6. Decisões arquiteturais relevantes (monólito vs. serviços, estratégia de autenticação, tratamento de concorrência etc.) viram novos **ADRs** (`ADR-NNN`, `Status: proposta` até o usuário aprovar).
7. Se uma decisão de design contradiz a spec, **não corrija a spec aqui**: sinalize e proponha `/sdd-back 3`.
8. `python3 harness/scripts/run_all.py --gate 4` e depois `stamp.py 04-design/design.md 04-design/modelo-de-dados.md`.

## Gate (fase 4 → 5)
Sem erros nos validadores; usuário aprova os diagramas → `fase_atual: 5`.

## Modo evolução
Mostre o diagrama *as-is* (de `legado/`) e o *to-be*, destacando o que muda.
