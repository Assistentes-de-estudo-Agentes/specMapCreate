#!/usr/bin/env python3
"""Valida project.yaml, perguntas bloqueantes, ADRs e integridade do intake."""
import re
from sddlib import *

FASES = range(0, 8)


def main():
    ap = std_args("Valida estado do projeto")
    ap.add_argument("--gate", type=int, help="fase cuja conclusão está sendo validada (padrão: fase_atual - 1)")
    a = ap.parse_args()
    sdd = get_sdd(a.sdd)
    r = Report("validate_state")
    p = load_project(sdd)
    if not p:
        r.erro("STATE-000", "project.yaml ausente ou vazio")
        return r.emit(a.json)
    enums = {"modo": ("greenfield", "evolucao"), "metodologia": ("scrum", "kanban"),
             "tamanho": ("pequeno", "medio", "grande", "indefinido"), "idioma": ("pt-BR",)}
    for k, vals in enums.items():
        if p.get(k) not in vals:
            r.erro("STATE-001", f"project.yaml: '{k}' deve ser um de {vals} (atual: {p.get(k)})")
    fase = p.get("fase_atual")
    if fase not in FASES:
        r.erro("STATE-002", "project.yaml: 'fase_atual' deve ser 0..7")
        return r.emit(a.json)
    if p.get("modo") == "evolucao" and not (sdd / "legado" / "baseline.md").exists():
        r.erro("STATE-003", "modo evolução exige legado/baseline.md (rode /sdd-adopt)")
    raw = sdd / RAW
    if p.get("intake_sha256") and raw.exists() and raw_sha256(raw) != p["intake_sha256"]:
        r.erro("STATE-010", "raw.md foi alterado após o registro do hash; o intake é imutável")
    completed = a.gate if a.gate is not None else max(fase - 1, 0)
    if (fase >= 1 or completed >= 1) and not read(raw).strip():
        r.erro("STATE-011", "intake vazio")
    qs = bold_items(clean(read(sdd / QUESTIONS)), "Q")
    abertas = [q for q in qs if norm(q["fields"].get("status", "aberta")).startswith("aberta")]
    bloq = [q for q in abertas if norm(q["fields"].get("impacto", "")).startswith("bloqueante")]
    for q in qs:
        if not q["fields"].get("impacto"):
            r.erro("STATE-020", f"{q['id']}: sem 'Impacto' (bloqueante/importante/cosmético)")
    if completed >= 1 and bloq:
        r.erro("STATE-021", "perguntas bloqueantes em aberto: " + ", ".join(q["id"] for q in bloq))
    elif abertas:
        r.aviso("STATE-022", f"{len(abertas)} pergunta(s) aberta(s) não bloqueante(s)")
    for s in bold_items(clean(read(sdd / ASSUMPTIONS)), "A"):
        if not s["fields"].get("confianca"):
            r.aviso("STATE-030", f"{s['id']}: suposição sem 'Confiança'")
    stack = {k: v for k, v in (p.get("stack") or {}).items() if v}
    adrdir = sdd / "02-stack" / "adr"
    adrs = sorted(adrdir.glob("ADR-*.md")) if adrdir.exists() else []
    if completed >= 2:
        if not stack and p.get("modo") == "greenfield":
            r.erro("STATE-040", "stack não definida em project.yaml")
        if len(adrs) < len(stack):
            r.erro("STATE-041", f"{len(stack)} camada(s) escolhida(s) mas só {len(adrs)} ADR(s)")
        for f in adrs:
            if re.search(r"status:\**\s*propost", norm(read(f))):
                r.erro("STATE-042", f"{f.name}: ADR ainda 'proposta'; aprove antes de avançar")
    return r.emit(a.json)


if __name__ == "__main__":
    raise SystemExit(main())
