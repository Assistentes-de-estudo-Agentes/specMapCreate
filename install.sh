#!/usr/bin/env bash
# Instala o harness em um projeto: ./install.sh /caminho/do/projeto
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${1:-.}"
mkdir -p "$DEST/.claude/skills" "$DEST/.claude/agents" "$DEST/.github/workflows" "$DEST/.github/ISSUE_TEMPLATE"
cp -R "$SRC/.claude/skills/." "$DEST/.claude/skills/"
cp -R "$SRC/.claude/agents/." "$DEST/.claude/agents/"
rm -rf "$DEST/harness"; cp -R "$SRC/harness" "$DEST/harness"
find "$DEST/harness" -name __pycache__ -prune -exec rm -rf {} +
cp "$SRC/.github/workflows/validate-spec.yml" "$DEST/.github/workflows/"
cp "$SRC/.github/ISSUE_TEMPLATE/refinamento.yml" "$DEST/.github/ISSUE_TEMPLATE/"
[ -f "$DEST/.github/pull_request_template.md" ] || cp "$SRC/.github/pull_request_template.md" "$DEST/.github/"
[ -f "$DEST/AGENTS.md" ] || cp "$SRC/AGENTS.md" "$DEST/AGENTS.md"
if [ ! -f "$DEST/CLAUDE.md" ]; then cp "$SRC/CLAUDE.md" "$DEST/CLAUDE.md"; elif ! grep -q "@AGENTS.md" "$DEST/CLAUDE.md"; then printf '\n@AGENTS.md\n' >> "$DEST/CLAUDE.md"; fi
mkdir -p "$DEST/examples" && cp -R "$SRC/examples/." "$DEST/examples/"
[ -d "$SRC/evals" ] && mkdir -p "$DEST/evals" && cp -R "$SRC/evals/." "$DEST/evals/"
echo "Harness instalado em $DEST. Abra o agente na pasta e rode /sdd-init (ou /sdd-run \"descrição do sistema\")."
