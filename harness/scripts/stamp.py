#!/usr/bin/env python3
"""Registra hashes: intake (imutável) e insumos de artefatos derivados."""
import re
import sys
from sddlib import *


def main():
    ap = std_args("Stamp de hashes")
    ap.add_argument("artefatos", nargs="*", help="caminhos relativos a .sdd (ex.: 05-planejamento/tasks.md)")
    ap.add_argument("--intake", action="store_true", help="grava intake_sha256 em project.yaml")
    ap.add_argument("--all", action="store_true", help="carimba todos os derivados existentes")
    ap.add_argument("--aprovar-discovery", action="store_true", help="registra a aprovação do resumo do Discovery (só após o usuário aprovar)")
    ap.add_argument("--por", help="nome de quem aprovou")
    a = ap.parse_args()
    sdd = get_sdd(a.sdd)
    if a.aprovar_discovery:
        import datetime
        from validate_discovery import check, SUF
        if not a.por:
            sys.exit("--por é obrigatório (quem aprovou o resumo)")
        h = str(load_project(sdd).get("intake_sha256") or "")[:12]
        if not h:
            sys.exit("registre o intake antes: stamp.py --intake")
        pend = [e for e in check(sdd, 1).erros if not e[1].startswith("DISC-05")]
        if pend:
            sys.exit("corrija antes de aprovar:\n" + "\n".join(f"- {c}: {m}" for _, c, m in pend))
        f = sdd / SUF
        t = read(f)
        for label, val in (("Resumo aprovado por", a.por), ("Aprovado em", datetime.date.today().isoformat()), ("Intake (hash)", h)):
            pat = re.compile(rf"^(- \*\*{re.escape(label)}:\*\*).*$", re.M)
            t = pat.sub(lambda m: f"{m.group(1)} {val}", t, count=1) if pat.search(t) else t.rstrip() + f"\n- **{label}:** {val}\n"
        f.write_text(t, encoding="utf-8")
        print(f"Discovery aprovado por {a.por} (intake {h})")
        return
    if a.intake:
        h = raw_sha256(sdd / RAW)
        py = sdd / "project.yaml"
        t = read(py)
        t = re.sub(r"^intake_sha256:.*$", f"intake_sha256: {h}", t, flags=re.M) if "intake_sha256" in t else t.rstrip() + f"\nintake_sha256: {h}\n"
        py.write_text(t, encoding="utf-8")
        print(f"intake_sha256 = {h}")
    for rel in (list(DEPS) if a.all else a.artefatos):
        if stamp(sdd, rel):
            print(f"carimbado: {rel}")


if __name__ == "__main__":
    main()
