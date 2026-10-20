#!/usr/bin/env python3
"""Gate da Fase 5: valida tasks.md."""
import re
from sddlib import *

TIPOS = {"backend", "frontend", "infra", "qa", "design", "dados", "seguranca", "docs", "spike", "devops", "mobile"}


def main():
    a = std_args("Valida tasks.md").parse_args()
    sdd = get_sdd(a.sdd)
    r = Report("validate_tasks")
    proj = load_project(sdd)
    limite = (proj.get("limites") or {}).get("max_tarefa") or (5 if proj.get("metodologia") != "kanban" else 2)
    tasks = parse_tasks(read(sdd / TASKS))
    if not tasks:
        r.erro("TASK-000", f"nenhuma task em {TASKS} (formato '### TSK001: Título')")
        return r.emit(a.json)
    spec = parse_spec(read(sdd / SPEC))
    valid = {s["id"] for s in spec["stories"]} | {ac["id"] for s in spec["stories"] for ac in s["acs"]}
    valid |= {i for i, _ in spec["rn"]} | {i for i, _ in spec["rnf"]} | {e["id"] for e in spec["epics"]}
    adrs = {p.name[:7] for p in (sdd / "02-stack" / "adr").glob("ADR-*.md")} if (sdd / "02-stack" / "adr").exists() else set()
    ids = [t["id"] for t in tasks]
    for t in tasks:
        i = t["id"]
        if not t["title"].strip() or len(t["title"].strip()) < 8:
            r.erro("TASK-002", f"{i}: título ausente ou vago; descreva um resultado concreto")
        if len(t["fields"].get("descricao", "").strip()) < 20:
            r.erro("TASK-003", f"{i}: descrição ausente ou insuficiente; explique o que fazer e por quê")
        if ids.count(i) > 1:
            r.erro("TASK-001", f"ID duplicado: {i}")
        if not t["refs"]:
            r.erro("TASK-010", f"{i}: sem 'Refs' (US/AC/RN/RNF/ADR)")
        for ref in t["refs"]:
            if ref.startswith("ADR"):
                if ref not in adrs:
                    r.erro("TASK-011", f"{i}: referencia {ref}, que não existe em 02-stack/adr/")
            elif ref not in valid:
                r.erro("TASK-011", f"{i}: referencia {ref}, que não existe na spec")
        if t["tipo"] not in TIPOS:
            r.erro("TASK-020", f"{i}: 'Tipo' inválido ('{t['tipo']}'). Use: {', '.join(sorted(TIPOS))}")
        if t["est"] is None:
            r.erro("TASK-030", f"{i}: sem 'Estimativa'")
        elif t["est"] <= 0:
            r.erro("TASK-032", f"{i}: estimativa deve ser maior que zero")
        elif t["est"] > limite:
            r.erro("TASK-031", f"{i}: estimativa {t['est']:g} acima do limite ({limite}); quebre a task")
        if t["dod"] < 1:
            r.erro("TASK-040", f"{i}: sem 'Definition of Done' (checklist '- [ ]')")
        for d in t["depende"]:
            if d not in ids:
                r.erro("TASK-050", f"{i}: depende de {d}, que não existe")
            if d == i:
                r.erro("TASK-051", f"{i}: depende de si mesma")
        if t["confianca"] in ("baixa",) and not i.startswith("SPK"):
            r.aviso("TASK-060", f"{i}: confiança baixa, considere criar um spike")
        if i.startswith("SPK") and t["tipo"] != "spike":
            r.aviso("TASK-061", f"{i}: spikes devem ter Tipo 'spike'")
        if i.startswith("SPK") and not re.search(r"(?i)time-?box", t["fields"].get("descricao", "")):
            r.aviso("TASK-062", f"{i}: spike deve declarar timebox e pergunta que pretende responder")
    return r.emit(a.json)


if __name__ == "__main__":
    raise SystemExit(main())
