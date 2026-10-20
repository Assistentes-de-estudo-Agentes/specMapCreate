# BDD e EARS

## BDD (Dado que / Quando / Então), nessa ordem
```
**AC003.1 (BDD)**
- **Dado que** o livro está disponível e o sócio possui menos de 3 empréstimos ativos
- **Quando** a bibliotecária registra o empréstimo
- **Então** o livro passa a "emprestado" e o vencimento é a data atual mais 14 dias
```
O "Então" descreve resultado **observável** (tela, dado gravado, mensagem, evento), não implementação.

## EARS (o validador exige "deve")
| Padrão | Modelo |
|---|---|
| Ubíquo | O sistema **deve** ... |
| Evento | **Quando** <evento>, o sistema **deve** ... |
| Estado | **Enquanto** <estado>, o sistema **deve** ... |
| Indesejado | **Se** <condição>, **então** o sistema **deve** ... |
| Opcional | **Onde** <recurso presente>, o sistema **deve** ... |

```
**AC003.2 (EARS)**
- **Se** o sócio já possuir 3 empréstimos ativos, **então** o sistema **deve** impedir o novo empréstimo e informar o limite.
```

## Boas práticas
- Um comportamento por AC. Números, unidades e mensagens exatas quando importarem.
- Cubra: caminho feliz, validações, permissões, limites, concorrência, falhas de integração.
- Evite voz passiva ("deve ser enviado"): diga **quem** faz.
- INVEST nas US: independente, negociável, valiosa, estimável, pequena, testável.
