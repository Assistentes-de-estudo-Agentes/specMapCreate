# SDD Harness

Harness de **Spec-Driven Development** para agentes de IA (ex.: Claude Code). Você descreve o sistema em linguagem livre; o harness conduz, fase a fase e com gates, até um **backlog pronto para Scrum ou Kanban**: épicos, user stories (BDD/EARS), UML, ADRs, tasks, plano de testes, rastreabilidade e export para o quadro.

> Só especificação. **Nenhum código de aplicação é gerado.** Idioma da saída: português (pt-BR).

## Instalação
```bash
git clone <este-repositorio> && cd sdd-harness
./install.sh /caminho/do/seu-projeto      # copia skills, subagentes, scripts, templates e CI
```
Ou use este repositório diretamente como *template repository* e abra o agente na raiz. Requer **Python 3.9+** (sem dependências). Opcional: `npm i -g @mermaid-js/mermaid-cli` para validar sintaxe Mermaid completa.

## Uso rápido
```
/sdd-init                      # nome, modo (greenfield/evolução), Scrum/Kanban, perfil da equipe
/sdd-intake <seu prompt livre> # texto bruto, imutável (pode ser transcrição de voz)
/sdd-discover                  # atores, escopo, suposições, perguntas, tamanho
/sdd-stack                     # escolha guiada camada por camada, com recomendação e ADRs
/sdd-spec                      # épicos, US, AC em BDD/EARS, RN, RNF
/sdd-design                    # UML (Mermaid), modelo de dados, contratos de API
/sdd-plan                      # tasks atômicas, spikes, riscos, plano Scrum ou Kanban
/sdd-quality                   # plano de testes, rastreabilidade, revisão independente
/sdd-export                    # Jira, Linear, Trello, GitHub Issues, CSV
/sdd-docs                      # documento final: especificação, casos de uso e UML em Markdown, HTML e PDF
```
Atalho: `/sdd-run "descrição do sistema"` executa tudo, parando em cada gate.
Sistema existente: `/sdd-adopt` (baseline) e `/sdd-evolve` (mudança como delta). Outros: `/sdd-status`, `/sdd-back <fase>`.

## Fluxo e gates
| Fase | Skill | Saída principal | Gate mecânico |
|---|---|---|---|
| 0 | `sdd-intake` | `00-intake/raw.md` + hash | integridade do hash |
| 1 | `sdd-discover` | contexto, suposições, perguntas, tamanho | sem pergunta bloqueante |
| 2 | `sdd-stack` | ADRs, `project.yaml#stack` | ADR por camada, aprovados |
| 3 | `sdd-spec` | `spec.md` | `validate_spec`, `lint_language`, `check_sizing` |
| 4 | `sdd-design` | `.mmd`, dados, contratos, `design.md` | `validate_diagrams` |
| 5 | `sdd-plan` | `tasks.md`, riscos, plano | `validate_tasks`, `graph_deps` |
| 6 | `sdd-quality` | testes, rastreabilidade, revisão | `validate_traceability` + revisor independente |
| 7 | `sdd-export` | `backlog.json` + CSV/JSON | `validate_export` |

Gate N = fase N concluída (`--gate 0` valida só a estrutura). Rodar manualmente: `python3 harness/scripts/run_all.py --gate 3`. O gate 1 exige o Discovery suficiente e aprovado (`01-discovery/suficiencia.md`). Os gates 2–7 também validam os packs tecnológicos. Para avaliar os próprios comportamentos de IA, consulte `evals/README.md`; o autoteste mecânico não prova sozinho a qualidade semântica.

## Estrutura do repositório
```
.claude/skills/sdd-*/        14 skills (uma por fase + adopt, evolve, status, back, run) e references/
.claude/agents/              spec-reviewer, ambiguity-adversary, stack-analyst, legacy-analyst
harness/scripts/             validadores, rastreabilidade, rank_stack/validate_stacks, status, export, init_project, selftest
harness/templates/sdd/       arquivos iniciais do .sdd/
harness/templates/evolucao/  templates do modo evolução (legado/, mudancas/)
harness/templates/extras/    ADR e documento de refinamento
harness/stacks/              packs de stack: django, nextjs, spring-boot, dotnet, _template
harness/schemas/             contratos JSON (backlog, project)
evals/                         cenários adversariais e rubrica de qualidade do harness
examples/biblioteca-comunitaria/   projeto de exemplo completo (passa no gate 7)
docs/ARQUITETURA.md          desenho e justificativas
.github/                     CI de validação, template de PR, issue de refinamento
```

