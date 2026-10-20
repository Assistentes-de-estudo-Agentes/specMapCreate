#!/usr/bin/env python3
"""Gera a documentação final a partir do .sdd/: especificação consolidada, catálogo de
casos de uso e diagramas em Markdown, mais HTML e PDF (opcionais, se houver ferramentas).

Uso: build_docs.py [--sdd .sdd] [--formatos md,html,pdf] [--saida .sdd/08-docs]
Somente biblioteca padrão. Para diagramas renderizados e PDF: mmdc e Chrome/Chromium
(ou wkhtmltopdf como alternativa para o PDF). Sem eles, os .md continuam sendo gerados."""
import argparse
import base64
import datetime
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from sddlib import *


# ------------------------------------------------------------------ utilidades de texto
def strip_comments(text):
    _, body = split_front(text)
    return re.sub(r"<!--.*?-->", "", body, flags=re.S)


def has_content(text):
    """True se o arquivo tem algo além de títulos, tabelas vazias e orientações do template."""
    n, tab = 0, 0
    for l in strip_comments(text).split("\n"):
        s = l.strip()
        if not s:
            tab = 0
            continue
        if s.startswith("|"):
            tab += 1
            if tab > 2 and re.search(r"[^|\s\-:]", s):
                n += 1
            continue
        tab = 0
        if s.startswith("#") or re.match(r"^_\(.*\)_$", s) or re.match(r"^[-*]\s+\*\*[^*]+\*\*:?\s*$", s):
            continue
        n += 1
    return n > 0


def include(md, base, drop_h1=False):
    """Reaproveita um .md ajustando os níveis de título (H1 -> base, ou H2 -> base se drop_h1)."""
    shift = base - (2 if drop_h1 else 1)
    out, fence, first = [], False, True
    for l in strip_comments(md).split("\n"):
        if l.lstrip().startswith("```"):
            fence = not fence
        elif not fence:
            m = re.match(r"^(#{1,6})\s+(.*)$", l)
            if m:
                if len(m.group(1)) == 1 and first and drop_h1:
                    first = False
                    continue
                first = False
                l = "#" * min(6, len(m.group(1)) + shift) + " " + m.group(2)
        out.append(l)
    return "\n".join(out).strip()


def cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ").strip() or "—"


def table(head, rows):
    if not rows:
        return ""
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(cell(c) if not c.startswith("\0") else c[1:] for c in r) + " |" for r in rows]
    return "\n".join(out)


def slug(t):
    return re.sub(r"[^\w\- ]", "", t.lower()).strip().replace(" ", "-")


def split_hist(h):
    h = h.replace("*", "")
    m = re.match(r"(?is)^como\s+(.+?),?\s+quero\s+(.+?)\s+para\s+(.+?)\.?$", h)
    return m.groups() if m else ("", h, "")


def parse_bdd(text):
    m = re.search(r"(?is)dado que\s+(.*?)\s+quando\s+(.*?)\s+(?:então|entao)\s+(.*)$", text)
    return m.groups() if m else None


