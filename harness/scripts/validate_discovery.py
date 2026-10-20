#!/usr/bin/env python3
"""Gate 1 (Discovery): suficiência verificável da descoberta.

Não prova que a descoberta é boa, mas impede fechar o Discovery sem: checklist dos 9 domínios
com evidência, registro de conhecimento classificado, lacunas aceitas com responsável, resumo
aprovado e vínculo da aprovação com a versão atual do intake."""
import datetime
import re
from collections import Counter

from sddlib import *

SUF = "01-discovery/suficiencia.md"
DOMINIOS = ["produto", "escopo", "funcional", "acesso", "dados", "integracoes", "nfr", "operacao", "restricoes"]
OBRIGATORIOS = {"produto", "escopo", "funcional"}
SIT = {"considerado", "nao aplicavel", "pendente aceito"}
TIPOS = {"confirmado", "inferido", "suposicao", "pendente", "restricao obrigatoria", "preferencia"}


def section(text, title):
    out, on = [], False
    for l in text.split("\n"):
        m = re.match(r"^##\s+(.*?)\s*$", l)
        if m:
            on = norm(m.group(1)).startswith(norm(title))
            continue
        if on:
            out.append(l)
    return out


def rows(lines):
    res = []
    for l in lines:
        s = l.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) or c == "" for c in cells):
            continue
        res.append(cells + [""] * (5 - len(cells)))
    return res[1:]  # descarta cabeçalho


def short(s, n=3):
    return len(s.strip()) >= n and norm(s) not in ("-", "—", "n/a")


