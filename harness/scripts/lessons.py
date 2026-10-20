#!/usr/bin/env python3
"""Registra uma lição sobre qualidade de especificação em .sdd/LESSONS.md."""
import re
from sddlib import *


def main():
    ap = std_args("Adiciona lição")
    ap.add_argument("--padrao", required=True)
    ap.add_argument("--detectado", required=True)
    ap.add_argument("--regra", required=True)
    ap.add_argument("--fase", required=True)
    a = ap.parse_args()
    sdd = get_sdd(a.sdd)
    f = sdd / "LESSONS.md"
    t = read(f) or "# Lições aprendidas (qualidade da especificação)\n"
    n = max([int(x) for x in re.findall(r"^### L(\d{3})", t, re.M)] or [0]) + 1
    t = t.rstrip() + f"\n\n### L{n:03d}\n- **Padrão:** {a.padrao}\n- **Detectado por:** {a.detectado}\n- **Regra derivada:** {a.regra}\n- **Aplica-se a:** fase {a.fase}\n"
    f.write_text(t, encoding="utf-8")
    print(f"lição L{n:03d} registrada")


if __name__ == "__main__":
    main()
