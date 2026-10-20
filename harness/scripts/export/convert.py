#!/usr/bin/env python3
"""Converte backlog.json para CSV/JSON de ferramentas de quadro.
Alvos: generic | jira | linear | trello | github   (use --dry-run para só listar)."""
import argparse
import csv
import json
import sys
from pathlib import Path

PRIO_JIRA = {"must": "Highest", "should": "High", "could": "Medium", "wont": "Low", "won't": "Low"}
PRIO_LINEAR = {"must": 1, "should": 2, "could": 3, "wont": 4, "won't": 4}


def flatten(b):
    """Gera linhas: (tipo, id, pai, titulo, descricao, prioridade, estimativa, labels)."""
    rows = []
    for e in b["epicos"]:
        rows.append(("Epic", e["id"], "", e["titulo"], "", "", "", ["epico"]))
        for h in e["historias"]:
            ac = "\n".join(f"- {c['id']} ({c['tipo']}): {c['texto']}" for c in h["criterios"])
            desc = f"{h['historia']}\n\nCritérios de aceite:\n{ac}"
            labels = ["mvp"] if h["mvp"] else []
            rows.append(("Story", h["id"], e["id"], h["titulo"], desc, h["prioridade"].split(" ")[0].lower(), "", labels))
            for t in h["tasks"]:
                dod = "\n".join(f"- [ ] {d}" for d in t["dod"])
                rows.append(("Task", t["id"], h["id"], t["titulo"], f"{t['descricao']}\n\nDoD:\n{dod}\nRefs: {', '.join(t['refs'])}\nDepende de: {', '.join(t['depende_de']) or '-'}", "", t["estimativa"], [t["tipo"]]))
    for t in b["fundacao"]:
        dod = "\n".join(f"- [ ] {d}" for d in t["dod"])
        rows.append(("Task", t["id"], "", t["titulo"], f"{t['descricao']}\n\nDoD:\n{dod}\nRefs: {', '.join(t['refs'])}", "", t["estimativa"], [t["tipo"], "fundacao"]))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sdd", default=".sdd")
    ap.add_argument("--alvo", required=True, choices=["generic", "jira", "linear", "trello", "github"])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    src = Path(a.sdd) / "07-export" / "backlog.json"
    if not src.exists():
        sys.exit("backlog.json ausente: rode build_backlog.py")
    b = json.loads(src.read_text(encoding="utf-8"))
    rows = flatten(b)
    out = Path(a.sdd) / "07-export"
    if a.dry_run:
        for r in rows:
            print(f"{r[0]:6} {r[1]:7} pai={r[2] or '-':6} {r[3]}")
        print(f"{len(rows)} itens (dry-run, nada gravado)")
        return
    if a.alvo == "github":
        issues = [{"title": f"[{r[1]}] {r[3]}", "body": r[4] + (f"\n\nPai: {r[2]}" if r[2] else ""), "labels": r[7] + [r[0].lower()]} for r in rows]
        (out / "github-issues.json").write_text(json.dumps(issues, ensure_ascii=False, indent=2), encoding="utf-8")
        sh = ["#!/usr/bin/env bash", "# Requer GitHub CLI autenticado: gh auth login", "set -euo pipefail"]
        for i in issues:
            labels = ",".join(i["labels"])
            body = i["body"].replace("'", "'\\''")
            title = i["title"].replace("'", "'\\''")
            sh.append(f"gh issue create --title '{title}' --body '{body}' --label '{labels}'")
        (out / "github-issues.sh").write_text("\n".join(sh) + "\n", encoding="utf-8")
        print(f"gerados github-issues.json e github-issues.sh ({len(issues)} issues)")
        return
    name = {"generic": "backlog.csv", "jira": "jira.csv", "linear": "linear.csv", "trello": "trello.csv"}[a.alvo]
    with open(out / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if a.alvo in ("generic", "jira"):
            w.writerow(["Issue Id", "Issue Type", "Summary", "Description", "Priority", "Labels", "Story Points", "Parent Id"])
            for t, i, p, ti, d, pr, est, lb in rows:
                w.writerow([i, t, ti, d, PRIO_JIRA.get(pr, ""), " ".join(lb), est, p])
        elif a.alvo == "linear":
            w.writerow(["Title", "Description", "Priority", "Estimate", "Labels"])
            for t, i, p, ti, d, pr, est, lb in rows:
                if t != "Epic":
                    w.writerow([f"[{i}] {ti}", d, PRIO_LINEAR.get(pr, 0), est, ",".join(lb)])
        else:
            w.writerow(["Card Name", "Card Description", "List", "Labels"])
            for t, i, p, ti, d, pr, est, lb in rows:
                if t != "Epic":
                    w.writerow([f"[{i}] {ti}", d, "Backlog", ",".join(lb)])
    print(f"gerado: {out / name} ({len(rows)} itens). Ajuste o mapeamento de colunas ao seu projeto, se necessário.")


if __name__ == "__main__":
    main()
