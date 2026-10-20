#!/usr/bin/env python3
"""Gate da Fase 4: valida diagramas Mermaid (.mmd)."""
import re
import shutil
import subprocess
import tempfile
from sddlib import *

TIPOS = ("flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram-v2", "stateDiagram",
         "erDiagram", "C4Context", "C4Container", "C4Component", "journey", "gantt")


def main():
    a = std_args("Valida diagramas").parse_args()
    sdd = get_sdd(a.sdd)
    r = Report("validate_diagrams")
    proj = load_project(sdd)
    files = sorted((sdd / "04-design" / "diagramas").glob("*.mmd")) if (sdd / "04-design" / "diagramas").exists() else []
    if not files:
        (r.erro if proj.get("tamanho") in ("medio", "grande") else r.aviso)("DIAG-000", "nenhum diagrama em 04-design/diagramas/")
        return r.emit(a.json)
    spec = parse_spec(read(sdd / SPEC))
    valid = {s["id"] for s in spec["stories"]} | {e["id"] for e in spec["epics"]} | {i for i, _ in spec["rn"]}
    mmdc = shutil.which("mmdc")
    for f in files:
        txt = f.read_text(encoding="utf-8")
        body = [l for l in txt.split("\n") if l.strip() and not l.strip().startswith("%%")]
        if not body or not body[0].strip().startswith(TIPOS):
            r.erro("DIAG-001", f"{f.name}: tipo de diagrama não reconhecido na primeira linha")
        m = re.search(r"^%%\s*refs:\s*(.+)$", txt, re.M)
        if not m:
            r.erro("DIAG-002", f"{f.name}: falta '%% refs: US001, US002'")
        else:
            for ref in re.findall(r"[A-Z]+\d{3}", m.group(1)):
                if ref not in valid:
                    r.erro("DIAG-003", f"{f.name}: ref {ref} não existe na spec")
        sem_rel = re.sub(r"[|o}{]+(?:--|\.\.)[|o}{]+", "", txt)
        for o, c in ("()", "[]", "{}"):
            if sem_rel.count(o) != sem_rel.count(c):
                r.erro("DIAG-004", f"{f.name}: delimitadores '{o}{c}' desbalanceados")
        if mmdc:
            with tempfile.TemporaryDirectory() as d:
                p = subprocess.run([mmdc, "-i", str(f), "-o", f"{d}/o.svg"], capture_output=True, text=True)
                if p.returncode != 0 and re.search(r"chrome|puppeteer|browser", p.stderr, re.I):
                    r.aviso("DIAG-006", f"{f.name}: mmdc sem navegador disponível; validação de sintaxe pulada")
                elif p.returncode != 0:
                    r.erro("DIAG-005", f"{f.name}: mmdc falhou: {p.stderr.strip()[:200]}")
    if not mmdc:
        r.info("DIAG-100", "mmdc não instalado: validação apenas estrutural (npm i -g @mermaid-js/mermaid-cli para validar a sintaxe completa)")
    return r.emit(a.json)


if __name__ == "__main__":
    raise SystemExit(main())