def check(sdd, gate=None):
    sdd = Path(sdd)
    r = Report("validate_discovery")
    p = load_project(sdd)
    fase = p.get("fase_atual", 0) if isinstance(p.get("fase_atual", 0), int) else 0
    completed = gate if gate is not None else max(fase - 1, 0)
    if completed < 1:
        r.info("DISC-000", "Discovery em andamento; a suficiência é exigida a partir do gate 1")
        return r
    text = clean(read(sdd / SUF))
    if not text.strip():
        r.erro("DISC-001", f"{SUF} ausente ou vazio (modelo em harness/templates/sdd/01-discovery/suficiencia.md)")
        return r
    qs = bold_items(clean(read(sdd / QUESTIONS)), "Q")
    ass = bold_items(clean(read(sdd / ASSUMPTIONS)), "A")
    qids, aids = {q["id"] for q in qs}, {a["id"] for a in ass}
    known = qids | aids

    # --- resumo e tamanho
    resumo = "\n".join(section(clean(read(sdd / CONTEXT)), "Resumo")).strip()
    if len(resumo) < 40:
        r.erro("DISC-060", "contexto.md: seção '## Resumo' ausente ou curta demais (mín. 40 caracteres); ela é o resumo que o usuário aprova")
    if p.get("tamanho") in (None, "indefinido"):
        r.erro("DISC-061", "project.yaml: 'tamanho' indefinido; confirme pequeno/medio/grande no Discovery")

    # --- checklist de domínios
    dom = {}
    for c in rows(section(text, "Checklist")):
        for key in DOMINIOS:
            if norm(c[0]).startswith(key):
                dom[key] = c
    pend_aceitas, evid = set(), []
    for key in DOMINIOS:
        c = dom.get(key)
        if not c:
            r.erro("DISC-010", f"domínio ausente no checklist: {key}")
            continue
        sit, ev, refs = norm(c[1]), c[2], c[3]
        if sit not in SIT:
            r.erro("DISC-011", f"{key}: situação '{c[1]}' inválida (use: considerado | não aplicável | pendente aceito)")
            continue
        if len(ev.strip()) < 15:
            r.erro("DISC-012", f"{key}: evidência/justificativa insuficiente (mín. 15 caracteres); " + ("explique por que não se aplica" if sit == "nao aplicavel" else "diga o que foi decidido ou perguntado"))
        if key in OBRIGATORIOS and sit == "nao aplicavel":
            r.erro("DISC-013", f"{key}: domínio obrigatório não pode ser 'não aplicável'")
        ids = re.findall(r"[QA]\d{3}", ev + " " + refs)
        for i in ids:
            if i not in known:
                r.erro("DISC-014", f"{key}: referencia {i}, que não existe em perguntas/suposições")
        if sit in ("considerado", "pendente aceito") and not short(refs):
            r.erro("DISC-016", f"{key}: informe 'Refs' (arquivo, Qxxx, Axxx ou 'intake') que sustentem a situação")
        if sit == "pendente aceito":
            qr = [i for i in ids if i.startswith("Q")]
            if not qr:
                r.erro("DISC-015", f"{key}: 'pendente aceito' exige a pergunta pendente (Qxxx) nas Refs")
            pend_aceitas |= set(qr)
        evid.append(norm(ev))
    rep = Counter(evid).most_common(1)
    if rep and rep[0][1] >= 4:
        r.aviso("DISC-017", f"{rep[0][1]} domínios com a mesma evidência: parece texto copiado, não análise")

    # --- registro de conhecimento
    reg = rows(section(text, "Registro"))
    if not reg:
        r.erro("DISC-020", "registro de conhecimento vazio: classifique os fatos (Confirmado, Inferido, Suposição, Pendente, Restrição obrigatória, Preferência)")
    if reg and not any(norm(c[1]) in ("confirmado", "restricao obrigatoria") for c in reg):
        r.erro("DISC-021", "nenhum item 'Confirmado' ou 'Restrição obrigatória': o que o usuário declarou deve estar registrado com fonte")
    for c in reg:
        t = norm(c[1])
        if t not in TIPOS:
            r.erro("DISC-022", f"registro '{c[0][:40]}': tipo '{c[1]}' inválido")
            continue
        if not short(c[2]):
            r.erro("DISC-023", f"registro '{c[0][:40]}': sem fonte")
        refs = re.findall(r"[QA]\d{3}", c[0] + " " + c[2])
        if t == "suposicao" and not any(i in aids for i in refs):
            r.erro("DISC-024", f"registro '{c[0][:40]}': suposição precisa referenciar uma Axxx existente")
        if t == "pendente" and not any(i in qids for i in refs):
            r.erro("DISC-025", f"registro '{c[0][:40]}': pendente precisa referenciar uma Qxxx existente")

    # --- perguntas e suposições
    for item in qs + ass:
        if not item["fields"].get("fonte"):
            r.aviso("DISC-030", f"{item['id']}: sem campo 'Fonte' (trecho do intake, resposta ou requisito)")
    aceitas = {q["id"] for q in qs if norm(q["fields"].get("status", "")).startswith("aceit")}
    for q in qs:
        if q["id"] in aceitas and norm(q["fields"].get("impacto", "")).startswith("bloqueante"):
            r.aviso("DISC-042", f"{q['id']}: pergunta BLOQUEANTE seguiu com risco aceito; confirme que foi decisão de usuário autorizado")

    # --- lacunas aceitas
    lac = {}
    for c in rows(section(text, "Lacunas")):
        for i in re.findall(r"Q\d{3}", c[0]):
            lac[i] = c
    for i in sorted(aceitas | pend_aceitas):
        c = lac.get(i)
        if not c:
            r.erro("DISC-040", f"{i}: risco aceito sem registro em 'Lacunas aceitas'")
            continue
        if not short(c[2]) or len(c[3].strip()) < 10 or not short(c[4]):
            r.erro("DISC-041", f"{i}: lacuna aceita exige 'Aceito por', justificativa (mín. 10 caracteres) e artefatos afetados")

    # --- aprovação
    f = fields(section(text, "Aprovacao"))
    por, em, h = f.get("resumo aprovado por", ""), f.get("aprovado em", ""), f.get("intake (hash)", "")
    if not short(por) or not short(em) or not short(h):
        r.erro("DISC-050", "aprovação ausente: o usuário precisa aprovar o resumo (stamp.py --aprovar-discovery --por \"Nome\")")
    else:
        try:
            datetime.date.fromisoformat(em.strip())
        except ValueError:
            r.erro("DISC-053", f"'Aprovado em' deve ser data ISO AAAA-MM-DD (atual: {em})")
        atual = str(p.get("intake_sha256") or "")[:12]
        if not atual:
            r.erro("DISC-052", "intake sem hash em project.yaml (rode stamp.py --intake)")
        elif h.strip() != atual:
            r.erro("DISC-051", "o intake mudou depois da aprovação do Discovery; revise e reaprove (stamp.py --aprovar-discovery)")
    if not r.erros:
        n = Counter(norm(dom[k][1]) for k in DOMINIOS if k in dom)
        r.info("DISC-100", f"Discovery suficiente: {n['considerado']} considerado(s), {n['nao aplicavel']} não aplicável(is), {n['pendente aceito']} pendente(s) aceito(s)")
    return r


def main():
    ap = std_args("Valida suficiência do Discovery")
    ap.add_argument("--gate", type=int, help="fase cuja conclusão está sendo validada")
    a = ap.parse_args()
    return check(get_sdd(a.sdd), a.gate).emit(a.json)


if __name__ == "__main__":
    raise SystemExit(main())
