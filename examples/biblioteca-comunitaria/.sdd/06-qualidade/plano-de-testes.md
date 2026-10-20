---
id: plano-de-testes
gerado_em: 2026-10-20
derivado_de:
  03-requisitos/spec.md: f49bc0042832
  05-planejamento/tasks.md: 988cb3eecb00
---
# Plano de testes

### CT001.1.1: Cadastro de livro válido
- **Cobre:** AC001.1
- **Nível:** integração
- **Resultado esperado:** livro listado com status "disponível"

### CT001.2.1: Código de livro duplicado
- **Cobre:** AC001.2
- **Nível:** integração
- **Resultado esperado:** recusa com mensagem "Código já cadastrado"

### CT002.1.1: Cadastro de sócio gera carteirinha única
- **Cobre:** AC002.1
- **Nível:** integração
- **Resultado esperado:** carteirinha distinta para dois cadastros consecutivos

### CT003.1.1: Empréstimo válido define vencimento em 14 dias
- **Cobre:** AC003.1
- **Nível:** integração
- **Resultado esperado:** vencimento igual à data atual mais 14 dias

### CT003.2.1: Quarto empréstimo é recusado
- **Cobre:** AC003.2
- **Nível:** integração
- **Resultado esperado:** recusa informando o limite de 3

### CT003.3.1: Livro já emprestado é recusado
- **Cobre:** AC003.3
- **Nível:** integração
- **Resultado esperado:** recusa informando a data prevista de devolução

### CT004.1.1: Devolução com 4 dias de atraso
- **Cobre:** AC004.1
- **Nível:** unitário
- **Resultado esperado:** multa de R$ 2,00 e livro disponível

### CT004.2.1: Devolução no prazo
- **Cobre:** AC004.2
- **Nível:** unitário
- **Resultado esperado:** sem multa

### CT005.1.1: Consulta do sócio lista vencimentos
- **Cobre:** AC005.1
- **Nível:** E2E
- **Resultado esperado:** lista com título e vencimento de cada empréstimo ativo
