#!/usr/bin/env python3
"""Gate da Fase 6: rastreabilidade Requisito -> US -> AC -> Task -> Caso de teste."""
from sddlib import *


def main():
    ap = std_args("Rastreabilidade")
    ap.add_argument("--write", action="store_true", help="gera 06-qualidade/rastreabilidade.md")
    a = ap.parse_args()
    sdd = get_sdd(a.sdd)
    r = Report("validate_traceability")
    spec = parse_spec(read(sdd / SPEC))
    tasks = parse_tasks(read(sdd / TASKS))
    tests = parse_tests(read(sdd / TESTS))
    ac_ids = [ac["id"] for s in spec["stories"] for ac in s["acs"]]
    story_ids = [s["id"] for s in spec["stories"]]
    task_ids = [t["id"] for t in tasks]
    test_ids = [c["id"] for c in tests]
    known_spec_refs = ({e["id"] for e in spec["epics"]} | set(story_ids) | set(ac_ids)
                       | {i for i, _ in spec["rn"]} | {i for i, _ in spec["rnf"]})
    for label, values in (("AC", ac_ids), ("US", story_ids), ("task", task_ids), ("teste", test_ids)):
        seen_ids = set()
        for value in values:
            if value in seen_ids:
                r.erro("TRACE-007", f"ID duplicado ({label}): {value}")
            seen_ids.add(value)
    task_by_ac = {x: [] for x in ac_ids}
    test_id_set = set(test_ids)
    for t in tasks:
        for ref in t["refs"]:
            if ref in task_by_ac:
                task_by_ac[ref].append(t["id"])
            elif ref not in known_spec_refs and not ref.startswith("ADR-"):
                r.erro("TRACE-008", f"{t['id']} referencia {ref}, que não existe na especificação")
        for ct in t["cts"]:
            if ct not in test_id_set:
                r.erro("TRACE-012", f"{t['id']} lista {ct} em 'Casos de teste', mas o caso não existe em {TESTS}")
    ct_by_ac = {x: [] for x in ac_ids}
    for c in tests:
        for x in c["cobre"]:
            if x in ct_by_ac:
                ct_by_ac[x].append(c["id"])
            else:
                r.erro("TRACE-004", f"{c['id']} cobre {x}, que não existe na spec")
    for x in ac_ids:
        if not task_by_ac[x]:
            r.erro("TRACE-001", f"{x}: nenhuma task implementa este critério")
        if not ct_by_ac[x]:
            r.erro("TRACE-002", f"{x}: sem caso de teste em {TESTS}")
    for t in tasks:
        if not t["refs"]:
            r.erro("TRACE-003", f"{t['id']}: task órfã (sem Refs)")
    for c in tests:
        if not c["cobre"]:
            r.erro("TRACE-009", f"{c['id']}: caso de teste sem critério em 'Cobre'")
        if not any(x in ac_ids for x in c["cobre"]):
            r.aviso("TRACE-010", f"{c['id']}: caso de teste não cobre nenhum AC reconhecido")
    for s in spec["stories"]:
        if not any(s["id"] in t["refs"] or any(ac["id"] in t["refs"] for ac in s["acs"]) for t in tasks):
            r.erro("TRACE-005", f"{s['id']}: nenhuma task associada")
        if not s["acs"]:
            r.erro("TRACE-011", f"{s['id']}: história sem critérios de aceitação rastreáveis")
    used = set()
    for s in spec["stories"]:
        used |= set(REF_RE.findall(s["fields"].get("regras de negocio", "") + " " + s["fields"].get("nfr relacionados", "")))
    for t in tasks:
        used |= set(t["refs"])
    for i, _ in spec["rn"] + spec["rnf"]:
        if i not in used:
            r.aviso("TRACE-006", f"{i}: não é referenciado por nenhuma US ou task")
    if a.write:
        L = ["# Matriz de rastreabilidade", "", "| US | AC | Tasks | Casos de teste |", "|---|---|---|---|"]
        for s in spec["stories"]:
            for ac in s["acs"]:
                L.append(f"| {s['id']} | {ac['id']} | {', '.join(task_by_ac[ac['id']]) or '—'} | {', '.join(ct_by_ac[ac['id']]) or '—'} |")
        L += ["", "_Gerado por `validate_traceability.py --write`. Não edite manualmente._", ""]
        (sdd / TRACE).parent.mkdir(parents=True, exist_ok=True)
        (sdd / TRACE).write_text("\n".join(L), encoding="utf-8")
        stamp(sdd, TRACE)
        r.info("TRACE-100", f"{TRACE} atualizado")
    return r.emit(a.json)


if __name__ == "__main__":
    raise SystemExit(main())
