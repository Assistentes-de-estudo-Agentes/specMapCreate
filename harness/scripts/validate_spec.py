#!/usr/bin/env python3
"""Gate da Fase 3: valida spec.md (IDs, US, AC em BDD/EARS, RN/RNF)."""
import re
from sddlib import *

PRIOR = {"must", "should", "could", "wont", "won't"}


def main():
    a = std_args("Valida spec.md").parse_args()
    sdd = get_sdd(a.sdd)
    r = Report("validate_spec")
    text = read(sdd / SPEC)
    if not text.strip():
        r.erro("SPEC-000", f"{SPEC} ausente ou vazio")
        return r.emit(a.json)
    spec = parse_spec(text)
    epics = {e["id"] for e in spec["epics"]}
    rn = {i for i, _ in spec["rn"]}
    rnf = {i for i, _ in spec["rnf"]}
    if not spec["stories"]:
        r.erro("SPEC-001", "nenhuma User Story encontrada (formato: '### US001: Título')")
    seen = set()
    for kind, ids in (("EP", [e["id"] for e in spec["epics"]]), ("US", [s["id"] for s in spec["stories"]]),
                      ("RN", [i for i, _ in spec["rn"]]), ("RNF", [i for i, _ in spec["rnf"]])):
        for i in ids:
            if i in seen:
                r.erro("SPEC-002", f"ID duplicado: {i}")
            seen.add(i)
    for e in spec["epics"]:
        if not any(e["id"] in s["fields"].get("epico", "") for s in spec["stories"]):
            r.aviso("SPEC-003", f"{e['id']} não possui nenhuma US")
    for s in spec["stories"]:
        f, sid = s["fields"], s["id"]
        ep = re.findall(r"EP\d{3}", f.get("epico", ""))
        if not ep or any(x not in epics for x in ep):
            r.erro("SPEC-010", f"{sid}: campo 'Épico' ausente ou aponta para épico inexistente")
        if norm(f.get("prioridade", "")).split(" ")[0] not in PRIOR:
            r.erro("SPEC-011", f"{sid}: 'Prioridade' deve ser Must/Should/Could/Won't")
        if norm(f.get("mvp", "")) not in {"sim", "nao", "yes", "no"}:
            r.erro("SPEC-012", f"{sid}: 'MVP' deve ser sim ou não")
        if len(f.get("origem", "")) < 3:
            r.erro("SPEC-013", f"{sid}: 'Origem' obrigatória (trecho do intake ou suposição Axxx)")
        hist = f.get("historia", "").replace("*", "")
        if not re.match(r"(?i)^como\s+.+?,?\s+quero\s+.+?\s+para\s+.+$", hist):
            r.erro("SPEC-014", f"{sid}: história fora do padrão 'Como [papel], quero [ação] para [objetivo]'")
        for x in re.findall(r"RN\d{3}", f.get("regras de negocio", "")):
            if x not in rn:
                r.erro("SPEC-015", f"{sid}: referencia {x}, que não está definida")
        for x in re.findall(r"RNF\d{3}", f.get("nfr relacionados", "")):
            if x not in rnf:
                r.erro("SPEC-016", f"{sid}: referencia {x}, que não está definido")
        if not s["acs"]:
            r.erro("SPEC-020", f"{sid}: nenhum critério de aceite (formato '**AC001.1 (BDD)**')")
        for ac in s["acs"]:
            n = norm(ac["text"])
            if ac["id"][2:5] != sid[2:5]:
                r.erro("SPEC-021", f"{ac['id']} não pertence a {sid}")
            if ac["tipo"] == "BDD":
                if not re.search(r"dado que.*quando.*entao", n):
                    r.erro("SPEC-022", f"{ac['id']}: BDD exige 'Dado que / Quando / Então' nessa ordem")
            else:
                if not re.match(r"^(quando|se|enquanto|onde|durante|apos)\b.*\bdeve\b|^o sistema deve\b", n):
                    r.erro("SPEC-023", f"{ac['id']}: EARS exige 'Quando/Se/Enquanto/Onde ... deve ...' ou 'O sistema deve ...'")
    for i, t in spec["rnf"]:
        if not re.search(r"\d", t):
            r.aviso("SPEC-030", f"{i}: RNF sem métrica numérica mensurável")
    if spec["stories"] and not any(norm(s["fields"].get("mvp", "")) in {"sim", "yes"} for s in spec["stories"]):
        r.aviso("SPEC-040", "nenhuma US marcada como MVP")
    return r.emit(a.json)


if __name__ == "__main__":
    raise SystemExit(main())
