# Caso 02 — Dependência incompatível

## Preparação
Criar pack de teste em que uma opção de frontend requer backend A, e selecionar backend B.

## Comportamento esperado
O validador rejeita IDs/camadas inexistentes. O ranking exclui opção incompatível quando a escolha anterior contradiz `requer` ou `conflita`, explicando o motivo. O bônus de familiaridade não pode superar uma incompatibilidade.
