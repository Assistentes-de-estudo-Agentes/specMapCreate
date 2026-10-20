#!/usr/bin/env python3
"""Biblioteca compartilhada do SDD Harness (somente biblioteca padrão)."""
import datetime
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------- caminhos
SPEC = "03-requisitos/spec.md"
TASKS = "05-planejamento/tasks.md"
TESTS = "06-qualidade/plano-de-testes.md"
TRACE = "06-qualidade/rastreabilidade.md"
DESIGN = "04-design/design.md"
RAW = "00-intake/raw.md"
QUESTIONS = "01-discovery/perguntas-abertas.md"
ASSUMPTIONS = "01-discovery/suposicoes.md"
CONTEXT = "01-discovery/contexto.md"
ANALYSIS = "02-stack/analise.md"

# artefato derivado -> insumos (usado pelo controle de "stale")
DEPS = {
    SPEC: [CONTEXT, ASSUMPTIONS, QUESTIONS],
    DESIGN: [SPEC, ANALYSIS],
    "04-design/modelo-de-dados.md": [SPEC],
    TASKS: [SPEC, DESIGN],
    TESTS: [SPEC, TASKS],
    TRACE: [SPEC, TASKS, TESTS],
}

REF_RE = re.compile(r"ADR-\d{3}|RNF\d{3}|RN\d{3}|US\d{3}|AC\d{3}\.\d+|EP\d{3}")


# ---------------------------------------------------------------- texto
def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s.strip().lower())


def _scalar(v):
    v = v.strip()
    if v == "":
        return None
    if v == "{}":
        return {}
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        return [] if not inner else [_scalar(x) for x in inner.split(",")]
    if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    low = v.lower()
    if low in ("null", "~"):
        return None
    if low == "true":
        return True
    if low == "false":
        return False
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return v


def mini_yaml(text):
    """Subconjunto de YAML: mapas aninhados por indentação, listas simples, [a, b]."""
    rows = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        rows.append((len(raw) - len(raw.lstrip(" ")), raw.strip()))

    def block(i, indent):
        if i >= len(rows):
            return None, i
        if rows[i][1].startswith("- "):
            out = []
            while i < len(rows) and rows[i][0] == indent and rows[i][1].startswith("- "):
                out.append(_scalar(re.split(r"\s+#", rows[i][1][2:])[0]))
                i += 1
            return out, i
        d = {}
        while i < len(rows) and rows[i][0] == indent and not rows[i][1].startswith("- "):
            k, _, v = rows[i][1].partition(":")
            k, v = k.strip(), v.strip()
            if v and v[0] not in "\"'":
                v = re.split(r"\s+#", v)[0].strip()
            i += 1
            if v == "":
                if i < len(rows) and rows[i][0] > indent:
                    val, i = block(i, rows[i][0])
                else:
                    val = None
                d[k] = val
            else:
                d[k] = _scalar(v)
        return d, i

    if not rows:
        return {}
    val, _ = block(0, rows[0][0])
    return val or {}


FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.S)


def split_front(text):
    text = text.replace("\r\n", "\n")
    m = FRONT_RE.match(text)
    if m:
        return mini_yaml(m.group(1)), text[m.end():]
    return {}, text


def clean(text):
    """Remove front matter, comentários HTML e blocos de código, preservando nº de linhas."""
    text = text.replace("\r\n", "\n")
    m = FRONT_RE.match(text)
    if m:
        text = "\n" * m.group(0).count("\n") + text[m.end():]
    blank = lambda mm: "\n" * mm.group(0).count("\n")
    text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    text = re.sub(r"^```.*?^```", blank, text, flags=re.S | re.M)
    return text


def read(path):
    p = Path(path)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def content_hash(path):
    p = Path(path)
    if not p.exists():
        return "ausente"
    _, body = split_front(p.read_text(encoding="utf-8"))
    body = "\n".join(l.rstrip() for l in body.strip().splitlines())
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]


def raw_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ---------------------------------------------------------------- blocos
FIELD_RE = re.compile(r"^\s*[-*]\s+\*\*([^*]+?):?\*\*:?\s*(.*)$")


def fields(lines):
    out = {}
    for l in lines:
        m = FIELD_RE.match(l)
        if m:
            out.setdefault(norm(m.group(1)), m.group(2).strip())
    return out


def blocks(text, head_re):
    lines = text.split("\n")
    out, cur = [], None
    for i, l in enumerate(lines):
        m = head_re.match(l)
        if m:
            if cur:
                out.append(cur)
            cur = {"id": m.group(1), "title": m.group(2).strip(), "lines": [], "line": i + 1}
        elif re.match(r"^#{1,3}\s", l):
            if cur:
                out.append(cur)
                cur = None
        elif cur is not None:
            cur["lines"].append(l)
    if cur:
        out.append(cur)
    for b in out:
        b["text"] = "\n".join(b["lines"])
        b["fields"] = fields(b["lines"])
    return out


def bold_items(text, prefix):
    """Itens no formato '**Q001**: texto' + campos '- **Chave:** valor'."""
    start = re.compile(r"^\*\*(%s\d{3})\*\*:\s*(.+)$" % prefix)
    items, cur = [], None
    for i, l in enumerate(text.split("\n")):
        m = start.match(l)
        if m:
            if cur:
                items.append(cur)
            cur = {"id": m.group(1), "title": m.group(2).strip(), "lines": [], "line": i + 1}
        elif re.match(r"^#{1,6}\s", l) or re.match(r"^\*\*[A-Z]+\d{3}", l):
            if cur:
                items.append(cur)
                cur = None
        elif cur is not None:
            cur["lines"].append(l)
    if cur:
        items.append(cur)
    for b in items:
        b["fields"] = fields(b["lines"])
    return items


