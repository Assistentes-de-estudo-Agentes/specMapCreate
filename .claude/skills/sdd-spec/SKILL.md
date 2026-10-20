---
name: sdd-spec
description: Fase 3 do SDD. Gera épicos, user stories (BDD/EARS), regras de negócio e requisitos não funcionais no formato validável. Use quando o usuário chamar /sdd-spec ou pedir para "transformar em histórias de usuário e critérios de aceite".
---

# /sdd-spec: requisitos

Leia antes: `STATE.md`, `LESSONS.md`, `project.yaml`, `01-discovery/*`, `02-stack/analise.md`, `GLOSSARIO.md`. Notação em `references/ears-bdd.md`.

## Regras de ouro
- **Rastreabilidade de origem:** toda US tem `Origem` citando trecho do intake ou uma suposição (`A001`). Sem origem = não escreva (vira pergunta aberta).
- **Nada ambíguo:** sem "rápido", "amigável", "adequado", "etc.", "e/ou". Todo RNF tem número e unidade.
- **Auto-sizing:** pequeno = poucas US e RNFs essenciais; médio = spec completa; grande = spec completa + `compliance.md` + roteiro de UAT por épico.
- **IDs estáveis**, nunca reutilizados. Formato exato abaixo, pois os validadores dependem dele.
- Use os termos do `GLOSSARIO.md` e acrescente os novos.

## Passos
1. Agrupe em **épicos** (`## EP001: ...`), depois **US** (`### US001: ...`) com os campos: Épico, Prioridade (MoSCoW: Must/Should/Could/Won't), MVP (sim/não), Origem, História (`Como **papel**, quero **ação** para **objetivo**`), Regras de negócio, NFR relacionados. **Um campo por linha** (`- **Campo:** valor`).
2. Para cada US, **critérios de aceite**: `**AC001.1 (BDD)**` com Dado que/Quando/Então; use `**AC001.2 (EARS)**` para lógica crítica, estados e casos indesejados (ver referência). Inclua casos negativos e de borda.
3. **Regras de negócio** `**RN001**: ...` e **RNFs** `**RNF001**: ...` (desempenho, segurança, disponibilidade, acessibilidade, observabilidade). Parta de `nfr_comuns` do pack de stack.
4. **Compliance:** se o Discovery apontou domínio sensível, injete RNFs/RNs e preencha `compliance.md` (LGPD: base legal, consentimento, direitos do titular, retenção; PCI-DSS; HIPAA; WCAG).
5. Atualize `GLOSSARIO.md`. Dúvidas novas vão para `perguntas-abertas.md` (não chute regra de negócio).
6. Rode `python3 harness/scripts/run_all.py --gate 3`. Corrija **erros**; **avisos** (linguagem vaga) exigem correção ou justificativa registrada em `STATE.md`.
7. Chame o subagente **ambiguity-adversary** nos ACs. ACs com duas interpretações voltam para correção. Registre padrões recorrentes com `lessons.py`.
8. Carimbe: `python3 harness/scripts/stamp.py 03-requisitos/spec.md`.
9. Apresente ao usuário um resumo (nº de épicos/US/AC, MVP, perguntas abertas, pontos delicados) para aprovação.

## Gate (fase 3 → 4)
Validadores sem erros + aprovação do usuário → `fase_atual: 4`.

## Modo evolução
Não edite a spec principal: use `/sdd-evolve`, que trabalha com deltas.
