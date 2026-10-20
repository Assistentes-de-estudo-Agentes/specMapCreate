# Estratégia de testes (especificação)

| Tipo de requisito | Nível sugerido |
|---|---|
| Regra de negócio / cálculo | unitário |
| Persistência, API, integração | integração / contrato |
| Fluxo completo do usuário | E2E |
| RNF de desempenho | carga/desempenho (com meta numérica) |
| RNF de segurança | segurança (autorização, injeção, sessão) |
| Acessibilidade | auditoria WCAG + teste manual |

Cobertura mínima por AC:
- BDD: caminho feliz + ao menos um caso de borda;
- EARS "Se...então": caso que provoca a condição;
- RNF: um caso mensurável com o número da spec.

Ferramentas recomendadas vêm do pack da stack (`testes` em `pack.json`).
Dados de exemplo devem ser fictícios (nada de dados pessoais reais).
