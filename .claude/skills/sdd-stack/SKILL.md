---
name: sdd-stack
description: Fase 2 do SDD. Conduz a escolha de stack camada por camada, com recomendação ranqueada e ADRs; adapta-se à stack pedida usando packs. Use quando o usuário chamar /sdd-stack ou pedir ajuda para escolher tecnologias.
---

# /sdd-stack: seleção guiada de stack

Leia antes: `STATE.md`, `LESSONS.md`, `project.yaml`, `01-discovery/contexto.md`. Camadas e critérios em `references/camadas.md`.

## Modo evolução
A stack já existe (ADRs retroativos em `legado/`). Faça **validação de aderência**: a mudança cabe na stack atual? exige nova dependência/camada? Só abra seleção completa para camadas novas.

## Passos (greenfield)
1. **Critérios.** Peça ao usuário para ordenar/pesar (0-5): `time_to_market, custo, escala, conhecimento_time, seguranca, manutenibilidade, ecossistema`. Confirme o perfil da equipe (stacks que domina). Grave em `02-stack/criterios.md`.
2. **Pack.** Veja `harness/stacks/`. Se o usuário já indicou uma stack (ex.: Django, Next.js), use o pack correspondente: `python3 harness/scripts/rank_stack.py --pack <nome>` lista as camadas. Se não houver pack, siga em **modo genérico**: faça a análise sem script, marque `confianca: baixa` no ADR e sugira criar um pack (`harness/stacks/_template`).
3. **Escolha em camadas, uma por vez**, na ordem de `references/camadas.md`. Para cada camada:
   - rode `python3 harness/scripts/rank_stack.py --pack <p> --camada <c> --pesos <...> --selecionadas <camada=opcao,...> --time-conhece <ids>`;
   - valide o pack com `python3 harness/scripts/validate_stacks.py --pack <nome>` antes de ranquear; pack inválido bloqueia a recomendação até correção;
   - delegue ao subagente **stack-analyst** a análise contextual (o que do Discovery pesa, alertas de conflito, custo operacional para o tamanho da equipe e requisitos não atendidos);
   - se a escolha depender de versões, suporte, licenciamento ou compatibilidade atual, consulte fontes oficiais e registre URL, data e fato verificado. Se não houver acesso à web, diga explicitamente que não verificou; nunca apresente dado de memória como verificação atual;
   - apresente: ★ **recomendada**, alternativas e ⚠ desaconselhadas, cada uma com justificativa ligada ao contexto. A nota ponderada é apenas sinal comparativo, não probabilidade nem prova objetiva;
   - **o usuário decide**. Aceite escolha fora do ranking, mas registre o alerta.
   - As escolhas anteriores **filtram** as próximas (compatibilidade em cascata).
4. **Um ADR por camada** em `02-stack/adr/ADR-NNN-<camada>.md` (modelo em `harness/templates/extras/adr.md`), com `Status: aceita` somente após a aprovação do usuário, `Verificado em`, fontes verificadas (URL + data + afirmação confirmada), alternativas rejeitadas e premissas/risco residual. Se nada foi consultado, escreva “não verificado” e confiança baixa.
5. Atualize `project.yaml` (`stack: {camada: opção}`) e `02-stack/analise.md` (tabela de decisões, alertas).
6. As **tasks de fundação** do pack (`tasks_fundacao`) e os **NFRs comuns** (`nfr_comuns`) serão usados em `/sdd-spec` e `/sdd-plan`: cite-os em `analise.md`.

## Gate (fase 2 → 3)
`python3 harness/scripts/run_all.py --gate 2`. Todas as camadas escolhidas têm ADR `aceita`. Ao aprovar: `fase_atual: 3`.

## Regras
- Restrições obrigatórias eliminam opções que não as atendem; preferências apenas alteram a comparação. Nunca deixe o bônus de familiaridade compensar incompatibilidade técnica.
- Após uma escolha, reavalie as camadas dependentes; se o usuário mudar uma decisão, identifique ADRs, design, tarefas e testes afetados antes de propagar a mudança.
- Nunca decida pelo usuário. Se ele disser "você escolhe", apresente a recomendação e peça confirmação.
- Sinalize exageros para o tamanho (ex.: Kubernetes ou Kafka em projeto pequeno).
- As notas dos packs são julgamento curado: diga isso ao usuário.
