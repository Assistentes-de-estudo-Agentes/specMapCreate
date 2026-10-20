#!/usr/bin/env python3
"""Mostra o estado do projeto. Com --set-fase N --motivo '...' reabre/avança fase e registra no STATE.md."""
import datetime
import re
from sddlib import *

NOMES = ["Intake", "Discovery", "Stack", "Requisitos", "Design/UML", "Planejamento", "Qualidade", "Export"]


def main():
    ap = std_args("Status do projeto")
    ap.add_argument("--set-fase", type=int)
    ap.add_argument("--motivo", default="")
    a = ap.parse_args()
    sdd = get_sdd(a.sdd)
    py = sdd / "project.yaml"
    if a.set_fase is not None:
        t = re.sub(r"^fase_atual:.*$", f"fase_atual: {a.set_fase}", read(py), flags=re.M)
        py.write_text(t, encoding="utf-8")
        st = sdd / "STATE.md"
        st.write_text(read(st).rstrip() + f"\n| {datetime.date.today()} | fase -> {a.set_fase} ({NOMES[a.set_fase]}) | {a.motivo or '-'} |\n", encoding="utf-8")
    p = load_project(sdd)
    spec = parse_spec(read(sdd / SPEC))
    tasks = parse_tasks(read(sdd / TASKS))
    qs = bold_items(clean(read(sdd / QUESTIONS)), "Q")
    abertas = [q for q in qs if norm(q["fields"].get("status", "aberta")).startswith("aberta")]
    print(f"Projeto: {p.get('nome')} | modo={p.get('modo')} | metodologia={p.get('metodologia')} | tamanho={p.get('tamanho')}")
    f = p.get("fase_atual", 0)
    print(f"Fase atual: {f} ({NOMES[f] if isinstance(f, int) and f < 8 else '?'})")
    print(f"Épicos={len(spec['epics'])} US={len(spec['stories'])} AC={sum(len(s['acs']) for s in spec['stories'])} Tasks={len(tasks)}")
    print(f"Perguntas abertas: {len(abertas)} (bloqueantes: {len([q for q in abertas if norm(q['fields'].get('impacto', '')).startswith('bloqueante')])})")
    stale = [rel for rel, deps in DEPS.items() if (sdd / rel).exists() and (split_front(read(sdd / rel))[0].get("derivado_de") or {}) and any((split_front(read(sdd / rel))[0]["derivado_de"].get(d) != content_hash(sdd / d)) for d in deps)]
    print("Artefatos stale: " + (", ".join(stale) if stale else "nenhum"))


if __name__ == "__main__":
    main()
