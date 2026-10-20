#!/usr/bin/env python3
"""Cria a estrutura .sdd/ a partir dos templates."""
import argparse
import shutil
import sys
from pathlib import Path

TPL = Path(__file__).resolve().parent.parent / "templates"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--destino", default=".")
    ap.add_argument("--nome", required=True)
    ap.add_argument("--modo", choices=["greenfield", "evolucao"], default="greenfield")
    ap.add_argument("--metodologia", choices=["scrum", "kanban"], default="scrum")
    ap.add_argument("--tamanho", choices=["pequeno", "medio", "grande", "indefinido"], default="indefinido")
    ap.add_argument("--equipe-tamanho", type=int, default=0)
    ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args()
    dest = Path(a.destino) / ".sdd"
    if dest.exists() and not a.forcar:
        sys.exit(f"{dest} já existe (use --forcar para sobrescrever arquivos de template).")
    subs = {"{{NOME}}": a.nome, "{{MODO}}": a.modo, "{{METODOLOGIA}}": a.metodologia, "{{TAMANHO}}": a.tamanho, "{{EQUIPE}}": str(a.equipe_tamanho)}
    skip = {"plano-kanban.md"} if a.metodologia == "scrum" else {"plano-scrum.md"}
    for src in (TPL / "sdd").rglob("*"):
        if src.is_dir() or src.name in skip:
            continue
        out = dest / src.relative_to(TPL / "sdd")
        out.parent.mkdir(parents=True, exist_ok=True)
        txt = src.read_text(encoding="utf-8")
        for k, v in subs.items():
            txt = txt.replace(k, v)
        out.write_text(txt, encoding="utf-8")
    (dest / "02-stack" / "adr").mkdir(parents=True, exist_ok=True)
    (dest / "04-design" / "diagramas").mkdir(parents=True, exist_ok=True)
    (dest / "07-export").mkdir(parents=True, exist_ok=True)
    if a.modo == "evolucao":
        for src in (TPL / "evolucao").rglob("*"):
            if src.is_file():
                out = dest / src.relative_to(TPL / "evolucao")
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, out)
    print(f"estrutura criada em {dest}. Próximo passo: /sdd-intake")


if __name__ == "__main__":
    main()
