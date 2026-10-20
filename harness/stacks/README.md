# Packs de stack

Cada pack em `stacks/<nome>/pack.json` descreve, por **camada**, opções, notas (0–5) por critério, prós/contras, regras de compatibilidade (`requer`, `conflita`), tasks de fundação, NFRs comuns e anti-padrões.

## Fluxo de recomendação

1. Use Discovery para separar restrições obrigatórias de preferências negociáveis.
2. Elimine primeiro opções que violem restrições obrigatórias ou incompatibilidades confirmadas.
3. Compare opções restantes com pesos contextualizados; não trate a nota ponderada como probabilidade nem como verdade objetiva.
4. Explique recomendação, alternativas, trade-offs, custos operacionais, riscos e premissas no contexto deste projeto.
5. Verifique documentação oficial atual para versões suportadas, licenciamento, compatibilidade e ciclo de manutenção quando isso afetar a decisão. Registre URL/fonte, data e o que foi efetivamente verificado. Se não houver acesso a fontes atuais, declare explicitamente “não verificado” e reduza a confiança.
6. Solicite aprovação humana antes de registrar `Status: aceita` no ADR.
7. Ao alterar uma escolha anterior, reavalie camadas dependentes e marque artefatos afetados como obsoletos.

## Critérios e pesos

Ordem das notas: `time_to_market, custo, escala, conhecimento_time, seguranca, manutenibilidade, ecossistema`.
As notas são julgamento curado (0–5), não medição. O bônus de conhecimento do time é limitado e deve ser informado; não pode tornar uma opção tecnicamente incompatível aceitável.

## Usar

```bash
python3 harness/scripts/validate_stacks.py                 # valida todos os packs
python3 harness/scripts/validate_stacks.py --pack spring-boot
python3 harness/scripts/rank_stack.py --pack django        # lista camadas
python3 harness/scripts/rank_stack.py --pack django --camada banco --pesos time_to_market=5,manutenibilidade=4,custo=3 --selecionadas backend=django-drf --time-conhece postgres
```

O ranking exclui conflitos conhecidos pelas escolhas já registradas. Se uma camada requerida ainda não foi selecionada, a opção não é automaticamente rejeitada: a dependência precisa ser resolvida quando essa camada for escolhida.

## Criar pack

Copie `_template/`, renomeie e substitua todas as opções de exemplo. Valide antes de usar:

```bash
python3 harness/scripts/validate_stacks.py --pack meu-pack
python3 harness/scripts/rank_stack.py --pack meu-pack
```

Contrato mínimo:
- IDs de opção únicos dentro da camada, em minúsculas com números/hífens;
- exatamente sete notas numéricas entre 0 e 5, na ordem dos critérios;
- `requer` aponta para camadas e IDs existentes;
- `conflita` aponta para IDs existentes;
- `revisado_em` e justificativas mantidas atualizadas;
- as fontes consultadas e suas datas ficam registradas no ADR do projeto, não presumidas pelo pack.

## Manutenção

Revise packs pelo menos a cada seis meses e sempre que houver mudança relevante. A data `revisado_em` é uma declaração editorial, não prova de que versões e suporte foram verificados hoje. Sem fonte oficial atual, a recomendação deve dizer isso claramente e marcar a confiança como baixa.
