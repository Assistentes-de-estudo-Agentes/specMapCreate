# Caso 02 — Ciclo de dependências

## Preparação
Criar TSK001 dependente de TSK002 e TSK002 dependente de TSK001.

## Comportamento esperado
`graph_deps.py` detecta o ciclo, não publica caminho crítico como se fosse válido e retorna código diferente de zero.
