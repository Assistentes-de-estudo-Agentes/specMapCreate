#!/usr/bin/env python3
"""Auto-sizing: reprova artefatos acima do permitido para o tamanho declarado."""
from sddlib import *

LIMITES = {"pequeno": {"us": 8, "diagramas": 2}, "medio": {"us": 25, "diagramas": 8}}


def main():
    a = std_args("Valida sizing").parse_args()
    sdd = get_sdd(a.sdd)
    r = Report("check_sizing")
    t = load_project(sdd).get("tamanho", "indefinido")
    spec = parse_spec(read(sdd / SPEC))
    n_us = len(spec["stories"])
    dd = sdd / "04-design" / "diagramas"
    n_d = len(list(dd.glob("*.mmd"))) if dd.exists() else 0
    r.info("SIZE-100", f"tamanho declarado: {t}; US={n_us}; diagramas={n_d}")
    if t in LIMITES:
        if n_us > LIMITES[t]["us"]:
            r.erro("SIZE-001", f"{n_us} US excedem o limite de '{t}' ({LIMITES[t]['us']}); reclassifique o projeto")
        if n_d > LIMITES[t]["diagramas"]:
            r.erro("SIZE-002", f"{n_d} diagramas excedem o limite de '{t}' ({LIMITES[t]['diagramas']})")
        if t == "pequeno" and ((sdd / "legado").exists() and any((sdd / "legado").iterdir())):
            r.aviso("SIZE-003", "projeto 'pequeno' com pasta legado/: confirme o tamanho")
    elif t == "indefinido" and n_us:
        r.aviso("SIZE-004", "tamanho 'indefinido': defina em project.yaml (pequeno/medio/grande)")
    return r.emit(a.json)


if __name__ == "__main__":
    raise SystemExit(main())
