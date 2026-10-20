#!/usr/bin/env bash
# Requer GitHub CLI autenticado: gh auth login
set -euo pipefail
gh issue create --title '[EP001] Acervo e sócios' --body '' --label 'epico,epic'
gh issue create --title '[US001] Cadastrar livro' --body 'Como bibliotecária, quero cadastrar livros no acervo para controlar quais títulos estão disponíveis.

Critérios de aceite:
- AC001.1 (BDD): Dado que a bibliotecária está autenticada Quando informa título, autor e código do livro e confirma Então o livro aparece na lista do acervo com status "disponível"
- AC001.2 (EARS): Se o código informado já existir no acervo, então o sistema deve recusar o cadastro e exibir a mensagem "Código já cadastrado".

Pai: EP001' --label 'mvp,story'
gh issue create --title '[TSK002] Modelar e migrar tabelas livro, sócio e empréstimo' --body 'criar entidades conforme er.mmd e migrações.

DoD:
- [ ] migrações aplicam e revertem sem erro
- [ ] restrições de unicidade para código do livro e carteirinha
Refs: US001, US002, US003, AC001.1
Depende de: TSK001

Pai: US001' --label 'dados,task'
gh issue create --title '[TSK003] API de cadastro de livros' --body 'endpoint de criação e listagem com validação de código duplicado.

DoD:
- [ ] AC001.1 e AC001.2 atendidos
- [ ] revisão de código
Refs: US001, AC001.1, AC001.2
Depende de: TSK002

Pai: US001' --label 'backend,task'
gh issue create --title '[TSK004] Autenticação da bibliotecária' --body 'login com política de senha de 10 caracteres ou mais.

DoD:
- [ ] rotas da bibliotecária exigem sessão válida
- [ ] política de senha aplicada
Refs: RNF002, US001
Depende de: TSK001

Pai: US001' --label 'seguranca,task'
gh issue create --title '[TSK008] Telas da bibliotecária (livros, sócios, empréstimo, devolução)' --body 'interface web responsiva consumindo as APIs.

DoD:
- [ ] fluxos principais navegáveis ponta a ponta
- [ ] revisão de usabilidade com a bibliotecária
Refs: US001, US002, US003, US004
Depende de: TSK006, TSK007

Pai: US001' --label 'frontend,task'
gh issue create --title '[US002] Cadastrar sócio' --body 'Como bibliotecária, quero cadastrar sócios para registrar quem pode pegar livros emprestados.

Critérios de aceite:
- AC002.1 (BDD): Dado que a bibliotecária está autenticada Quando informa nome e telefone do sócio e confirma Então o sistema gera um número de carteirinha único e exibe o sócio como "ativo"

Pai: EP001' --label 'mvp,story'
gh issue create --title '[TSK005] API de cadastro de sócios' --body 'criação de sócio com geração de número de carteirinha único.

DoD:
- [ ] AC002.1 atendido
Refs: US002, AC002.1
Depende de: TSK002

Pai: US002' --label 'backend,task'
gh issue create --title '[EP002] Empréstimos' --body '' --label 'epico,epic'
gh issue create --title '[US003] Registrar empréstimo' --body 'Como bibliotecária, quero registrar o empréstimo de um livro a um sócio para controlar prazos e disponibilidade.

Critérios de aceite:
- AC003.1 (BDD): Dado que o livro está disponível e o sócio possui menos de 3 empréstimos ativos Quando a bibliotecária registra o empréstimo Então o livro passa a "emprestado" e a data de vencimento é a data atual mais 14 dias
- AC003.2 (EARS): Se o sócio já possuir 3 empréstimos ativos, então o sistema deve impedir o novo empréstimo e informar o limite.
- AC003.3 (EARS): Se o livro estiver com status "emprestado", então o sistema deve impedir o empréstimo e informar a data prevista de devolução.

Pai: EP002' --label 'mvp,story'
gh issue create --title '[TSK006] API de empréstimo com regras de prazo e limite' --body 'registrar empréstimo calculando vencimento e validando limite e disponibilidade.

DoD:
- [ ] AC003.1 a AC003.3 atendidos
- [ ] cenário concorrente de dois empréstimos do mesmo livro coberto
Refs: US003, AC003.1, AC003.2, AC003.3, RN001, RN002
Depende de: TSK003, TSK005

Pai: US003' --label 'backend,task'
gh issue create --title '[US004] Registrar devolução com multa' --body 'Como bibliotecária, quero registrar a devolução e calcular a multa de atraso para liberar o livro e cobrar o valor devido.

Critérios de aceite:
- AC004.1 (BDD): Dado que existe um empréstimo ativo vencido há 4 dias Quando a bibliotecária registra a devolução Então o livro volta a "disponível" e o sistema exibe multa de R$ 2,00
- AC004.2 (EARS): Quando a devolução ocorrer até a data de vencimento, o sistema deve concluir a devolução sem multa.

Pai: EP002' --label 'mvp,story'
gh issue create --title '[TSK007] API de devolução e cálculo de multa' --body 'registrar devolução, liberar livro e calcular multa por dia corrido.

DoD:
- [ ] AC004.1 e AC004.2 atendidos
Refs: US004, AC004.1, AC004.2, RN003
Depende de: TSK006

Pai: US004' --label 'backend,task'
gh issue create --title '[US005] Consultar meus empréstimos' --body 'Como sócio, quero consultar meus empréstimos e vencimentos pelo celular para devolver os livros no prazo.

Critérios de aceite:
- AC005.1 (BDD): Dado que o sócio informa seu número de carteirinha Quando abre a consulta Então vê a lista de livros emprestados com a data de vencimento de cada um

Pai: EP002' --label 'story'
gh issue create --title '[TSK009] Consulta de empréstimos do sócio (mobile)' --body 'página responsiva de consulta por número de carteirinha.

DoD:
- [ ] AC005.1 atendido
- [ ] p95 abaixo de 2 s medido em teste de carga leve
Refs: US005, AC005.1, RNF001
Depende de: TSK006

Pai: US005' --label 'frontend,task'
gh issue create --title '[TSK001] Preparar repositório, CI e deploy em PaaS' --body 'criar repositório, pipeline de CI e ambiente de homologação com PostgreSQL.

DoD:
- [ ] pipeline roda testes em todo PR
- [ ] ambiente de homologação acessível
Refs: ADR-001, RNF002' --label 'devops,fundacao,task'
