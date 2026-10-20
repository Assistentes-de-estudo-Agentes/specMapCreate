# Entrevista adaptativa e suficiência da descoberta

## Princípio
Não transforme o intake diretamente em backlog. Conduza uma entrevista orientada a risco. Cada pergunta deve reduzir uma incerteza que possa mudar escopo, regra de negócio, arquitetura, dados, segurança, custo ou aceitação.

## Registro obrigatório de conhecimento
Classifique cada afirmação relevante como:
- **Confirmado:** declarado ou aprovado explicitamente pelo usuário.
- **Inferido:** dedução plausível, ainda não confirmada.
- **Suposição:** decisão provisória com confiança, impacto se falsa e método de validação.
- **Pendente:** pergunta que precisa de resposta.
- **Restrição obrigatória:** não pode ser violada (ex.: stack mandatória, orçamento máximo, jurisdição).
- **Preferência:** orienta a escolha, mas pode ser negociada.

Nunca converta uma inferência em fato confirmado. Registre a fonte (trecho do intake, resposta Qxxx, requisito ou ADR) e a data quando disponível.

## Ordem de prioridade das perguntas
1. Objetivo do negócio e resultado mensurável.
2. Atores, permissões e limites de confiança.
3. Jornada principal e critérios de sucesso.
4. Regras de negócio, exceções e estados terminais.
5. Dados sensíveis, privacidade, retenção e obrigações legais aplicáveis.
6. Integrações, sistemas de origem, falhas e propriedade dos dados.
7. Volume, latência, disponibilidade, recuperação e crescimento esperado.
8. Restrições de equipe, prazo, orçamento, ambiente e stack.
9. UX, acessibilidade, relatórios, auditoria e requisitos secundários.

A ordem é adaptativa: riscos críticos de segurança, conformidade ou impacto financeiro sobem para o topo.

## Como perguntar
- Faça uma pergunta por vez se a resposta alterar as próximas perguntas; agrupe apenas decisões independentes.
- Explique em uma frase por que a resposta importa quando isso não for óbvio.
- Ofereça 2–4 opções com consequências e permita “outro”, “não sei” ou “decidir depois”.
- Se “não sei”, proponha uma opção provisória, mostre o impacto e marque como pendente/suposição; não trate como aprovado.
- Se houver contradição, cite as duas afirmações e peça que o usuário escolha ou esclareça.
- Não repita perguntas já respondidas. Antes de perguntar, consulte intake, respostas, glossário, decisões e requisitos existentes.
- Não faça perguntas cosméticas enquanto houver incerteza bloqueante.
- Evite perguntas que não alterem nenhum artefato ou decisão.

## Matriz de impacto
Para cada lacuna, estime impacto em Escopo, Negócio, Arquitetura, Dados, Segurança/Compliance, Custo/Prazo e Testabilidade, de 0 (nenhum) a 3 (alto). Registre a justificativa; não some a pontuação como se fosse uma probabilidade objetiva.

- **Bloqueante:** pode alterar o escopo principal, regra central, modelo de autorização/dados, requisito regulatório ou decisão arquitetural irreversível. Não liberar gate relacionado.
- **Importante:** altera critérios, tarefas, custos ou qualidade, mas permite continuar em artefatos provisórios claramente marcados.
- **Cosmético:** não muda comportamento ou arquitetura; pode ficar para refinamento.

## Critérios de suficiência por domínio
Antes de fechar discovery, confirme ou registre explicitamente como pendente:
- Produto: problema, usuários, objetivo e indicador de sucesso.
- Escopo: MVP, fora de escopo e limites do sistema.
- Funcional: jornadas principais, exceções e resultados observáveis.
- Acesso: atores, permissões e ações proibidas.
- Dados: entidades principais, origem, sensibilidade, retenção/exclusão e integridade.
- Integrações: proprietário, contrato conhecido/desconhecido, autenticação e comportamento em falha.
- NFR: metas mensuráveis ou decisão explícita de que serão definidas depois; evitar inventar números.
- Operação: ambientes, observabilidade, backup/recuperação e implantação quando aplicável.
- Restrições: equipe, prazo, orçamento e tecnologias obrigatórias versus preferidas.

## Registro verificável
A suficiência é registrada em `01-discovery/suficiencia.md` (checklist dos 9 domínios com evidência e refs, registro de conhecimento tipado, lacunas aceitas com responsável, aprovação). O gate `run_all.py --gate 1` valida essa estrutura e vincula a aprovação ao hash do intake: se o intake mudar, é preciso reaprovar. O script confere a **forma** e as referências, não a qualidade das respostas.

## Regra de saída
Discovery pode terminar quando:
1. todos os domínios aplicáveis foram considerados;
2. perguntas bloqueantes foram respondidas ou explicitamente aceitas como risco por um usuário autorizado;
3. suposições importantes têm impacto e validação definidos;
4. tamanho do projeto foi justificado e confirmado;
5. o usuário aprovou o resumo de contexto.

Não use “não há perguntas abertas” como único sinal de suficiência. A ausência de perguntas pode indicar descoberta incompleta. Produza um resumo para aprovação e uma lista de lacunas aceitas.

## Mudança posterior
Quando uma resposta/decisão muda, identifique os artefatos dependentes e marque-os como obsoletos. Não reescreva decisões aprovadas silenciosamente. Peça confirmação antes de propagar mudanças de escopo ou arquitetura.
