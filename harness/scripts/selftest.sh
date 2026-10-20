#!/usr/bin/env bash
# Autotestes positivos e adversariais do harness. Não altera o exemplo versionado.
set -u
cd "$(dirname "$0")/../.."
S=harness/scripts
EX=examples/biblioteca-comunitaria/.sdd
python3 $S/run_all.py --gate 7 --sdd "$EX" >/dev/null || { echo "FALHA: exemplo deveria passar no gate 7"; exit 1; }
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
cp -r "$EX" "$TMP/.sdd"
sed -i 's/^- \*\*Prioridade:\*\* Must/- **Prioridade:** Urgente/' "$TMP/.sdd/03-requisitos/spec.md"
python3 $S/validate_spec.py --sdd "$TMP/.sdd" >/dev/null && { echo "FALHA: spec quebrada deveria ser reprovada"; exit 1; }
INIT="$TMP/init"; python3 $S/init_project.py --destino "$INIT" --nome Teste >/dev/null || { echo "FALHA: init"; exit 1; }
python3 $S/run_all.py --gate 0 --sdd "$INIT/.sdd" >/dev/null || { echo "FALHA: projeto novo deveria passar no gate 0"; exit 1; }
python3 $S/validate_stacks.py >/dev/null || { echo "FALHA: packs de stack deveriam ser válidos"; exit 1; }
python3 $S/rank_stack.py --pack django --camada banco >/dev/null || { echo "FALHA: rank_stack"; exit 1; }
python3 $S/rank_stack.py --pack django --camada banco --pesos custo=9 >/dev/null 2>&1 && { echo "FALHA: peso fora do intervalo deveria ser rejeitado"; exit 1; }
# Caso adversarial: pack com nota fora da faixa precisa falhar.
python3 - "$TMP/pack-invalido.json" <<'PY'
import json, sys
from pathlib import Path
p=json.loads(Path('harness/stacks/django/pack.json').read_text(encoding='utf-8'))
layer=next(iter(p['camadas']))
p['camadas'][layer][0]['notas'][0]=9
Path(sys.argv[1]).write_text(json.dumps(p), encoding='utf-8')
PY
python3 $S/validate_stacks.py --arquivo "$TMP/pack-invalido.json" >/dev/null 2>&1 && { echo "FALHA: nota de pack fora de 0..5 deveria ser rejeitada"; exit 1; }
# Caso adversarial: teste sem critério de aceitação associado.
mkdir -p "$TMP/trace"
cp -r "$EX" "$TMP/trace/.sdd"
python3 - "$TMP/trace/.sdd/06-qualidade/plano-de-testes.md" <<'PY'
import re, sys
from pathlib import Path
p=Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
s2=re.sub(r'(?m)^- \*\*Cobre:\*\*.*$', '- **Cobre:**', s, count=1)
if s2 == s: raise SystemExit('não encontrou campo Cobre para teste adversarial')
p.write_text(s2, encoding='utf-8')
PY
python3 $S/validate_traceability.py --sdd "$TMP/trace/.sdd" >/dev/null 2>&1 && { echo "FALHA: teste sem Cobre deveria ser rejeitado"; exit 1; }
# Discovery: intake de uma linha, sem suficiência, deve ser reprovado no gate 1
G1="$TMP/g1"; mkdir -p "$G1"; python3 $S/init_project.py --destino "$G1" --nome T >/dev/null
echo "quero um sistema" > "$G1/.sdd/00-intake/raw.md"; python3 $S/stamp.py --sdd "$G1/.sdd" --intake >/dev/null
python3 $S/run_all.py --gate 1 --sdd "$G1/.sdd" >/dev/null 2>&1 && { echo "FALHA: discovery vazio deveria ser reprovado no gate 1"; exit 1; }
python3 $S/stamp.py --sdd "$G1/.sdd" --aprovar-discovery --por Teste >/dev/null 2>&1 && { echo "FALHA: aprovação de discovery incompleto deveria ser recusada"; exit 1; }
# Discovery: intake alterado depois da aprovação invalida a aprovação
D1="$TMP/d1"; cp -r "$EX" "$D1"; printf '\n\nComplemento: agora também haverá reservas.\n' >> "$D1/00-intake/raw.md"; python3 $S/stamp.py --sdd "$D1" --intake >/dev/null
python3 $S/validate_discovery.py --sdd "$D1" --gate 1 >/dev/null 2>&1 && { echo "FALHA: intake alterado após aprovação deveria ser reprovado"; exit 1; }
# Discovery: risco aceito sem registro de lacuna
D2="$TMP/d2"; cp -r "$EX" "$D2"; sed -i '/^| Q003:/d' "$D2/01-discovery/suficiencia.md"
python3 $S/validate_discovery.py --sdd "$D2" --gate 1 >/dev/null 2>&1 && { echo "FALHA: risco aceito sem lacuna deveria ser reprovado"; exit 1; }
# Discovery: domínio obrigatório marcado como não aplicável
D3="$TMP/d3"; cp -r "$EX" "$D3"; sed -i 's/^| Funcional | considerado/| Funcional | não aplicável/' "$D3/01-discovery/suficiencia.md"
python3 $S/validate_discovery.py --sdd "$D3" --gate 1 >/dev/null 2>&1 && { echo "FALHA: domínio obrigatório não aplicável deveria ser reprovado"; exit 1; }
# Pergunta bloqueante aberta reprova o gate 1
D4="$TMP/d4"; cp -r "$EX" "$D4"; sed -i '0,/\*\*Impacto:\*\* importante/s//**Impacto:** bloqueante/; 0,/\*\*Status:\*\* respondida/s//**Status:** aberta/' "$D4/01-discovery/perguntas-abertas.md"
python3 $S/validate_state.py --sdd "$D4" --gate 1 >/dev/null 2>&1 && { echo "FALHA: pergunta bloqueante aberta deveria reprovar o gate 1"; exit 1; }
# Documentação final: Markdown consolidado com casos de uso e UML (sem render, não exige Chrome)
python3 $S/build_docs.py --sdd "$EX" --formatos md --sem-render --saida "$TMP/docs" >/dev/null || { echo "FALHA: build_docs"; exit 1; }
grep -q "UC-01" "$TMP/docs/casos-de-uso.md" && grep -q '```mermaid' "$TMP/docs/diagramas.md" && grep -q "Rastreabilidade" "$TMP/docs/especificacao.md" || { echo "FALHA: documentação incompleta"; exit 1; }
echo "autoteste OK (positivo + casos adversariais)"
