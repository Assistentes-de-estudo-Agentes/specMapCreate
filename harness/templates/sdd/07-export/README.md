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
