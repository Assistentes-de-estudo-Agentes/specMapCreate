# ADR-001: Banco relacional (PostgreSQL)
- **Status:** aceita
- **Data:** 2026-10-19
- **Verificado em:** 2026-10-19
- **Camada:** banco

## Contexto
Dados relacionais (livros, sócios, empréstimos) e regras transacionais (RN002).

## Decisão
PostgreSQL, que o time já domina.

## Alternativas consideradas
| Alternativa | Motivo da rejeição |
|---|---|
| MongoDB | dados fortemente relacionais |

## Consequências
- Positivas: transações e integridade referencial.
- Negativas: nenhuma relevante para a escala prevista.

## Tasks geradas
TSK001
