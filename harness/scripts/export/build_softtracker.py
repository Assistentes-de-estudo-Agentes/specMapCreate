#!/usr/bin/env python3
"""Exporta os dois contratos YAML consumidos pelo SoftTracker.

Gera <pasta-do-projeto>/softtracker/spec.yaml e especificacao.yml a partir
 de .sdd/03-requisitos/spec.md, .sdd/05-planejamento/tasks.md e project.yaml.
Não cria requisitos nem critérios que não existam nas fontes.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sddlib import load_project, parse_spec, parse_tasks, read, SPEC, TASKS


def dump_yaml(data):
    if yaml:
        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110)
    # JSON é um subconjunto válido de YAML 1.2; mantém exportação sem dependências.
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def clean_story(s):
    return s.get("fields", {}).get("historia", "").replace("**", "").strip()


def task_dod(t):
    out = []
    in_dod = False
    for line in t.get("lines", []):
        if re.match(r"\s*[-*]\s+\*\*Definition of Done:?\*\*", line, re.I):
            in_dod = True
            continue
        if in_dod:
            m = re.match(r"\s*[-*]\s+\[[ xX]\]\s*(.+)", line)
            if m:
                out.append(m.group(1).strip())
            elif line.strip() and not line.startswith((" ", "\t")):
                in_dod = False
    return out


def criteria_for(t):
    """Critérios derivados somente da descrição e DoD explícitos da task."""
    criteria = []
    desc = t.get("fields", {}).get("descricao", "").strip()
    if desc:
        criteria.append({"id": "C1", "descricao": desc, "origem": "descricao_da_task"})
    for i, item in enumerate(task_dod(t), 2 if desc else 1):
        criteria.append({"id": f"C{i}", "descricao": item, "origem": "definition_of_done"})
    return criteria


def order_tasks(tasks):
    by_id = {t["id"]: t for t in tasks}
    pending, result, done = list(tasks), [], set()
    while pending:
        ready = [t for t in pending if all(d not in by_id or d in done for d in t["depende"])]
        if not ready:  # mantém visíveis tarefas com ciclo, sem ocultá-las
            result.extend(pending)
            break
        for t in ready:
            result.append(t); done.add(t["id"]); pending.remove(t)
    return result


def main():
    ap = argparse.ArgumentParser(description="Gera spec.yaml e especificacao.yml para o SoftTracker")
    ap.add_argument("--sdd", default=".sdd", help="pasta .sdd do projeto")
    ap.add_argument("--saida", default="softtracker", help="pasta de saída (padrão: softtracker)")
    a = ap.parse_args()
    sdd = Path(a.sdd)
    if not sdd.exists():
        sys.exit(f"Pasta SDD não encontrada: {sdd}")
    project = load_project(sdd)
    spec = parse_spec(read(sdd / SPEC))
    tasks = parse_tasks(read(sdd / TASKS))
    out_dir = Path(a.saida)
    out_dir.mkdir(parents=True, exist_ok=True)

    stories = spec["stories"]
    story_to_uc = {s["id"]: f"UC{i:03d}" for i, s in enumerate(stories, 1)}
    task_to_story = {}
    for t in tasks:
        refs = [r for r in t["refs"] if r in story_to_uc]
        task_to_story[t["id"]] = refs[0] if refs else None

    # Formato compacto de integração: projeto/stack/requisitos/casos de uso/UML/tasks.
    stack_items = []
    for layer, value in (project.get("stack") or {}).items():
        stack_items.append({"camada": str(layer).replace("_", " ").title(),
                            "itens": [{"nome": str(value), "uso": "Stack declarada no projeto"}]})
    requisitos = [{"id": i, "titulo": title, "tipo": "funcional"} for i, title in spec["rf"]]
    requisitos.extend({"id": i, "titulo": title, "tipo": "nao_funcional"}
                      for i, title in spec["rnf"])
    requisitos_ids = {item["id"] for item in requisitos}
    casos = []
    for i, s in enumerate(stories, 1):
        f = s["fields"]
        refs = [rid for rid in re.findall(r"RF\d{3}|RNF\d{3}",
                f.get("requisitos", "") + " " + f.get("requisito", "") + " " + f.get("nfr relacionados", ""))
                if rid in requisitos_ids]
        casos.append({"id": story_to_uc[s["id"]], "titulo": s["title"], "historia_id": s["id"],
                      "requisitos": list(dict.fromkeys(refs)),
                      "criterios_aceitacao": [{"id": ac["id"], "descricao": ac["text"], "tipo": ac["tipo"]} for ac in s["acs"]]})
    uml = []
    design = read(sdd / "04-design/design.md")
    for cls in dict.fromkeys(re.findall(r"(?m)^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)", design)):
        related = [t["id"] for t in tasks if cls.lower() in (t["title"] + " " + t["text"]).lower()]
        uml.append({"id": "UML-" + cls, "tipo": "classe", "elemento": cls, "tasks": related})
    compact_tasks = []
    for t in tasks:
        criteria = criteria_for(t)
        compact_tasks.append({"id": t["id"], "titulo": t["title"],
                              "caso_de_uso": story_to_uc.get(task_to_story[t["id"]]) if task_to_story[t["id"]] else None,
                              "depende_de": t["depende"], "criterios": [
                                  # Não inventa símbolos/rotas/classes a partir de texto livre.
                                  # O SoftTracker aceita critérios sem artefato determinístico e
                                  # os encaminha para análise semântica, sem erro de schema.
                                  {"id": c["id"], "descricao": c["descricao"], "usar_ia": True}
                                  for c in criteria]})
    compact = {"projeto": project.get("nome", "Projeto"),
               "ignorar": ["*.md", "tests/**", "migrations/**"],
               "stack": stack_items, "requisitos": requisitos, "casos_de_uso": casos,
               "uml": uml, "tasks": compact_tasks}

    # Formato detalhado: mantém RF/RNF, histórias/ACs e tarefas com dependências.
    rf_details = [{"id": i, "descricao": title} for i, title in spec["rf"]]
    rnf_details = [{"id": i, "descricao": title} for i, title in spec["rnf"]]
    requisitos_detalhados_ids = {item["id"] for item in rf_details + rnf_details}
    use_cases = []
    for i, s in enumerate(stories, 1):
        f = s["fields"]
        use_cases.append({"id": story_to_uc[s["id"]], "nome": s["title"],
                          "historia_id": s["id"], "ator": re.search(r"Como\s+(.+?),\s+quero", clean_story(s), re.I).group(1) if re.search(r"Como\s+(.+?),\s+quero", clean_story(s), re.I) else "",
                          "requisitos": [rid for rid in re.findall(
                              r"RF\d{3}|RNF\d{3}", f.get("requisitos", "") + " " +
                              f.get("requisito", "") + " " + f.get("nfr relacionados", ""))
                              if rid in requisitos_detalhados_ids],
                          "historia": clean_story(s),
                          "prioridade": f.get("prioridade", ""), "mvp": f.get("mvp", ""),
                          "criterios_aceitacao": [{"id": ac["id"], "tipo": ac["tipo"], "descricao": ac["text"]} for ac in s["acs"]]})
    development_tasks = []
    canonical_tasks = []
    for t in order_tasks(tasks):
        linked_story = task_to_story[t["id"]]
        development_tasks.append({"id": t["id"], "descricao": t["title"],
                                  "detalhes": t.get("fields", {}).get("descricao", ""),
                                  "relacionado_a": [story_to_uc[linked_story]] if linked_story else [],
                                  "status": "nao_especificado"})
        canonical_tasks.append({"id": t["id"], "titulo": t["title"],
                                "descricao": t.get("fields", {}).get("descricao", ""),
                                "caso_de_uso": story_to_uc.get(linked_story) if linked_story else None,
                                "refs": t["refs"], "depende_de": t["depende"],
                                "tipo": t["tipo"], "estimativa": t["est"],
                                "criterios": criteria_for(t), "casos_de_teste": t["cts"]})
    detailed = {"projeto": {"nome": project.get("nome", "Projeto"),
                            "descricao": project.get("descricao", ""),
                            "objetivo": project.get("objetivo", ""),
                            "stack": project.get("stack", {})},
                "requisitos_funcionais": rf_details,
                "requisitos_nao_funcionais": rnf_details,
                "regras_de_negocio": [{"id": i, "descricao": title} for i, title in spec["rn"]],
                "casos_de_uso": use_cases,
                "tarefas_desenvolvimento": development_tasks,
                "tasks": canonical_tasks,
                "ordem_implementacao": {"requisitos_funcionais": [x["id"] for x in rf_details],
                                        "casos_de_uso": [x["id"] for x in use_cases],
                                        "tasks": [x["id"] for x in canonical_tasks]}}
    (out_dir / "spec.yaml").write_text(dump_yaml(compact), encoding="utf-8")
    (out_dir / "especificacao.yml").write_text(dump_yaml(detailed), encoding="utf-8")
    print(f"SoftTracker exportado: {out_dir / 'spec.yaml'} e {out_dir / 'especificacao.yml'}")
    print(f"{len(spec['rf'])} RF, {len(spec['rnf'])} RNF, {len(stories)} US/casos de uso, {len(tasks)} tasks")

if __name__ == "__main__":
    main()
