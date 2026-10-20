# Guia de diagramas (Mermaid)

| Diagrama | Quando | Primeira linha |
|---|---|---|
| Casos de uso | médio+ | `flowchart LR` (atores e casos como nós; Mermaid não tem sintaxe nativa de use case) |
| Classes de domínio | regras de negócio ricas | `classDiagram` |
| ER / dados | sempre que há persistência | `erDiagram` |
| Sequência | fluxo crítico multi-serviço | `sequenceDiagram` |
| Atividade / processo | ramificações de negócio | `flowchart TD` |
| Estados | entidade com ciclo de vida | `stateDiagram-v2` |
| Componentes / C4 | grande ou vários serviços | `flowchart` ou `C4Container` |
| Implantação | infra relevante | `flowchart` |

## Convenções
- Nome do arquivo descritivo: `sequencia-emprestimo.mmd`, `estados-pedido.mmd`.
- Cabeçalho obrigatório: `%% refs: US003, RN001`.
- Nomes de atores/entidades **iguais** aos da spec e do glossário.
- Um fluxo por diagrama; legível sem rolar. Preferir poucos diagramas bons.
- Validação sintática completa exige `mmdc` (`npm i -g @mermaid-js/mermaid-cli`); sem ele, o validador faz checagem estrutural.
