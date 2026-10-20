---
name: sdd-docs
description: Gera a documentação final do projeto SDD a partir do .sdd/: especificação consolidada em Markdown, catálogo de casos de uso, diagramas UML e, se houver ferramentas, HTML e PDF. Use quando o usuário chamar /sdd-docs ou pedir "o documento final", "manual do sistema", "PDF da especificação" ou "casos de uso em markdown".
---

# /sdd-docs: documentação final

Os documentos são **derivados**: nunca edite `.sdd/08-docs/` à mão. Corrija a fonte (spec, design, tasks) e gere de novo.

## Passos
1. Rode `python3 harness/scripts/run_all.py --gate 6`. Gerar com erros é permitido, mas o documento sai marcado como **RASCUNHO**; avise o usuário.
2. Gere: `python3 harness/scripts/build_docs.py` (padrão: md, html e pdf). Opções: `--formatos md` (só Markdown), `--sem-render` (não renderiza Mermaid), `--saida <pasta>`.
3. Saídas em `.sdd/08-docs/`:
   - `especificacao.md`: documento completo (visão geral, stack e ADRs, requisitos, casos de uso, design e UML, planejamento, testes, rastreabilidade, glossário, pendências; no modo evolução, também baseline e mudanças);
   - `casos-de-uso.md`: catálogo de casos de uso (ator, pré-condições, fluxo principal, exceções, pós-condições, regras) + diagrama de casos de uso;
   - `diagramas.md` e `diagramas/*.svg|.mmd`: todos os diagramas UML (Mermaid renderiza no GitHub);
   - `especificacao.html` e `especificacao.pdf`: versão para leitura e entrega.
4. Informe o que foi gerado e o que **não** foi: se `mmdc` ou Chrome/Chromium não existirem, os diagramas aparecem como código no HTML/PDF e o PDF pode não ser gerado (alternativa: abrir o HTML e imprimir em PDF). Defina `CHROME_PATH` se o Chrome não for encontrado.

## Regras
- O catálogo de casos de uso é montado de forma **determinística** a partir das US/AC (BDD → pré-condição/fluxo/pós; EARS → exceções). Se um caso ficou pobre, o defeito está na US/AC: corrija na spec.
- Se não existir `casos-de-uso*.mmd` em `04-design/diagramas/`, o diagrama de casos de uso é gerado automaticamente (não conta no limite de diagramas do tamanho do projeto).
- Não afirme que o PDF foi gerado sem conferir o arquivo.
