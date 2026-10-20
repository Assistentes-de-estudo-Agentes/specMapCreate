#!/usr/bin/env python3
"""Detecta ciclos de dependência e calcula o caminho crítico."""
from sddlib import *


def main():
    ap = std_args("Grafo de dependências")
    a = ap.parse_args()
    sdd = get_sdd(a.sdd)
    r = Report("graph_deps")
    tasks = {t["id"]: t for t in parse_tasks(read(sdd / TASKS))}
    if not tasks:
        r.erro("GRAPH-000", "sem tasks")
        return r.emit(a.json)
    deps = {i: [d for d in t["depende"] if d in tasks] for i, t in tasks.items()}
    state, cycle = {}, []

    def dfs(n, path):
        state[n] = 1
        for d in deps[n]:
            if state.get(d) == 1:
                cycle.extend(path[path.index(d):] + [n, d] if d in path else [n, d])
                return True
            if d not in state and dfs(d, path + [n]):
                return True
        state[n] = 2
        return False

    for n in tasks:
        if n not in state and dfs(n, []):
            break
    if cycle:
        r.erro("GRAPH-001", "ciclo de dependência: " + " -> ".join(cycle))
        return r.emit(a.json)
    memo = {}

    def longest(n):
        if n not in memo:
            best = max((longest(d) for d in deps[n]), key=lambda x: x[0], default=(0, []))
            memo[n] = (best[0] + (tasks[n]["est"] or 0), best[1] + [n])
        return memo[n]

    total, path = max((longest(n) for n in tasks), key=lambda x: x[0])
    r.info("GRAPH-100", f"caminho crítico ({total:g} pts/dias): " + " -> ".join(path))
    dependidos = {d for ds in deps.values() for d in ds}
    folhas = [n for n in tasks if n not in dependidos]
    r.info("GRAPH-101", f"{len(tasks)} tasks, {len(folhas)} sem dependentes (entregas finais ou candidatas a revisão)")
    return r.emit(a.json)


if __name__ == "__main__":
    raise SystemExit(main())
