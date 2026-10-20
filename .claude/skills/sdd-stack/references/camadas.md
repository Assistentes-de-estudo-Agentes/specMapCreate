# Camadas e ordem de decisão

1. **backend** (linguagem/framework)
2. **orm / acesso a dados** (depende do backend)
3. **frontend**
4. **banco**
5. **cache_mensageria**
6. **auth**
7. **infra** (cloud/hospedagem)
8. **cicd**
9. **observabilidade**
10. **testes**
11. **qualidade** (lint, tipagem, análise estática)

Se o usuário escolheu a linguagem/framework primeiro, a escolha filtra as demais.
Em projetos só-API ou só-mobile, `frontend` pode ser dispensado (registre como "n/a" em `analise.md`).

## Perguntas que mudam o ranking
- O time já domina alguma opção? (bônus de conhecimento)
- Volume de dados e de usuários esperados?
- Requisitos regulatórios que restringem local dos dados ou fornecedores?
- Orçamento mensal de infraestrutura?
- Quem opera em produção?
