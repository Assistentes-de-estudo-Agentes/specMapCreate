# Scrum x Kanban no harness

| Aspecto | Scrum | Kanban |
|---|---|---|
| Estimativa | pontos (1, 2, 3, 5) | dias (máx. 2) |
| Estrutura | sprints com meta | fluxo contínuo, ondas de entrega |
| Capacidade | velocidade × duração | throughput (itens/semana) |
| Limites | tasks ≤ 5 pts | WIP por coluna |
| Prioridade | ordem do backlog + MoSCoW | classes de serviço |
| Plano | `plano-scrum.md` | `plano-kanban.md` |

O backlog base (US, AC, tasks) é o mesmo; troque a metodologia em `project.yaml` e regenere só o plano.

## Dicas
- Sprint 0 / primeira onda: fundação + o menor fatiamento vertical que valide a arquitetura (walking skeleton).
- Sem velocidade conhecida: assuma valor conservador (ex.: ~3-5 pts por pessoa por sprint de 2 semanas), marque como suposição e revise após 2 sprints.
- Kanban: defina política explícita de entrada (DoR) e saída (DoD) por coluna.
- Dependência externa (aprovação, fornecedor) é risco: registre em `riscos.md`.
