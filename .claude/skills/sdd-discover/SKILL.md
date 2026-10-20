---
name: sdd-discover
description: Fase 1 do SDD (Discovery). Extrai atores, objetivos, escopo, suposições, perguntas abertas e dimensiona o projeto (pequeno/médio/grande). Use quando o usuário chamar /sdd-discover, ou /sdd-discover --sync para reimportar respostas.
---

# /sdd-discover: Discovery

Leia antes: `.sdd/STATE.md`, `.sdd/LESSONS.md`, `.sdd/project.yaml`, `.sdd/00-intake/raw.md`. Guias de perguntas em `references/perguntas-guia.md` e `references/entrevista-adaptativa.md`. Siga os critérios de suficiência e registre fontes para fatos, inferências, suposições e pendências.

## Passos
1. **Extraia do intake** (não invente; o que faltar vira pergunta):
   - atores e papéis, objetivos de negócio, métricas de sucesso;
   - escopo **dentro** e **fora**;
   - integrações externas, domínio sensível (saúde, finanças, dados pessoais, crianças, setor público);
   - termos de domínio, que vão para `GLOSSARIO.md`.
   Grave em `01-discovery/contexto.md`.
2. **Suposições** (`suposicoes.md`): palpites razoáveis sobre detalhes secundários, formato `**A001**: ...` com *Confiança*, *Se falsa, o impacto é* e *Validar com*.
3. **Perguntas abertas** (`perguntas-abertas.md`), formato `**Q001**: ...`, com `Impacto` (**bloqueante** | importante | cosmético), `Afeta`, `Responsável pela resposta`, `Status`.
   - Bloqueante = a resposta muda escopo, arquitetura, regra de negócio central ou compliance (ex.: fuso horário de prazos, regras de pagamento, persistência de sessão).
   - Não bloqueie por detalhes que uma suposição resolve.
4. **Dimensionamento** em `contexto.md`: proponha `pequeno`, `medio` ou `grande` com justificativa numérica (nº estimado de US, integrações, compliance, riscos). Heurística: pequeno ≤ ~8 US sem integrações críticas; médio ~9-25; grande > 25, múltiplos serviços ou regulatório. **O usuário confirma**; grave em `project.yaml` (`tamanho`).
5. Se detectar domínio sensível, liste as normas aplicáveis (LGPD, PCI-DSS, HIPAA, WCAG) em `contexto.md` e marque como candidato a `grande`.
6. **Entrevista adaptativa.** Priorize perguntas por risco e impacto; evite questionários genéricos. Pergunte uma por vez quando a resposta muda o próximo ramo; ofereça opções e consequências, aceite “não sei” sem converter em decisão aprovada e resolva contradições citando as fontes conflitantes. Não repita o que já está respondido.
7. **Suficiência.** Revise explicitamente produto, escopo, jornadas/exceções, permissões, dados/privacidade, integrações/falhas, NFRs, operação e restrições. Para cada domínio não aplicável, registre por que; para lacunas importantes, registre impacto e validação. Mostre um resumo consolidado para aprovação do usuário. Registre tudo em `01-discovery/suficiencia.md` (checklist dos 9 domínios com evidência e refs, registro de conhecimento tipado, lacunas aceitas com responsável) e preencha a seção `## Resumo` de `contexto.md`: é o texto que o usuário aprova.
8. **Pare e pergunte** as perguntas bloqueantes. Atualize `Status`/`Resposta` conforme ele responder. Se o usuário autorizar seguir com risco, registre quem aceitou, a justificativa e os artefatos afetados; não oculte a pendência.
9. Para stakeholders externos: ofereça gerar um documento de refinamento (`harness/templates/extras/refinamento.md` + as perguntas) ou issues no GitHub (template `refinamento.yml`).

## `--sync`
Reimporte respostas editadas no arquivo ou vindas de issues/PR, atualize `Status` e revise suposições afetadas.

## Gate (fase 1 → 2)
`python3 harness/scripts/run_all.py --gate 1` precisa passar para a fase 1 terminar. Ele exige: sem perguntas bloqueantes abertas, tamanho confirmado, `suficiencia.md` completo (9 domínios com evidência e refs, registro de conhecimento, lacunas aceitas com responsável) e a **aprovação registrada**.

**Só depois de o usuário aprovar o resumo**, registre: `python3 harness/scripts/stamp.py --aprovar-discovery --por "<quem aprovou>"` e rode o gate. Nunca aprove em nome do usuário. O gate confere forma e referências, não a qualidade das respostas: continue mostrando ao usuário a evidência de cada domínio. Se o intake mudar depois (complemento), a aprovação perde a validade e o resumo precisa ser reaprovado. Ao passar: `fase_atual: 2` e registro em `STATE.md`.

Modo `evolucao`: use também `.sdd/legado/` e o intake da mudança; o foco é o que muda.
