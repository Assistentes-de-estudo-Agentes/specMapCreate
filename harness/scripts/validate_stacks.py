#!/usr/bin/env python3
"""Valida estrutura, notas e referências internas dos packs tecnológicos.

Não tenta provar que uma tecnologia é a melhor; verifica se os dados usados
pelo Stack Advisor são consistentes e seguros para ranqueamento.
"""
import argparse
import datetime
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "stacks"
CRITERIOS_PADRAO = ["time_to_market", "custo", "escala", "conhecimento_time", "seguranca", "manutenibilidade", "ecossistema"]
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def validar(path):
    errors, warnings = [], []
    try:
        p = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"JSON inválido: {e}"], []
    for key in ("nome", "descricao", "revisado_em", "criterios", "camadas"):
        if key not in p:
            errors.append(f"campo obrigatório ausente: {key}")
    criterios = p.get("criterios", [])
    if criterios != CRITERIOS_PADRAO:
        errors.append(f"criterios deve seguir a ordem contratual: {', '.join(CRITERIOS_PADRAO)}")
    camadas = p.get("camadas", {})
    if not isinstance(camadas, dict) or not camadas:
        errors.append("camadas deve ser um objeto não vazio")
        camadas = {}
    ids_por_camada = {}
    for camada, opcoes in camadas.items():
        if not isinstance(opcoes, list) or not opcoes:
            errors.append(f"camada '{camada}' deve conter uma lista não vazia de opções")
            continue
        ids = set()
        for idx, o in enumerate(opcoes):
            label = f"{camada}[{idx}]"
            if not isinstance(o, dict):
                errors.append(f"{label}: opção deve ser objeto")
                continue
            oid = o.get("id", "")
            if not ID_RE.match(str(oid)):
                errors.append(f"{label}: id inválido '{oid}' (use minúsculas, números e hífens)")
            if oid in ids:
                errors.append(f"{label}: id duplicado '{oid}' na camada")
            ids.add(oid)
            for key in ("nome", "pros", "contras"):
                if not isinstance(o.get(key), str) or not o[key].strip():
                    errors.append(f"{label}/{oid}: campo '{key}' obrigatório")
            notas = o.get("notas")
            if not isinstance(notas, list) or len(notas) != len(criterios):
                errors.append(f"{label}/{oid}: notas deve ter {len(criterios)} números, na ordem de criterios")
            elif any(not isinstance(n, (int, float)) or isinstance(n, bool) or n < 0 or n > 5 for n in notas):
                errors.append(f"{label}/{oid}: cada nota deve ser numérica e estar entre 0 e 5")
            for req in o.get("requer", []):
                if not isinstance(req, dict) or not req.get("camada") or not isinstance(req.get("ids"), list) or not req["ids"]:
                    errors.append(f"{label}/{oid}: cada requer deve ter camada e ids não vazios")
                elif req["camada"] not in camadas:
                    errors.append(f"{label}/{oid}: requer camada inexistente '{req['camada']}'")
                else:
                    available = {x.get("id") for x in camadas[req["camada"]] if isinstance(x, dict)}
                    for rid in req["ids"]:
                        if rid not in available:
                            errors.append(f"{label}/{oid}: requer opção inexistente '{rid}' na camada '{req['camada']}'")
            for conflict in o.get("conflita", []):
                if not isinstance(conflict, str) or not conflict:
                    errors.append(f"{label}/{oid}: conflito deve ser um ID de opção")
                elif conflict == oid:
                    errors.append(f"{label}/{oid}: uma opção não pode conflitar consigo mesma")
        ids_por_camada[camada] = ids
    for camada, opcoes in camadas.items():
        for o in opcoes if isinstance(opcoes, list) else []:
            if not isinstance(o, dict):
                continue
            for conflict in o.get("conflita", []):
                known = any(conflict in ids for ids in ids_por_camada.values())
                if not known:
                    errors.append(f"{camada}/{o.get('id')}: conflita com opção inexistente '{conflict}'")
    for key in ("tasks_fundacao", "nfr_comuns", "anti_padroes"):
        if key in p and not isinstance(p[key], list):
            errors.append(f"'{key}' deve ser lista")
    revisado = str(p.get("revisado_em", "")).strip()
    if not revisado or revisado == "AAAA-MM-DD":
        warnings.append("data de revisão ausente/placeholder; confiança nas recomendações deve ser baixa")
    else:
        try:
            data = datetime.date.fromisoformat(revisado)
            idade = (datetime.date.today() - data).days
            if idade < 0:
                warnings.append("data de revisão está no futuro; confirme o relógio e o valor")
            elif idade > 180:
                warnings.append(f"pack sem revisão há {idade} dias; verifique se ferramentas e suporte continuam atuais")
        except ValueError:
            errors.append("revisado_em deve usar formato ISO AAAA-MM-DD")
    if p.get("confianca", "curada") not in ("alta", "media", "média", "baixa", "curada"):
        warnings.append("valor de confiança não padronizado")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pack", help="nome de um pack; por padrão valida todos")
    ap.add_argument("--arquivo", help="caminho direto para um pack.json, útil para testes")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    paths = [Path(a.arquivo)] if a.arquivo else ([ROOT / a.pack / "pack.json"] if a.pack else sorted(ROOT.glob("*/pack.json")))
    if not paths or any(not p.exists() for p in paths):
        raise SystemExit(f"Pack não encontrado. Disponíveis: {', '.join(p.parent.name for p in ROOT.glob('*/pack.json'))}")
    result = []
    for path in paths:
        errors, warnings = validar(path)
        result.append({"pack": path.parent.name, "erros": errors, "avisos": warnings})
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result:
            print(f"[{ 'ERRO' if item['erros'] else 'OK' }] {item['pack']}")
            for msg in item["erros"]:
                print(f"  ERRO: {msg}")
            for msg in item["avisos"]:
                print(f"  AVISO: {msg}")
        print(f"Resumo: {sum(len(x['erros']) for x in result)} erro(s), {sum(len(x['avisos']) for x in result)} aviso(s), {len(result)} pack(s)")
    return 1 if any(x["erros"] for x in result) else 0

if __name__ == "__main__":
    raise SystemExit(main())