## Estrutura gerada no projeto (`.sdd/`)
`project.yaml` · `STATE.md` · `LESSONS.md` · `GLOSSARIO.md` · `00-intake/` · `01-discovery/` · `02-stack/(adr/)` · `03-requisitos/` · `04-design/(diagramas/)` · `05-planejamento/` · `06-qualidade/` · `07-export/` · `legado/` e `mudancas/` (só no modo evolução).

## Scripts
| Script | Função |
|---|---|
| `validate_spec.py` | IDs, US, AC em BDD/EARS, RN/RNF, origem obrigatória |
| `lint_language.py` | termos vagos, "e/ou", voz passiva |
| `validate_tasks.py` | refs existentes, DoD, estimativa e limite por metodologia |
| `graph_deps.py` | ciclos e caminho crítico |
| `validate_traceability.py` | AC↔task↔teste; `--write` gera a matriz |
| `validate_diagrams.py` | tipo, `%% refs`, delimitadores; `mmdc` se instalado |
| `validate_discovery.py` | suficiência do Discovery: 9 domínios com evidência, registro de conhecimento tipado, lacunas aceitas com responsável, aprovação vinculada ao hash do intake |
| `validate_state.py` | `project.yaml`, perguntas bloqueantes, ADRs, hash do intake |
| `validate_stale.py` / `stamp.py` | obsolescência por hash de insumos |
| `check_sizing.py` | limites por tamanho (pequeno/médio/grande) |
| `rank_stack.py` | ranking transparente por camada a partir dos packs, com validação prévia e limites de pesos |
| `validate_stacks.py` | valida campos, notas, IDs e referências de compatibilidade dos packs |
| `export/build_backlog.py` · `export/convert.py` | backlog canônico → jira, linear, trello, github, csv |
| `build_docs.py` | documentação final: `especificacao.md`, `casos-de-uso.md`, `diagramas.md`, HTML e PDF (Mermaid via `mmdc` + Chrome) |
| `status.py` · `lessons.py` · `init_project.py` | estado/fase, lições, scaffold |
| `selftest.sh` | autoteste usado na CI |

Os validadores de artefatos aceitam `--sdd <pasta>` e `--json`; `validate_stacks.py` aceita `--pack`/`--arquivo`, e `rank_stack.py` usa `--pack`. Código de saída ≠ 0 quando há erro.

## Convenções de formato (lidas pelos scripts)
US `### US001: título`, campos `- **Campo:** valor` (um por linha), AC `**AC001.1 (BDD|EARS)**`, regras `**RN001**: ...`, tasks `### TSK001: ...`, casos `### CT001.1.1: ...`. Templates e exemplo mostram o formato exato; blocos HTML `<!-- -->` e cercas de código são ignorados pelos parsers.

## Adicionar uma stack
Copie `harness/stacks/_template/`, preencha o `pack.json`, valide com `python3 harness/scripts/validate_stacks.py --pack <nome>` e só então use `rank_stack.py --pack <nome>`. Veja `harness/stacks/README.md`. Sem pack, o agente analisa em modo genérico e marca confiança baixa.

## Limitações conhecidas
- A suficiência do Discovery é verificada em **forma e referências** (campos, IDs, aprovação, hash do intake); a qualidade das respostas continua dependendo do agente e da revisão humana.
- Mermaid: sem `mmdc` a validação é estrutural.
- As notas dos packs são julgamento curado, não medição: confirme versões e suporte em fontes oficiais antes de decidir. A data de revisão do pack não prova verificação atual.
- O parser de YAML é um subconjunto próprio (mapas, listas simples, `[a, b]`); mantenha `project.yaml` simples.
- Skills e subagentes são instruções para o agente: a garantia "somente leitura" dos revisores depende das ferramentas concedidas e das regras do prompt.
- Os conversores de export geram arquivos de partida; ajuste o mapeamento de colunas conforme a configuração do seu Jira/Linear/Trello. Isso não é integração com APIs nem cria itens remotamente.
