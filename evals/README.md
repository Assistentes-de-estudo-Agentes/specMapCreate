# Avaliações do SDD Harness

Os evals medem o comportamento do harness, não apenas se os scripts terminam sem erro. Execute cada cenário com o agente configurado e registre os artefatos produzidos, decisões tomadas, perguntas feitas e defeitos encontrados.

## Rubrica (0–2 por dimensão)

- **Fidelidade:** não inventa requisitos nem transforma inferências em fatos.
- **Descoberta:** detecta as incertezas que mudam escopo, segurança, dados ou arquitetura.
- **Adaptatividade:** faz perguntas de acompanhamento relevantes, não repete respostas e resolve contradições.
- **Rastreabilidade:** cada requisito/critério importante chega a histórias, tarefas e testes.
- **Stack:** separa restrições de preferências, verifica compatibilidade e fundamenta as recomendações.
- **Testabilidade:** critérios e tarefas são observáveis, específicos e verificáveis.
- **Consistência:** artefatos não se contradizem e referências são válidas.
- **Disciplina de escopo:** não gera código da aplicação nem adiciona funcionalidades sem autorização.

0 = falha, 1 = parcial, 2 = satisfatório. Total máximo: 16. Não use a média para esconder falhas críticas: qualquer invenção de decisão de segurança, pagamento, autorização ou compliance é falha crítica, independentemente da nota total.

## Critérios mínimos para uma versão candidata

- Nenhuma falha crítica em qualquer cenário.
- Pelo menos 14/16 em cada cenário de avaliação de release.
- Todos os validadores mecânicos passam no pacote produzido.
- Revisor humano confirma que uma equipe sem acesso à conversa consegue entender e estimar o trabalho.
- Falhas, correções e regressões são registradas em `LESSONS.md` e convertidas em casos de teste quando recorrentes.

Esses limites são política inicial de qualidade, não uma alegação de que o harness já foi avaliado nesses níveis.
