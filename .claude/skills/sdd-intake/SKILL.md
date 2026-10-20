---
name: sdd-intake
description: Fase 0 do SDD. Captura o pedido bruto do usuário (texto ou transcrição de voz) em .sdd/00-intake/raw.md, de forma imutável. Use quando o usuário chamar /sdd-intake ou descrever um sistema que quer especificar.
---

# /sdd-intake: captura do pedido bruto

Entrada do usuário: `$ARGUMENTS` (ou o texto colado na conversa, ou transcrição de voz).

## Regras
- O texto vai para `.sdd/00-intake/raw.md` **exatamente como foi escrito**: sem correção, sem formatação, sem resumo. Pode estar desorganizado ou ter erros de transcrição. Isso é intencional.
- O intake é **imutável** depois do hash. Complementos entram como nova seção anexada ao final (`## Complemento AAAA-MM-DD`), nunca editando o que já existe. Depois de um complemento, rode o hash de novo e avise que o Discovery precisa ser revisto.
- Não interprete nem tire dúvidas nesta fase. Isso é o Discovery.

## Passos
1. Verifique que `.sdd/` existe (senão, sugira `/sdd-init`).
2. Grave o texto em `.sdd/00-intake/raw.md` (substitua o comentário do template na primeira vez).
3. Registre o hash: `python3 harness/scripts/stamp.py --intake`
4. Em `project.yaml`, defina `fase_atual: 1`; adicione uma linha ao histórico em `STATE.md`.
5. Informe: quantidade de palavras capturadas e que o próximo passo é `/sdd-discover`.

Se o usuário só disse "quero criar um sistema" sem detalhes, peça que ele descreva livremente (pode ser por voz), sem se preocupar com formato.
