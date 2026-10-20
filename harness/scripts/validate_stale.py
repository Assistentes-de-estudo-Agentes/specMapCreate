#!/usr/bin/env python3
"""Detecta artefatos derivados cujos insumos mudaram depois da geração."""
from sddlib import *


def main():
    a = std_args("Controle de stale").parse_args()
    sdd = get_sdd(a.sdd)
    r = Report("validate_stale")
    for rel, deps in DEPS.items():
        p = sdd / rel
        if not p.exists():
            continue
        fm, _ = split_front(read(p))
        stored = fm.get("derivado_de") or {}
        if not stored:
            r.aviso("STALE-001", f"{rel}: sem front matter; rode stamp.py {rel}")
            continue
        for dep in deps:
            if stored.get(dep) != content_hash(sdd / dep):
                r.erro("STALE-002", f"{rel} está STALE: '{dep}' mudou. Revise/regere e rode stamp.py {rel}")
    return r.emit(a.json)


if __name__ == "__main__":
    raise SystemExit(main())
