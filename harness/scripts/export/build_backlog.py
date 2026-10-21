#!/usr/bin/env python3
"""Gera o backlog canônico (07-export/backlog.json) a partir de spec.md + tasks.md."""
import datetime
import json
import sys
import subprocess

try:
    import yaml
except ImportError:
    yaml = None
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
    # Ordenação topológica estável das tasks; dependências desconhecidas não bloqueiam.
    by_task = {t["id"]: t for t in tasks}
    pending = list(tasks); ordered_tasks = []; done = set()
    while pending:
        ready = [t for t in pending if all(d not in by_task or d in done for d in t["depende"])]
        if not ready:
            ordered_tasks.extend(pending)
            break
        for task in ready:
            ordered_tasks.append(task); done.add(task["id"]); pending.remove(task)
    rf = [{"id": i, "texto": t} for i, t in spec.get("rf", [])]
    us_order = [{"ordem": i, "id": st["id"], "titulo": st["title"]}
                for i, st in enumerate(spec["stories"], 1)]
    task_order = [{"ordem": i, "id": t["id"], "titulo": t["title"],
                   "depende_de": t["depende"], "refs": t["refs"]}
                  for i, t in enumerate(ordered_tasks, 1)]
    out = {"versao_schema": 2, "projeto": proj.get("nome", ""), "metodologia": proj.get("metodologia", ""),
           "gerado_em": datetime.date.today().isoformat(), "epicos": epicos, "fundacao": fundacao,
           "requisitos_funcionais": rf,
           "regras_de_negocio": [{"id": i, "texto": t} for i, t in spec["rn"]],
           "rnf": [{"id": i, "texto": t} for i, t in spec["rnf"]],
           "ordem_implementacao": {"rf": [x["id"] for x in rf],
                                   "us": [x["id"] for x in us_order],
                                   "tasks": [x["id"] for x in task_order]},
           "catalogo_ordem": {"rf": rf, "us": us_order, "tasks": task_order}}
    dest = sdd / "07-export" / "backlog.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(out, ensure_ascii=False, indent=2)
    dest.write_text(serialized + "\n", encoding="utf-8")
    ydest = dest.with_suffix(".yml")
    if yaml:
        ydest.write_text(yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")
    else:
        # JSON é subconjunto válido de YAML 1.2 e mantém os dados sem dependências extras.
        ydest.write_text(serialized + "\n", encoding="utf-8")
    print(f"backlog gerado: {dest} e {ydest} ({sum(len(e['historias']) for e in epicos)} US, {len(tasks)} tasks)")
    # Exportações de compatibilidade para o programa SoftTracker ficam na raiz do projeto.
    softtracker_script = Path(__file__).resolve().parent / "build_softtracker.py"
    project_root = sdd.parent
    subprocess.run([sys.executable, str(softtracker_script), "--sdd", str(sdd),
                    "--saida", str(project_root / "softtracker")], check=True)


if __name__ == "__main__":
    main()
