# Suficiência do Discovery

## Checklist de domínios
| Domínio | Situação | Evidência / justificativa | Refs |
|---|---|---|---|
| Produto | considerado | Problema: controlar empréstimos de livros da biblioteca do bairro; sucesso = nenhum empréstimo fora de controle | intake, contexto.md |
| Escopo | considerado | MVP: cadastros, empréstimo, devolução com multa, consulta do sócio; fora: reservas, pagamento online, catálogo externo | contexto.md |
| Funcional | considerado | Jornada principal e exceções (limite de 3, livro indisponível, atraso) definidas; Q002 segue aberta e não bloqueia o MVP | intake, Q002 |
| Acesso | considerado | Dois papéis: bibliotecária (autenticada) e sócio (consulta por carteirinha); ações do sócio limitadas a leitura | contexto.md, A002 |
| Dados | pendente aceito | Nome e telefone dos sócios são dados pessoais; retenção e exclusão ainda não definidas | Q003 |
| Integrações | não aplicável | Sem integrações externas no MVP: pagamento online e catálogo externo estão fora do escopo | contexto.md |
| NFR | considerado | Consulta do sócio em menos de 2 s no p95 (RNF001) e senha de 10+ caracteres (RNF002); números vieram da conversa com a bibliotecária | intake, spec.md |
| Operação | considerado | Hospedagem em PaaS gerenciado, sem equipe de operação dedicada; backup diário na fundação (TSK001) | ADR-003, TSK001 |
| Restrições | considerado | Equipe de 3 pessoas domina Python e PostgreSQL; orçamento de infraestrutura baixo | criterios.md |

## Registro de conhecimento
| Item | Tipo | Fonte | Data |
|---|---|---|---|
| Bibliotecária cadastra livros e sócios e registra empréstimo e devolução | Confirmado | intake | 2026-10-19 |
| Prazo de 14 dias, limite de 3 livros e multa de R$ 0,50 por dia | Confirmado | intake | 2026-10-19 |
| Multa sem teto no MVP | Confirmado | Q001 (resposta da bibliotecária) | 2026-10-19 |
| A001: um exemplar por título | Suposição | A001 | 2026-10-19 |
| A002: sócio se identifica pelo número da carteirinha | Suposição | A002 | 2026-10-19 |
| Equipe domina Python e PostgreSQL | Preferência | criterios.md | 2026-10-19 |
| Política de retenção dos dados pessoais dos sócios | Pendente | Q003 | 2026-10-19 |

## Lacunas aceitas
| Lacuna | Impacto | Aceito por | Justificativa | Artefatos afetados |
|---|---|---|---|---|
| Q003: retenção e exclusão de dados pessoais | importante | Bibliotecária (responsável pelo projeto) | MVP de uso interno; a política será definida antes de abrir a consulta do sócio ao público | US002, modelo de dados |

## Aprovação
- **Resumo aprovado por:** Bibliotecária (responsável pelo projeto)
- **Aprovado em:** 2026-10-20
- **Intake (hash):** 93c04fcf3a15
