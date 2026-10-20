#!/usr/bin/env python3
"""Gera o backlog canônico (07-export/backlog.json) a partir de spec.md + tasks.md."""
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sddlib import *


def main():
    a = std_args("Gera backlog.json").parse_args()
    sdd = get_sdd(a.sdd)
    proj = load_project(sdd)
    spec = parse_spec(read(sdd / SPEC))
    tasks = parse_tasks(read(sdd / TASKS))
    tests = parse_tests(read(sdd / TESTS))
    rn = dict(spec["rn"])
    rnf = dict(spec["rnf"])
    story_of_ac = {ac["id"]: s["id"] for s in spec["stories"] for ac in s["acs"]}

    def tdict(t):
        return {"id": t["id"], "titulo": t["title"], "tipo": t["tipo"], "estimativa": t["est"],
                "confianca": t["confianca"], "depende_de": t["depende"], "refs": t["refs"],
                "descricao": t["fields"].get("descricao", ""), "dod": [l.strip()[6:].strip() for l in t["lines"] if l.strip().startswith(("- [ ]", "- [x]", "- [X]"))],
                "casos_de_teste": t["cts"]}

    by_story, fundacao = {}, []
    for t in tasks:
        owners = {r for r in t["refs"] if r.startswith("US")} | {story_of_ac[r] for r in t["refs"] if r in story_of_ac}
        if owners:
            for o in sorted(owners)[:1]:
                by_story.setdefault(o, []).append(tdict(t))
        else:
            fundacao.append(tdict(t))
    epicos = []
    for e in spec["epics"]:
        hist = []
        for s in spec["stories"]:
            if e["id"] in s["fields"].get("epico", ""):
                f = s["fields"]
                hist.append({"id": s["id"], "titulo": s["title"], "prioridade": f.get("prioridade", ""), "mvp": norm(f.get("mvp", "")) in ("sim", "yes"),
                             "historia": f.get("historia", "").replace("*", ""),
                             "regras_de_negocio": {i: rn.get(i, "") for i in REF_RE.findall(f.get("regras de negocio", "")) if i in rn},
                             "criterios": [{"id": ac["id"], "tipo": ac["tipo"], "texto": ac["text"]} for ac in s["acs"]],
                             "casos_de_teste": [c["id"] for c in tests if any(x in {ac["id"] for ac in s["acs"]} for x in c["cobre"])],
                             "tasks": by_story.get(s["id"], [])})
        epicos.append({"id": e["id"], "titulo": e["title"], "historias": hist})
    out = {"versao_schema": 1, "projeto": proj.get("nome", ""), "metodologia": proj.get("metodologia", ""),
           "gerado_em": datetime.date.today().isoformat(), "epicos": epicos, "fundacao": fundacao,
           "rnf": [{"id": i, "texto": t} for i, t in spec["rnf"]]}
    dest = sdd / "07-export" / "backlog.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"backlog gerado: {dest} ({sum(len(e['historias']) for e in epicos)} US, {len(tasks)} tasks)")


if __name__ == "__main__":
    main()
