# Suficiência do Discovery

Preencha durante `/sdd-discover`. É verificado por `validate_discovery.py` (gate 1): ausência de perguntas abertas **não** prova que a descoberta está completa.

Situação permitida: `considerado` | `não aplicável` | `pendente aceito`.
Em `Refs`, aponte a fonte: `intake`, `contexto.md`, `Q001`, `A002`... "Produto", "Escopo" e "Funcional" nunca são "não aplicável".

## Checklist de domínios
| Domínio | Situação | Evidência / justificativa | Refs |
|---|---|---|---|
| Produto | | | |
| Escopo | | | |
| Funcional | | | |
| Acesso | | | |
| Dados | | | |
| Integrações | | | |
| NFR | | | |
| Operação | | | |
| Restrições | | | |

## Registro de conhecimento
Tipos: Confirmado, Inferido, Suposição, Pendente, Restrição obrigatória, Preferência. Suposição referencia `Axxx`; Pendente referencia `Qxxx`.

| Item | Tipo | Fonte | Data |
|---|---|---|---|

## Lacunas aceitas
Perguntas que seguem sem resposta por decisão consciente de um usuário autorizado.

| Lacuna | Impacto | Aceito por | Justificativa | Artefatos afetados |
|---|---|---|---|---|

## Aprovação
Preenchida por `python3 harness/scripts/stamp.py --aprovar-discovery --por "Nome"`, **somente depois** de o usuário aprovar o resumo.

- **Resumo aprovado por:**
- **Aprovado em:**
- **Intake (hash):**
