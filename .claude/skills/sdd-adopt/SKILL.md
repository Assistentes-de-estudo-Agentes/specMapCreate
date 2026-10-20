---
name: sdd-adopt
description: Modo evolução do SDD. Faz engenharia reversa de um sistema existente e cria a linha de base (legado/baseline) para futuras mudanças. Use quando o usuário chamar /sdd-adopt ou quiser especificar evolução de um sistema que já existe.
---

# /sdd-adopt: linha de base do sistema existente

Pré-requisito: projeto com `modo: evolucao` (`/sdd-init`) e acesso ao repositório do sistema (somente leitura).

## Passos
1. Delegue ao subagente **legacy-analyst** a leitura do código/documentação. Ele retorna inventário e achados; **você** grava em `.sdd/legado/`:
   - `inventario.md`: módulos, entidades/dados, integrações, endpoints/telas, stack detectada;
   - `arquitetura-atual.md`: diagramas *as-is* em Mermaid;
   - `divida-tecnica.md`: pontos frágeis, riscos, ausência de testes;
   - `baseline.md`: US/AC **retroativas** reconstruídas do comportamento observável, cada item com **origem** (arquivo/módulo), **confiança** (alta/média/baixa) e coluna *Confirmado?*.
2. Crie **ADRs retroativos** da stack detectada com `Status: aceita` somente após confirmação e a marca `(inferido)` no contexto.
3. **Gate humano obrigatório:** apresente o baseline ao usuário, item a item, priorizando os de baixa confiança. **Nada inferido vale como verdade até ser confirmado.** Itens rejeitados são removidos ou corrigidos.
4. Atualize `project.yaml` (`stack` real detectada, `fase_atual: 2`) e `STATE.md`.

## Regras
- Nunca modifique o sistema existente.
- Não invente comportamento: se o código é ambíguo, marque confiança baixa e abra uma pergunta.
- Próximo passo: `/sdd-evolve` com a mudança desejada.
