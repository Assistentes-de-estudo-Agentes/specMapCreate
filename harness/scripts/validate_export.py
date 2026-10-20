#!/usr/bin/env python3
"""Valida backlog.json contra o contrato (campos obrigatórios e integridade)."""
import json
from sddlib import *


def main():
    a = std_args("Valida backlog.json").parse_args()
    sdd = get_sdd(a.sdd)
    r = Report("validate_export")
    p = sdd / "07-export" / "backlog.json"
    if not p.exists():
        r.erro("EXP-000", "backlog.json ausente; rode export/build_backlog.py")
        return r.emit(a.json)
    try:
        b = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        r.erro("EXP-001", f"JSON inválido: {e}")
        return r.emit(a.json)
    for k in ("versao_schema", "projeto", "metodologia", "epicos", "fundacao"):
        if k not in b:
            r.erro("EXP-002", f"campo obrigatório ausente: {k}")
    ids = []
    for e in b.get("epicos", []):
        for h in e.get("historias", []):
            ids.append(h["id"])
            if not h.get("criterios"):
                r.erro("EXP-010", f"{h['id']}: sem critérios")
            for t in h.get("tasks", []):
                ids.append(t["id"])
                if t.get("estimativa") is None:
                    r.erro("EXP-011", f"{t['id']}: sem estimativa")
    for t in b.get("fundacao", []):
        ids.append(t["id"])
    if len(ids) != len(set(ids)):
        r.erro("EXP-020", "IDs duplicados no backlog")
    spec = parse_spec(read(sdd / SPEC))
    if len(spec["stories"]) != sum(len(e["historias"]) for e in b.get("epicos", [])):
        r.erro("EXP-030", "backlog.json desatualizado em relação à spec (reexporte)")
    return r.emit(a.json)


if __name__ == "__main__":
    raise SystemExit(main())
