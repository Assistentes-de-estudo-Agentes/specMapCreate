# Exportações do backlog

Esta pasta contém artefatos gerados e prontos para revisão/versionamento:

- `backlog.json`: backlog canônico consumível por ferramentas e scripts.
- `backlog.yml`: mesmo conteúdo em YAML legível, incluindo RF, US, tasks, regras, NFR e ordem de implementação.
- `github-issues.json`: payload de issues para importação/automação no GitHub.
- `github-issues.sh`: script opcional que cria issues com GitHub CLI; revise antes de executar.
- `*.csv`: formatos de importação para Jira, Linear, Trello ou planilha, conforme o comando utilizado.

Os arquivos são derivados de `03-requisitos/spec.md` e `05-planejamento/tasks.md`. Regenere-os após alterar essas fontes; não edite manualmente os arquivos gerados como fonte de verdade.

## Gerar

```bash
python harness/scripts/export/build_backlog.py
python harness/scripts/export/convert.py --alvo github --dry-run
python harness/scripts/export/convert.py --alvo github
```

O último comando apenas gera os arquivos locais. Para criar issues remotas, é necessária autenticação do GitHub CLI e execução consciente do script `github-issues.sh`.

## SoftTracker (integração externa)

Ao executar `build_backlog.py`, o specMap também gera, na raiz do projeto, a pasta `softtracker/` com dois contratos YAML:

- `softtracker/spec.yaml`: formato compacto com stack, requisitos disponíveis, casos de uso, referências UML encontradas e tasks com critérios.
- `softtracker/especificacao.yml`: formato detalhado com RF, RNF, regras de negócio, histórias/casos de uso, tasks, critérios de aceite e ordem de implementação.

Os arquivos são derivados de `project.yaml`, `03-requisitos/spec.md`, `04-design/design.md` e `05-planejamento/tasks.md`. Não edite os arquivos gerados como fonte de verdade. Para gerá-los separadamente:

```bash
python harness/scripts/export/build_softtracker.py --sdd .sdd --saida softtracker
```

Quando a fonte não declara RF, RNF, status ou classes UML, o exportador não inventa esses dados; campos ausentes permanecem vazios ou como `nao_especificado`.