AC_RE = re.compile(r"^\*\*(AC\d{3}\.\d+)\s*\((BDD|EARS)\)\*\*\s*$")


def parse_acs(text):
    acs, cur = [], None
    for l in text.split("\n"):
        m = AC_RE.match(l.strip())
        if m:
            if cur:
                acs.append(cur)
            cur = {"id": m.group(1), "tipo": m.group(2), "lines": []}
        elif cur is not None:
            if l.startswith("#"):
                acs.append(cur)
                cur = None
            elif l.strip():
                cur["lines"].append(re.sub(r"^\s*[-*]\s*", "", l.replace("**", "")).strip())
    if cur:
        acs.append(cur)
    for a in acs:
        a["text"] = " ".join(a["lines"])
    return acs


def parse_spec(text):
    t = clean(text)
    epics = blocks(t, re.compile(r"^##\s+(EP\d{3}):\s*(.+)$"))
    stories = blocks(t, re.compile(r"^###\s+(US\d{3}):\s*(.+)$"))
    for s in stories:
        s["acs"] = parse_acs(s["text"])
    rn = [(m.group(1), m.group(2)) for m in re.finditer(r"^\*\*(RN\d{3})\*\*:\s*(.+)$", t, re.M)]
    rnf = [(m.group(1), m.group(2)) for m in re.finditer(r"^\*\*(RNF\d{3})\*\*:\s*(.+)$", t, re.M)]
    return {"epics": epics, "stories": stories, "rn": rn, "rnf": rnf, "text": t}


def parse_tasks(text):
    t = clean(text)
    tasks = blocks(t, re.compile(r"^###\s+((?:TSK|SPK)\d{3}):\s*(.+)$"))
    for k in tasks:
        f = k["fields"]
        k["refs"] = REF_RE.findall(f.get("refs", ""))
        k["depende"] = re.findall(r"(?:TSK|SPK)\d{3}", f.get("depende de", ""))
        m = re.search(r"\d+(?:[.,]\d+)?", f.get("estimativa", ""))
        k["est"] = float(m.group(0).replace(",", ".")) if m else None
        k["tipo"] = norm(f.get("tipo", ""))
        k["confianca"] = norm(f.get("confianca", ""))
        k["dod"] = len(re.findall(r"^\s*[-*]\s*\[[ xX]\]", k["text"], re.M))
        k["cts"] = re.findall(r"CT\d{3}\.\d+\.\d+", f.get("casos de teste", ""))
    return tasks


def parse_tests(text):
    t = clean(text)
    cts = blocks(t, re.compile(r"^###\s+(CT\d{3}\.\d+\.\d+):\s*(.+)$"))
    for c in cts:
        c["cobre"] = re.findall(r"AC\d{3}\.\d+", c["fields"].get("cobre", ""))
    return cts


# ---------------------------------------------------------------- projeto
def get_sdd(arg):
    p = Path(arg)
    if not p.exists():
        print(f"[ERRO] pasta '{arg}' não encontrada. Rode /sdd-init ou use --sdd <caminho>.")
        sys.exit(2)
    return p


def load_project(sdd):
    return mini_yaml(read(Path(sdd) / "project.yaml"))


def stamp(sdd, rel):
    """Grava front matter com os hashes dos insumos (base do controle de stale)."""
    sdd = Path(sdd)
    p = sdd / rel
    if rel not in DEPS or not p.exists():
        return False
    _, body = split_front(p.read_text(encoding="utf-8"))
    lines = ["---", f"id: {Path(rel).stem}", f"gerado_em: {datetime.date.today().isoformat()}", "derivado_de:"]
    for dep in DEPS[rel]:
        lines.append(f"  {dep}: {content_hash(sdd / dep)}")
    lines.append("---")
    p.write_text("\n".join(lines) + "\n" + body.lstrip("\n"), encoding="utf-8")
    return True


# ---------------------------------------------------------------- relatório
class Report:
    def __init__(self, name):
        self.name, self.items = name, []

    def erro(self, code, msg):
        self.items.append(("erro", code, msg))

    def aviso(self, code, msg):
        self.items.append(("aviso", code, msg))

    def info(self, code, msg):
        self.items.append(("info", code, msg))

    @property
    def erros(self):
        return [i for i in self.items if i[0] == "erro"]

    def emit(self, as_json=False):
        if as_json:
            print(json.dumps({"validador": self.name, "itens": [dict(nivel=a, codigo=b, mensagem=c) for a, b, c in self.items]}, ensure_ascii=False, indent=2))
        else:
            tag = {"erro": "ERRO ", "aviso": "AVISO", "info": "INFO "}
            for lvl, code, msg in self.items:
                print(f"[{tag[lvl]}] {code}: {msg}")
            n = len(self.erros)
            w = len([i for i in self.items if i[0] == "aviso"])
            print(f"== {self.name}: {n} erro(s), {w} aviso(s) ==")
        return 1 if self.erros else 0


def std_args(desc):
    import argparse
    ap = argparse.ArgumentParser(description=desc)
    ap.add_argument("--sdd", default=".sdd", help="pasta .sdd do projeto (padrão: .sdd)")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    return ap
