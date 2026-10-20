#!/usr/bin/env python3
"""Executa os validadores de um gate (0-7). Uso: run_all.py --gate 3 [--sdd .sdd]"""
import subprocess
import sys
from pathlib import Path

GATES = {
    0: ["validate_state"],
    1: ["validate_state", "validate_discovery"],
    2: ["validate_state", "validate_discovery", "validate_stacks"],
    3: ["validate_state", "validate_discovery", "validate_stacks", "validate_spec", "lint_language", "check_sizing", "validate_stale"],
    4: ["validate_state", "validate_discovery", "validate_stacks", "validate_spec", "lint_language", "check_sizing", "validate_diagrams", "validate_stale"],
    5: ["validate_state", "validate_discovery", "validate_stacks", "validate_spec", "validate_tasks", "graph_deps", "lint_language", "validate_diagrams", "validate_stale"],
    6: ["validate_state", "validate_discovery", "validate_stacks", "validate_spec", "validate_tasks", "graph_deps", "validate_diagrams", "validate_traceability", "validate_stale"],
    7: ["validate_state", "validate_discovery", "validate_stacks", "validate_spec", "validate_tasks", "graph_deps", "validate_diagrams", "validate_traceability", "validate_stale", "validate_export"],
}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", type=int, required=True, choices=sorted(GATES))
    ap.add_argument("--sdd", default=".sdd")
    a = ap.parse_args()
    here = Path(__file__).parent
    rc = 0
    for name in GATES[a.gate]:
        cmd = [sys.executable, str(here / f"{name}.py")]
        if name != "validate_stacks":
            cmd += ["--sdd", a.sdd]
        if name in ("validate_state", "validate_discovery"):
            cmd += ["--gate", str(a.gate)]
        p = subprocess.run(cmd)
        rc |= p.returncode
    print("\n>>> GATE", a.gate, "APROVADO pelos validadores" if rc == 0 else "REPROVADO: corrija os erros acima")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
