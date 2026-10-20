#!/usr/bin/env python3
"""Detecta ambiguidade e linguagem vaga em spec.md e tasks.md."""
import re
from sddlib import *

VAGOS = [
    (r"\brapid[oa]s?\b|\brapidamente\b", "'rápido' sem métrica"),
    (r"amigavel|intuitiv[oa]s?|\bfacil\b|facilmente", "termo subjetivo de usabilidade"),
    (r"adequad[oa]s?|suficiente|razoavel|\bboa?s?\b", "termo vago"),
    (r"\betc\b", "'etc.' esconde requisitos"),
    (r"e/ou", "'e/ou' é ambíguo: escolha 'e' ou 'ou'"),
    (r"\bsimples\b|robust[oa]s?|moderno|eficiente|flexivel|escalavel", "adjetivo sem critério mensurável"),
    (r"quando necessario|se aplicavel|a definir|\btbd\b|talvez|possivelmente", "indefinição explícita"),
    (r"melhor(es)?\b", "comparativo sem referência"),
]
PASSIVA = re.compile(r"\bdeve(m)? ser \w+(ad|id)[oa]s?\b")


def main():
    a = std_args("Lint de linguagem").parse_args()
    sdd = get_sdd(a.sdd)
    r = Report("lint_language")
    for rel in (SPEC, TASKS):
        t = clean(read(sdd / rel))
        for n, line in enumerate(t.split("\n"), 1):
            if not line.strip() or line.lstrip().startswith(("#", ">")):
                continue
            nl = norm(line)
            for pat, why in VAGOS:
                m = re.search(pat, nl)
                if m:
                    r.aviso("LANG-001", f"{rel}:{n}: '{m.group(0)}' ({why})")
            if PASSIVA.search(nl):
                r.aviso("LANG-002", f"{rel}:{n}: voz passiva, nomeie o ator responsável")
    return r.emit(a.json)


if __name__ == "__main__":
    raise SystemExit(main())