# ------------------------------------------------------------------ Mermaid -> SVG
def find_chrome():
    for env in ("CHROME_PATH", "PUPPETEER_EXECUTABLE_PATH"):
        if os.environ.get(env) and Path(os.environ[env]).exists():
            return os.environ[env]
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(n)
        if p:
            return p
    for p in ("/opt/google/chrome/chrome", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
        if Path(p).exists():
            return p
    return None


class Renderer:
    def __init__(self, enabled=True):
        self.mmdc = shutil.which("mmdc") if enabled else None
        self.chrome = find_chrome()
        self.cache, self.tmp, self.failed = {}, tempfile.mkdtemp(prefix="sddmmd"), 0
        if self.mmdc:
            cfg = {"executablePath": self.chrome} if self.chrome else {}
            cfg["args"] = ["--no-sandbox", "--disable-gpu"]
            Path(self.tmp, "pp.json").write_text(json.dumps(cfg))
            Path(self.tmp, "mm.json").write_text(json.dumps({"htmlLabels": False, "flowchart": {"htmlLabels": False}}))

    def svg(self, code):
        """Retorna o SVG como texto, ou None se não foi possível renderizar."""
        if not self.mmdc:
            return None
        key = hashlib.sha1(code.encode()).hexdigest()[:12]
        if key in self.cache:
            return self.cache[key]
        src, dst = Path(self.tmp, key + ".mmd"), Path(self.tmp, key + ".svg")
        src.write_text(code, encoding="utf-8")
        try:
            p = subprocess.run([self.mmdc, "-i", str(src), "-o", str(dst), "-p", str(Path(self.tmp, "pp.json")),
                                "-c", str(Path(self.tmp, "mm.json")), "-b", "transparent"],
                               capture_output=True, text=True, timeout=120)
            ok = p.returncode == 0 and dst.exists()
        except (subprocess.TimeoutExpired, OSError):
            ok = False
        self.cache[key] = dst.read_text(encoding="utf-8") if ok else None
        if not ok:
            self.failed += 1
        return self.cache[key]

    def html(self, code):
        svg = self.svg(code)
        if svg:
            uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()
            return f'<div class="diagrama"><img src="{uri}" alt="diagrama"></div>'
        return ('<div class="diagrama-fonte"><p class="aviso">Diagrama não renderizado (instale mmdc e Chrome). Código Mermaid:</p>'
                f"<pre><code>{html.escape(code)}</code></pre></div>")


# ------------------------------------------------------------------ Markdown -> HTML (mínimo)
def inline(s):
    s = html.escape(s, quote=False).replace("&lt;br&gt;", "<br>")
    codes = []
    s = re.sub(r"`([^`]+)`", lambda m: (codes.append(m.group(1)) or f"\0{len(codes) - 1}\0"), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return re.sub(r"\0(\d+)\0", lambda m: f"<code>{codes[int(m.group(1))]}</code>", s)


LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")


def _render_list(items, k, indent):
    tag = "ol" if items[k][1] else "ul"
    out = [f"<{tag}>"]
    while k < len(items) and items[k][0] >= indent:
        if items[k][0] > indent:
            sub, k = _render_list(items, k, items[k][0])
            if len(out) > 1:
                out[-1] = out[-1][:-5] + sub + "</li>"
            else:
                out.append(sub)
            continue
        t = re.sub(r"^\[ \]", "☐", items[k][2])
        t = re.sub(r"^\[[xX]\]", "☑", t)
        out.append(f"<li>{inline(t)}</li>")
        k += 1
    out.append(f"</{tag}>")
    return "".join(out), k


def _is_block_start(l, nxt):
    s = l.lstrip()
    return (not s or s.startswith(("```", "#", ">")) or LIST_RE.match(l) or
            (s.startswith("|") and nxt is not None and re.match(r"^\s*\|[\s:\-|]+\|?\s*$", nxt)))


def md_to_html(md, rend):
    lines, i, out, toc, seen = md.split("\n"), 0, [], [], {}
    while i < len(lines):
        l = lines[i]
        nxt = lines[i + 1] if i + 1 < len(lines) else None
        if l.lstrip().startswith("```"):
            lang, buf = l.strip()[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].lstrip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            code = "\n".join(buf)
            out.append(rend.html(code) if lang == "mermaid" else f"<pre><code>{html.escape(code)}</code></pre>")
        elif re.match(r"^#{1,6}\s", l):
            m = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", l)
            lvl, txt = len(m.group(1)), m.group(2)
            sid = slug(txt)
            seen[sid] = seen.get(sid, 0) + 1
            sid = sid if seen[sid] == 1 else f"{sid}-{seen[sid] - 1}"
            toc.append((lvl, txt, sid))
            out.append(f'<h{lvl} id="{sid}">{inline(txt)}</h{lvl}>')
            i += 1
        elif re.match(r"^\s*([-*_])(\s*\1){2,}\s*$", l):
            out.append("<hr>")
            i += 1
        elif l.lstrip().startswith("|") and nxt is not None and re.match(r"^\s*\|[\s:\-|]+\|?\s*$", nxt):
            def cells(r):
                r = r.strip().replace("\\|", "\0")
                r = r[1:] if r.startswith("|") else r
                r = r[:-1] if r.endswith("|") else r
                return [c.replace("\0", "|").strip() for c in r.split("|")]
            head = cells(l)
            i += 2
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            t = "<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            for r in rows:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</tbody></table>")
        elif l.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> ").rstrip())
                i += 1
            out.append("<blockquote>" + inline(" ".join(buf)) + "</blockquote>")
        elif LIST_RE.match(l):
            items = []
            while i < len(lines):
                m = LIST_RE.match(lines[i])
                if m:
                    items.append([len(m.group(1)), m.group(2)[0].isdigit(), m.group(3)])
                    i += 1
                elif lines[i].strip() and lines[i].startswith("  ") and items:
                    items[-1][2] += " " + lines[i].strip()
                    i += 1
                else:
                    break
            out.append(_render_list(items, 0, items[0][0])[0])
        elif not l.strip():
            i += 1
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not (buf and _is_block_start(lines[i], lines[i + 1] if i + 1 < len(lines) else None)):
                buf.append(lines[i].strip())
                i += 1
            out.append("<p>" + inline(" ".join(buf)) + "</p>")
    return "\n".join(out), toc


CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; @bottom-center { content: counter(page) " / " counter(pages); font-size: 9pt; color: #666; } }
:root { color-scheme: light; }
body { font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 10.5pt; line-height: 1.5; color: #1a1a1a; max-width: 980px; margin: 0 auto; padding: 16px; }
h1 { font-size: 22pt; margin: 0 0 6px; } h2 { font-size: 16pt; border-bottom: 2px solid #2b5fab; padding-bottom: 4px; margin-top: 28px; page-break-before: always; color: #17325c; }
h3 { font-size: 13pt; margin-top: 22px; color: #17325c; } h4 { font-size: 11.5pt; margin-top: 16px; } h5, h6 { font-size: 10.5pt; }
h2, h3, h4 { page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9.5pt; page-break-inside: auto; } tr { page-break-inside: avoid; }
th, td { border: 1px solid #c9d1dc; padding: 5px 8px; text-align: left; vertical-align: top; } th { background: #eef3fa; }
code { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 9pt; background: #f2f4f7; padding: 1px 4px; border-radius: 3px; }
pre { background: #f6f8fa; border: 1px solid #dde3ea; padding: 10px; overflow: auto; white-space: pre-wrap; page-break-inside: avoid; } pre code { background: none; padding: 0; }
blockquote { border-left: 4px solid #2b5fab; margin: 10px 0; padding: 4px 14px; background: #f5f8fd; }
.diagrama { text-align: center; margin: 12px 0; page-break-inside: avoid; } .diagrama img { max-width: 100%; max-height: 230mm; }
.aviso { color: #8a5a00; font-style: italic; }
.capa { min-height: 200mm; page-break-after: always; display: flex; flex-direction: column; justify-content: center; } .capa .sub { font-size: 14pt; color: #555; margin-bottom: 28px; }
.rascunho { color: #b00020; font-weight: bold; } .ok { color: #1b7f3b; font-weight: bold; }
.toc { page-break-after: always; } .toc a { text-decoration: none; color: #17325c; } .toc ul { list-style: none; padding-left: 16px; } .toc > ul { padding-left: 0; }
@media print { body { max-width: none; padding: 0; } }
"""


# ------------------------------------------------------------------ conteúdo
def diag_title(stem, code):
    first = next((l.strip() for l in code.split("\n") if l.strip() and not l.strip().startswith("%%")), "")
    tipo = ("Modelo ER" if first.startswith("erDiagram") else "Sequência" if first.startswith("sequenceDiagram") else
            "Classes" if first.startswith("classDiagram") else "Estados" if first.startswith("stateDiagram") else
            "Componentes (C4)" if first.startswith("C4") else "Fluxo")
    rest = re.sub(r"^(er|sequencia|estados?|classes|casos-de-uso|componentes|atividade|implantacao)[-_]?", "", stem)
    if stem.startswith("casos-de-uso"):
        tipo = "Casos de uso"
    return tipo + (": " + rest.replace("-", " ").replace("_", " ") if rest else "")


def auto_use_case_diagram(spec, nome):
    actors, L = {}, ["flowchart LR", "%% refs: " + ", ".join(s["id"] for s in spec["stories"])]
    uc_lines = {}
    for s in spec["stories"]:
        ator = split_hist(s["fields"].get("historia", ""))[0].strip().capitalize() or "Usuário"
        actors.setdefault(ator, f"A{len(actors) + 1}")
        ep = (re.findall(r"EP\d{3}", s["fields"].get("epico", "")) or ["EP000"])[0]
        uc_lines.setdefault(ep, []).append((s, ator))
    for ator, aid in actors.items():
        L.append(f'    {aid}(["{ator}"])')
    titles = {e["id"]: e["title"] for e in spec["epics"]}
    for ep, items in uc_lines.items():
        L.append(f'    subgraph {ep}["{titles.get(ep, ep).replace(chr(34), "")}"]')
        for s, ator in items:
            L.append(f'        UC_{s["id"]}(("{s["id"]} {s["title"].replace(chr(34), "")}"))')
        L.append("    end")
    for ep, items in uc_lines.items():
        for s, ator in items:
            L.append(f"    {actors[ator]} --> UC_{s['id']}")
    return "\n".join(L) + "\n"


def uc_md(spec, nome, lvl, uc_code):
    h = "#" * lvl
    out = [f"{h} Catálogo de casos de uso", "",
           "Cada user story é detalhada como caso de uso: pré-condições e fluxo principal vêm dos critérios BDD; "
           "exceções vêm dos critérios EARS. Gerado automaticamente a partir da especificação.", ""]
    by_actor = {}
    cases = []
    for n, s in enumerate(spec["stories"], 1):
        f = s["fields"]
        ator, acao, objetivo = split_hist(f.get("historia", ""))
        ator = ator.strip().capitalize() or "Usuário"
        bdd = [(a, parse_bdd(a["text"])) for a in s["acs"] if a["tipo"] == "BDD"]
        ears = [a for a in s["acs"] if a["tipo"] == "EARS"]
        pre = [b[0] for _, b in bdd if b]
        fluxo = [f"**{a['id']}** Quando {b[1]} → Então {b[2]}" for a, b in bdd if b]
        pos = [b[2] for _, b in bdd if b]
        rn_ids = re.findall(r"RN\d{3}", f.get("regras de negocio", ""))
        rn = dict(spec["rn"])
        rows = [("Ator primário", ator), ("Objetivo", f"{acao} para {objetivo}".strip()),
                ("Prioridade / MVP", f"{f.get('prioridade', '')} / {f.get('mvp', '')}"),
                ("Pré-condições", "<br>".join(dict.fromkeys(pre))), ("Fluxo principal", "<br>".join(fluxo)),
                ("Fluxos alternativos e exceções", "<br>".join(f"**{a['id']}** {a['text']}" for a in ears)),
                ("Pós-condições", "<br>".join(dict.fromkeys(pos))),
                ("Regras de negócio", "<br>".join(f"**{i}** {rn.get(i, '')}" for i in rn_ids)),
                ("Critérios de aceite", ", ".join(a["id"] for a in s["acs"])), ("Origem", f.get("origem", ""))]
        body = "\n".join(f"| {k} | {cell(v) if not v.startswith('**') and '<br>' not in v else v.replace('|', chr(92) + '|') or '—'} |" for k, v in rows)
        cases.append(f"{h}# UC-{n:02d} · {s['title']} ({s['id']})\n\n| Campo | Detalhe |\n|---|---|\n{body}\n")
        by_actor.setdefault(ator, []).append(f"UC-{n:02d} {s['title']}")
    out += ["**Atores e seus casos de uso**", "", table(["Ator", "Casos de uso"], [(a, "<br>".join(u)) for a, u in by_actor.items()]), "",
            f"{h}# Diagrama de casos de uso", "", "```mermaid", uc_code.strip(), "```", ""]
    return "\n".join(out + cases)


def diagrams_md(sdd, lvl, uc_code, has_uc_file):
    h = "#" * lvl
    items = []
    d = sdd / "04-design" / "diagramas"
    for f in sorted(d.glob("*.mmd")) if d.exists() else []:
        items.append((f.stem, f.read_text(encoding="utf-8")))
    if uc_code and not has_uc_file:
        items.insert(0, ("casos-de-uso", uc_code))
    out = []
    for stem, code in items:
        refs = re.search(r"^%%\s*refs:\s*(.+)$", code, re.M)
        out += [f"{h} {diag_title(stem, code)}", "", f"_Cobre: {refs.group(1).strip()}_" if refs else "", "", "```mermaid", code.strip(), "```", ""]
    return "\n".join(out), items


def requirements_md(spec, lvl):
    h = "#" * lvl
    out = []
    for e in spec["epics"]:
        out += [f"{h} {e['id']} · {e['title']}", ""]
        for s in spec["stories"]:
            f = s["fields"]
            if e["id"] not in f.get("epico", ""):
                continue
            out += [f"{h}# {s['id']} · {s['title']}", "", f"> {f.get('historia', '').replace('*', '')}", "",
                    table(["Prioridade", "MVP", "Regras", "NFR", "Origem"],
                          [(f.get("prioridade", ""), f.get("mvp", ""), f.get("regras de negocio", ""), f.get("nfr relacionados", ""), f.get("origem", ""))]), "",
                    "**Critérios de aceite**", ""]
            for a in s["acs"]:
                b = parse_bdd(a["text"]) if a["tipo"] == "BDD" else None
                txt = f"_Dado que_ {b[0]} · _Quando_ {b[1]} · _Então_ {b[2]}" if b else a["text"]
                out.append(f"- **{a['id']} ({a['tipo']}):** {txt}")
            out.append("")
    if spec["rn"]:
        out += [f"{h} Regras de negócio", "", table(["ID", "Regra"], spec["rn"]), ""]
    if spec["rnf"]:
        out += [f"{h} Requisitos não funcionais", "", table(["ID", "Requisito"], spec["rnf"]), ""]
    return "\n".join(out)


def critical_path(tasks):
    by = {t["id"]: t for t in tasks}
    memo = {}

    def lg(n, stack=()):
        if n in stack:
            return (0, [])
        if n not in memo:
            best = max((lg(d, stack + (n,)) for d in by[n]["depende"] if d in by), key=lambda x: x[0], default=(0, []))
            memo[n] = (best[0] + (by[n]["est"] or 0), best[1] + [n])
        return memo[n]
    return max((lg(n) for n in by), key=lambda x: x[0], default=(0, []))


def planning_md(sdd, tasks, lvl):
    h = "#" * lvl
    out = []
    if tasks:
        total = sum(t["est"] or 0 for t in tasks)
        por_tipo = {}
        for t in tasks:
            por_tipo[t["tipo"]] = por_tipo.get(t["tipo"], 0) + (t["est"] or 0)
        cp, path = critical_path(tasks)
        out += [f"{h} Tasks", "", f"**{len(tasks)} tasks · {total:g} (pontos/dias) no total.** Caminho crítico: {' → '.join(path)} ({cp:g}).", "",
                table(["ID", "Título", "Tipo", "Est.", "Depende de", "Refs"],
                      [(t["id"], t["title"], t["tipo"], f"{t['est']:g}" if t["est"] is not None else "—", ", ".join(t["depende"]) or "—", ", ".join(t["refs"])) for t in tasks]), "",
                "Distribuição por tipo: " + ", ".join(f"{k} {v:g}" for k, v in sorted(por_tipo.items())), ""]
    for rel, nome in (("05-planejamento/plano-scrum.md", "Plano Scrum"), ("05-planejamento/plano-kanban.md", "Plano Kanban"),
                      ("05-planejamento/dependencias.md", "Dependências")):
        t = read(sdd / rel)
        if has_content(t):
            out += [f"{h} {nome}", "", include(t, lvl + 1, drop_h1=True), ""]
    rs = bold_items(clean(read(sdd / "05-planejamento/riscos.md")), "RSK")
    if rs:
        out += [f"{h} Riscos", "", table(["ID", "Risco", "Probabilidade", "Impacto", "Mitigação", "Dono"],
                [(r["id"], r["title"], r["fields"].get("probabilidade", ""), r["fields"].get("impacto", ""), r["fields"].get("mitigacao", ""), r["fields"].get("dono", "")) for r in rs]), ""]
    return "\n".join(out)


def tests_md(tests, lvl):
    if not tests:
        return ""
    return table(["Caso", "Título", "Cobre", "Nível", "Resultado esperado"],
                 [(c["id"], c["title"], ", ".join(c["cobre"]), c["fields"].get("nivel", ""), c["fields"].get("resultado esperado", "")) for c in tests])


def trace_md(spec, tasks, tests):
    rows = []
    for s in spec["stories"]:
        for a in s["acs"]:
            tk = [t["id"] for t in tasks if a["id"] in t["refs"]]
            ct = [c["id"] for c in tests if a["id"] in c["cobre"]]
            rows.append((s["id"], a["id"], ", ".join(tk) or "—", ", ".join(ct) or "—"))
    return table(["US", "AC", "Tasks", "Casos de teste"], rows)


def pending_md(sdd, lvl):
    h, out = "#" * lvl, []
    qs = bold_items(clean(read(sdd / QUESTIONS)), "Q")
    if qs:
        out += [f"{h} Perguntas", "", table(["ID", "Pergunta", "Impacto", "Status", "Resposta"],
                [(q["id"], q["title"], q["fields"].get("impacto", ""), q["fields"].get("status", ""), q["fields"].get("resposta", "")) for q in qs]), ""]
    ss = bold_items(clean(read(sdd / ASSUMPTIONS)), "A")
    if ss:
        out += [f"{h} Suposições", "", table(["ID", "Suposição", "Confiança", "Se falsa", "Validar com"],
                [(s["id"], s["title"], s["fields"].get("confianca", ""), s["fields"].get("se falsa, o impacto e", ""), s["fields"].get("validar com", "")) for s in ss]), ""]
    from validate_discovery import SUF, section, rows
    suf = clean(read(sdd / SUF))
    lac = rows(section(suf, "Lacunas"))
    if lac:
        out += [f"{h} Lacunas aceitas", "", "Pendências que seguem sem resposta por decisão de um usuário autorizado.", "",
                table(["Lacuna", "Impacto", "Aceito por", "Justificativa", "Artefatos afetados"], [tuple(c[:5]) for c in lac]), ""]
    f = fields(section(suf, "Aprovacao"))
    if f.get("resumo aprovado por"):
        out += [f"{h} Aprovação do Discovery", "", f"Resumo aprovado por **{f['resumo aprovado por']}** em {f.get('aprovado em', '')}.", ""]
    return "\n".join(out)


def gate_status(sdd, proj):
    fase = proj.get("fase_atual", 0)
    gate = max(0, min((fase if isinstance(fase, int) else 1) - 1, 6))
    here = Path(__file__).parent
    p = subprocess.run([sys.executable, str(here / "run_all.py"), "--gate", str(gate), "--sdd", str(sdd)], capture_output=True, text=True)
    return gate, p.returncode == 0


# ------------------------------------------------------------------ montagem
def build(sdd, formatos, out_dir, render):
    proj = load_project(sdd)
    nome = proj.get("nome") or "Projeto"
    spec = parse_spec(read(sdd / SPEC))
    tasks = parse_tasks(read(sdd / TASKS))
    tests = parse_tests(read(sdd / TESTS))
    d = sdd / "04-design" / "diagramas"
    has_uc_file = d.exists() and any(f.stem.startswith("casos-de-uso") for f in d.glob("*.mmd"))
    uc_code = auto_use_case_diagram(spec, nome) if spec["stories"] else ""
    if has_uc_file:
        uc_code = next(f for f in sorted(d.glob("*.mmd")) if f.stem.startswith("casos-de-uso")).read_text(encoding="utf-8")
    gate, ok = gate_status(sdd, proj)
    status_html = f"Aprovado no gate {gate}" if ok else f"RASCUNHO: gate {gate} com erros"
    hoje = datetime.date.today().isoformat()
    meta = [("Projeto", nome), ("Modo", proj.get("modo", "")), ("Metodologia", proj.get("metodologia", "")), ("Tamanho", proj.get("tamanho", "")),
            ("Gerado em", hoje), ("Versão da spec", content_hash(sdd / SPEC)[:8]), ("Status de validação", status_html)]

    ch = []  # capítulos (lista de (titulo, md))
    visao = []
    for rel in (CONTEXT,):
        t = read(sdd / rel)
        if has_content(t):
            visao.append(include(t, 3, drop_h1=True))
    ch.append(("Visão geral", "\n\n".join(visao)))
    stack = []
    for rel in ("02-stack/criterios.md", ANALYSIS):
        t = read(sdd / rel)
        if has_content(t):
            stack.append(include(t, 3, drop_h1=True))
    adrdir = sdd / "02-stack" / "adr"
    for f in sorted(adrdir.glob("ADR-*.md")) if adrdir.exists() else []:
        stack.append(include(f.read_text(encoding="utf-8"), 3))
    ch.append(("Stack e decisões arquiteturais", "\n\n".join(stack)))
    req = requirements_md(spec, 3)
    comp = read(sdd / "03-requisitos/compliance.md")
    if has_content(comp):
        req += "\n\n### Compliance\n\n" + include(comp, 4, drop_h1=True)
    ch.append(("Requisitos", req))
    uc_section = uc_md(spec, nome, 3, uc_code) if spec["stories"] else ""
    ch.append(("Casos de uso", uc_section))
    dmd, dlist = diagrams_md(sdd, 3, uc_code, has_uc_file)
    design = []
    for rel, titulo in (("04-design/design.md", None), ("04-design/modelo-de-dados.md", "Modelo de dados"), ("04-design/contratos-api.md", "Contratos de API")):
        t = read(sdd / rel)
        if has_content(t):
            design.append(include(t, 3, drop_h1=True) if titulo is None else f"### {titulo}\n\n" + include(t, 4, drop_h1=True))
    design.append("### Diagramas UML\n\n" + diagrams_md(sdd, 4, uc_code, has_uc_file)[0])
    ch.append(("Design e UML", "\n\n".join(design)))
    ch.append(("Planejamento", planning_md(sdd, tasks, 3)))
    ch.append(("Plano de testes", tests_md(tests, 3)))
    ch.append(("Rastreabilidade", trace_md(spec, tasks, tests)))
    ch.append(("Glossário", include(read(sdd / "GLOSSARIO.md"), 3, drop_h1=True) if has_content(read(sdd / "GLOSSARIO.md")) else ""))
    ch.append(("Pendências e suposições", pending_md(sdd, 3)))
    leg = sdd / "legado"
    if leg.exists():
        parts = [include(f.read_text(encoding="utf-8"), 3) for f in sorted(leg.glob("*.md")) if has_content(f.read_text(encoding="utf-8"))]
        ch.append(("Sistema existente (linha de base)", "\n\n".join(parts)))
    mud = sdd / "mudancas"
    if mud.exists():
        parts = []
        for c in sorted(p for p in mud.iterdir() if p.is_dir() and not p.name.startswith("_")):
            t = read(c / "delta-spec.md")
            if has_content(t):
                parts.append(f"### {c.name}\n\n" + include(t, 4, drop_h1=True))
        ch.append(("Mudanças (evolução)", "\n\n".join(parts)))
    ch = [(t, b) for t, b in ch if b.strip()]

    def cover_md():
        return "\n".join([f"# {nome}", "", "**Documento de Especificação do Sistema**", "", table(["Campo", "Valor"], meta), ""])

    toc = "\n".join(f"{n}. [{t}](#{slug(t)})" for n, (t, _) in enumerate(ch, 1))
    full = cover_md() + "\n## Sumário\n\n" + toc + "\n\n" + "\n\n".join(f"## {t}\n\n{b}" for t, b in ch) + "\n"
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []

    def w(name, text):
        (out_dir / name).write_text(text, encoding="utf-8")
        written.append(name)

    if "md" in formatos:
        w("especificacao.md", full)
        if spec["stories"]:
            w("casos-de-uso.md", f"# Casos de uso: {nome}\n\n" + uc_md(spec, nome, 2, uc_code).replace("## Catálogo de casos de uso", "## Catálogo de casos de uso", 1) + "\n")
        if dlist:
            w("diagramas.md", f"# Diagramas UML: {nome}\n\n" + diagrams_md(sdd, 2, uc_code, has_uc_file)[0] + "\n")
    rend = Renderer(render)
    if "svg" in formatos or ("md" in formatos and render and rend.mmdc):
        (out_dir / "diagramas").mkdir(exist_ok=True)
        for stem, code in dlist:
            if stem == "casos-de-uso" and not has_uc_file:
                (out_dir / "diagramas" / "casos-de-uso.mmd").write_text(code, encoding="utf-8")
            svg = rend.svg(code)
            if svg:
                (out_dir / "diagramas" / f"{stem}.svg").write_text(svg, encoding="utf-8")
                written.append(f"diagramas/{stem}.svg")
    if "html" in formatos or "pdf" in formatos:
        body, tocl = md_to_html(full, rend)
        # capa e sumário próprios
        body = re.sub(r"<h1 id=[^>]*>.*?</h1>\s*<p>.*?</p>\s*<table>.*?</table>", "", body, count=1, flags=re.S)
        tocs = "".join(f'<li><a href="#{sid}">{html.escape(t)}</a></li>' for lv, t, sid in tocl if lv == 2 and t != "Sumário")
        stcls = "ok" if ok else "rascunho"
        capa = (f'<section class="capa"><h1>{html.escape(nome)}</h1><div class="sub">Documento de Especificação do Sistema</div><table>'
                + "".join(f"<tr><th>{html.escape(k)}</th><td{(' class=' + stcls) if k.startswith('Status') else ''}>{html.escape(str(v))}</td></tr>" for k, v in meta)
                + f'</table></section><section class="toc"><h2 style="page-break-before:auto">Sumário</h2><ul>{tocs}</ul></section>')
        body = re.sub(r'<h2 id="sumário">.*?</h2>\s*<ol>.*?</ol>', "", body, count=1, flags=re.S)
        doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{html.escape(nome)}: Especificação</title><style>{CSS}</style></head><body>{capa}{body}</body></html>'
        (out_dir / "especificacao.html").write_text(doc, encoding="utf-8")
        written.append("especificacao.html")
        if "pdf" in formatos:
            ok_pdf, motor = to_pdf(out_dir / "especificacao.html", out_dir / "especificacao.pdf")
            if ok_pdf:
                written.append("especificacao.pdf")
                print(f"PDF gerado com {motor}")
            else:
                print("AVISO: PDF não gerado (precisa de Chrome/Chromium ou wkhtmltopdf). Abra especificacao.html no navegador e use Imprimir > Salvar como PDF.")
        if rend.mmdc is None and any(True for _ in dlist):
            print("AVISO: mmdc não encontrado; diagramas aparecem como código no HTML/PDF (npm i -g @mermaid-js/mermaid-cli).")
        elif rend.failed:
            print(f"AVISO: {rend.failed} diagrama(s) não renderizaram (verifique Chrome/Chromium; defina CHROME_PATH).")
    return written, ok


def to_pdf(html_path, pdf_path):
    chrome = find_chrome()
    if chrome:
        p = subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()], capture_output=True, text=True, timeout=180)
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            return True, "Chrome"
    wk = shutil.which("wkhtmltopdf")
    if wk:
        subprocess.run([wk, "--quiet", "--enable-local-file-access", "--page-size", "A4", "--footer-center", "[page]/[topage]", str(html_path), str(pdf_path)], capture_output=True, timeout=180)
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            return True, "wkhtmltopdf"
    return False, None


def main():
    ap = std_args("Gera documentação final (md/html/pdf)")
    ap.add_argument("--formatos", default="md,html,pdf", help="md,html,pdf (padrão: todos)")
    ap.add_argument("--saida", help="pasta de saída (padrão: <sdd>/08-docs)")
    ap.add_argument("--sem-render", action="store_true", help="não renderiza Mermaid (usa código no HTML/PDF)")
    a = ap.parse_args()
    sdd = get_sdd(a.sdd)
    if not read(sdd / SPEC).strip() or not parse_spec(read(sdd / SPEC))["stories"]:
        sys.exit("Sem user stories em spec.md: nada a documentar ainda (rode /sdd-spec).")
    formatos = {f.strip() for f in a.formatos.split(",")}
    written, ok = build(sdd, formatos, Path(a.saida) if a.saida else sdd / "08-docs", not a.sem_render)
    print("Gerados:", ", ".join(written))
    if not ok:
        print("ATENÇÃO: os validadores do gate atual reprovaram; o documento foi marcado como RASCUNHO.")


if __name__ == "__main__":
    main()
