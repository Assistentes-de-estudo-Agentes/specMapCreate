#!/usr/bin/env python3
"""Ranking transparente de ferramentas por camada, a partir de um pack de stack.
Exemplo:
  rank_stack.py --pack django --camada banco --pesos time_to_market=5,manutenibilidade=4,custo=3 \
      --selecionadas backend=django-drf --time-conhece postgres
"""
import argparse
import json
import sys
from pathlib import Path

from validate_stacks import validar

STACKS = Path(__file__).resolve().parent.parent / "stacks"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--camada", help="omita para listar as camadas do pack")
    ap.add_argument("--pesos", default="", help="criterio=peso(0-5),... (omitidos = 3)")
    ap.add_argument("--selecionadas", default="", help="camada=opcao,... já escolhidas (filtra compatibilidade)")
    ap.add_argument("--time-conhece", default="", help="ids de opções que o time domina (bônus)")
    ap.add_argument("--bonus", type=float, default=0.5, help="bônus por conhecimento do time (pontos na nota 0-5)")
    a = ap.parse_args()
    p = STACKS / a.pack / "pack.json"
    if not p.exists():
        disp = ", ".join(sorted(d.name for d in STACKS.iterdir() if (d / "pack.json").exists()))
        sys.exit(f"pack '{a.pack}' não existe. Disponíveis: {disp}")
    errors, warnings = validar(p)
    if errors:
        sys.exit("pack inválido; corrija antes de ranquear:\n- " + "\n- ".join(errors))
    pack = json.loads(p.read_text(encoding="utf-8"))
    crit = pack["criterios"]
    if warnings:
        print("Avisos do pack: " + "; ".join(warnings), file=sys.stderr)
    if not a.camada:
        print(f"Pack {pack['nome']} (revisado em {pack['revisado_em']}). Camadas: " + ", ".join(pack["camadas"]))
        return
    if a.camada not in pack["camadas"]:
        sys.exit(f"camada '{a.camada}' não existe. Use: {', '.join(pack['camadas'])}")
    pesos = {c: 3.0 for c in crit}
    for kv in filter(None, a.pesos.split(",")):
        try:
            k, v = kv.split("=", 1)
        except ValueError:
            sys.exit("--pesos deve usar formato criterio=peso,criterio=peso")
        if k not in pesos:
            sys.exit(f"critério '{k}' inválido. Use: {', '.join(crit)}")
        try:
            valor = float(v)
        except ValueError:
            sys.exit(f"peso inválido para '{k}': '{v}'")
        if not 0 <= valor <= 5:
            sys.exit(f"peso de '{k}' deve estar entre 0 e 5")
        pesos[k] = valor
    try:
        sel = dict(kv.split("=", 1) for kv in filter(None, a.selecionadas.split(",")))
    except ValueError:
        sys.exit("--selecionadas deve usar formato camada=opcao,camada=opcao")
    for camada_sel, opcao_sel in sel.items():
        if camada_sel not in pack["camadas"]:
            sys.exit(f"camada selecionada '{camada_sel}' não existe no pack")
        if opcao_sel not in {o["id"] for o in pack["camadas"][camada_sel]}:
            sys.exit(f"opção selecionada '{opcao_sel}' não existe na camada '{camada_sel}'")
    if not 0 <= a.bonus <= 5:
        sys.exit("--bonus deve estar entre 0 e 5")
    conhece = set(filter(None, a.time_conhece.split(",")))
    todos_ids = {o["id"] for camada in pack["camadas"].values() for o in camada}
    desconhecidos = conhece - todos_ids
    if desconhecidos:
        print("Aviso: IDs em --time-conhece não encontrados no pack: " + ", ".join(sorted(desconhecidos)), file=sys.stderr)
    total = sum(pesos.values()) or 1
    ok, bad = [], []
    pendencias_por_id = {}
    for o in pack["camadas"][a.camada]:
        motivos = []
        pendencias = []
        for req in o.get("requer", []):
            if req["camada"] not in sel and req["camada"] != a.camada:
                pendencias.append(f"depende de {req['camada']} em {req['ids']}")
            # Se uma camada requerida já foi escolhida, a incompatibilidade é conclusiva.
            # Se ainda não foi escolhida, a opção fica elegível, mas a dependência é explicitada.
            if req["camada"] in sel and sel[req["camada"]] not in req["ids"]:
                motivos.append(f"requer {req['camada']} em {req['ids']}, mas foi escolhido {sel[req['camada']]}")
        for c in o.get("conflita", []):
            if c in sel.values():
                motivos.append(f"conflita com {c}")
        motivo = "; ".join(motivos) if motivos else None
        nota = sum(s * pesos[k] for s, k in zip(o["notas"], crit)) / total
        if o["id"] in conhece:
            nota = min(5.0, nota + a.bonus)
        pendencias_por_id[o["id"]] = pendencias
        (bad if motivo else ok).append((nota, o, motivo))
    ok.sort(key=lambda x: -x[0])
    print(f"Camada: {a.camada} | pesos: " + ", ".join(f"{k}={v:g}" for k, v in pesos.items()))
    print(f"(notas 0-5 são um ponto de partida curado em {pack['revisado_em']}; confirme versões e contexto antes de decidir)\n")
    for n, (nota, o, _) in enumerate(ok):
        tag = "★ RECOMENDADO" if n == 0 else "○ Alternativa "
        conh = " [time conhece]" if o["id"] in conhece else ""
        print(f"{tag} {o['nome']} (id: {o['id']})  aderência {nota * 2:.1f}/10{conh}")
        print(f"    + {o['pros']}\n    - {o['contras']}")
        if o.get("nota"):
            print(f"    ! {o['nota']}")
        for pendencia in pendencias_por_id.get(o["id"], []):
            print(f"    ? Compatibilidade ainda não confirmada: {pendencia}")
    for nota, o, motivo in bad:
        print(f"⚠ Incompatível  {o['nome']} (id: {o['id']}): {motivo}")


if __name__ == "__main__":
    main()
