---
id: spec
gerado_em: 2026-10-20
derivado_de:
  01-discovery/contexto.md: f0fd3cbb2e8d
  01-discovery/suposicoes.md: 3cb56728146c
  01-discovery/perguntas-abertas.md: 96eea4c4382a
---
# Especificação: Biblioteca Comunitária

## EP001: Acervo e sócios

## EP002: Empréstimos

## Histórias

### US001: Cadastrar livro
- **Épico:** EP001
- **Prioridade:** Must
- **MVP:** sim
- **Origem:** intake ("A bibliotecária cadastra os livros") e A001
- **História:** Como **bibliotecária**, quero **cadastrar livros no acervo** para **controlar quais títulos estão disponíveis**.
- **NFR relacionados:** RNF002

#### Critérios de aceite
**AC001.1 (BDD)**
- **Dado que** a bibliotecária está autenticada
- **Quando** informa título, autor e código do livro e confirma
- **Então** o livro aparece na lista do acervo com status "disponível"

**AC001.2 (EARS)**
- **Se** o código informado já existir no acervo, **então** o sistema **deve** recusar o cadastro e exibir a mensagem "Código já cadastrado".

### US002: Cadastrar sócio
- **Épico:** EP001
- **Prioridade:** Must
- **MVP:** sim
- **Origem:** intake ("e os sócios")
- **História:** Como **bibliotecária**, quero **cadastrar sócios** para **registrar quem pode pegar livros emprestados**.

#### Critérios de aceite
**AC002.1 (BDD)**
- **Dado que** a bibliotecária está autenticada
- **Quando** informa nome e telefone do sócio e confirma
- **Então** o sistema gera um número de carteirinha único e exibe o sócio como "ativo"

### US003: Registrar empréstimo
- **Épico:** EP002
- **Prioridade:** Must
- **MVP:** sim
- **Origem:** intake ("registra o empréstimo, com prazo de 14 dias")
- **História:** Como **bibliotecária**, quero **registrar o empréstimo de um livro a um sócio** para **controlar prazos e disponibilidade**.
- **Regras de negócio:** RN001, RN002

#### Critérios de aceite
**AC003.1 (BDD)**
- **Dado que** o livro está disponível e o sócio possui menos de 3 empréstimos ativos
- **Quando** a bibliotecária registra o empréstimo
- **Então** o livro passa a "emprestado" e a data de vencimento é a data atual mais 14 dias

**AC003.2 (EARS)**
- **Se** o sócio já possuir 3 empréstimos ativos, **então** o sistema **deve** impedir o novo empréstimo e informar o limite.

**AC003.3 (EARS)**
- **Se** o livro estiver com status "emprestado", **então** o sistema **deve** impedir o empréstimo e informar a data prevista de devolução.

### US004: Registrar devolução com multa
- **Épico:** EP002
- **Prioridade:** Must
- **MVP:** sim
- **Origem:** intake ("cobra multa de 50 centavos por dia de atraso") e Q001
- **História:** Como **bibliotecária**, quero **registrar a devolução e calcular a multa de atraso** para **liberar o livro e cobrar o valor devido**.
- **Regras de negócio:** RN003

#### Critérios de aceite
**AC004.1 (BDD)**
- **Dado que** existe um empréstimo ativo vencido há 4 dias
- **Quando** a bibliotecária registra a devolução
- **Então** o livro volta a "disponível" e o sistema exibe multa de R$ 2,00

**AC004.2 (EARS)**
- **Quando** a devolução ocorrer até a data de vencimento, o sistema **deve** concluir a devolução sem multa.

### US005: Consultar meus empréstimos
- **Épico:** EP002
- **Prioridade:** Should
- **MVP:** não
- **Origem:** intake ("consultar pelo celular o que está com ele") e A002
- **História:** Como **sócio**, quero **consultar meus empréstimos e vencimentos pelo celular** para **devolver os livros no prazo**.
- **NFR relacionados:** RNF001

#### Critérios de aceite
**AC005.1 (BDD)**
- **Dado que** o sócio informa seu número de carteirinha
- **Quando** abre a consulta
- **Então** vê a lista de livros emprestados com a data de vencimento de cada um

## Regras de negócio
**RN001**: O prazo de empréstimo é de 14 dias corridos.
**RN002**: Cada sócio pode ter no máximo 3 empréstimos ativos.
**RN003**: A multa é de R$ 0,50 por dia corrido de atraso, sem teto.

## Requisitos não funcionais
**RNF001**: A consulta do sócio deve carregar em menos de 2 segundos no p95 em conexão 4G.
**RNF002**: O acesso à área da bibliotecária exige autenticação com senha de no mínimo 10 caracteres.
