---
id: tasks
gerado_em: 2026-10-20
derivado_de:
  03-requisitos/spec.md: f49bc0042832
  04-design/design.md: 0467c9824497
---
# Tasks

### TSK001: Preparar repositório, CI e deploy em PaaS
- **Refs:** ADR-001, RNF002
- **Tipo:** devops
- **Estimativa:** 5
- **Confiança:** média
- **Depende de:** nenhuma
- **Descrição:** criar repositório, pipeline de CI e ambiente de homologação com PostgreSQL.
- **Definition of Done:**
  - [ ] pipeline roda testes em todo PR
  - [ ] ambiente de homologação acessível

### TSK002: Modelar e migrar tabelas livro, sócio e empréstimo
- **Refs:** US001, US002, US003, AC001.1
- **Tipo:** dados
- **Estimativa:** 3
- **Confiança:** alta
- **Depende de:** TSK001
- **Descrição:** criar entidades conforme er.mmd e migrações.
- **Definition of Done:**
  - [ ] migrações aplicam e revertem sem erro
  - [ ] restrições de unicidade para código do livro e carteirinha

### TSK003: API de cadastro de livros
- **Refs:** US001, AC001.1, AC001.2
- **Tipo:** backend
- **Estimativa:** 3
- **Confiança:** alta
- **Depende de:** TSK002
- **Descrição:** endpoint de criação e listagem com validação de código duplicado.
- **Definition of Done:**
  - [ ] AC001.1 e AC001.2 atendidos
  - [ ] revisão de código
- **Casos de teste:** CT001.1.1, CT001.2.1

### TSK004: Autenticação da bibliotecária
- **Refs:** RNF002, US001
- **Tipo:** seguranca
- **Estimativa:** 3
- **Confiança:** média
- **Depende de:** TSK001
- **Descrição:** login com política de senha de 10 caracteres ou mais.
- **Definition of Done:**
  - [ ] rotas da bibliotecária exigem sessão válida
  - [ ] política de senha aplicada

### TSK005: API de cadastro de sócios
- **Refs:** US002, AC002.1
- **Tipo:** backend
- **Estimativa:** 2
- **Confiança:** alta
- **Depende de:** TSK002
- **Descrição:** criação de sócio com geração de número de carteirinha único.
- **Definition of Done:**
  - [ ] AC002.1 atendido
- **Casos de teste:** CT002.1.1

### TSK006: API de empréstimo com regras de prazo e limite
- **Refs:** US003, AC003.1, AC003.2, AC003.3, RN001, RN002
- **Tipo:** backend
- **Estimativa:** 5
- **Confiança:** média
- **Depende de:** TSK003, TSK005
- **Descrição:** registrar empréstimo calculando vencimento e validando limite e disponibilidade.
- **Definition of Done:**
  - [ ] AC003.1 a AC003.3 atendidos
  - [ ] cenário concorrente de dois empréstimos do mesmo livro coberto
- **Casos de teste:** CT003.1.1, CT003.2.1, CT003.3.1

### TSK007: API de devolução e cálculo de multa
- **Refs:** US004, AC004.1, AC004.2, RN003
- **Tipo:** backend
- **Estimativa:** 3
- **Confiança:** alta
- **Depende de:** TSK006
- **Descrição:** registrar devolução, liberar livro e calcular multa por dia corrido.
- **Definition of Done:**
  - [ ] AC004.1 e AC004.2 atendidos
- **Casos de teste:** CT004.1.1, CT004.2.1

### TSK008: Telas da bibliotecária (livros, sócios, empréstimo, devolução)
- **Refs:** US001, US002, US003, US004
- **Tipo:** frontend
- **Estimativa:** 5
- **Confiança:** média
- **Depende de:** TSK006, TSK007
- **Descrição:** interface web responsiva consumindo as APIs.
- **Definition of Done:**
  - [ ] fluxos principais navegáveis ponta a ponta
  - [ ] revisão de usabilidade com a bibliotecária

### TSK009: Consulta de empréstimos do sócio (mobile)
- **Refs:** US005, AC005.1, RNF001
- **Tipo:** frontend
- **Estimativa:** 3
- **Confiança:** média
- **Depende de:** TSK006
- **Descrição:** página responsiva de consulta por número de carteirinha.
- **Definition of Done:**
  - [ ] AC005.1 atendido
  - [ ] p95 abaixo de 2 s medido em teste de carga leve
- **Casos de teste:** CT005.1.1
