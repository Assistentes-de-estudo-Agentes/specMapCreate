# Diagramas UML: Biblioteca Comunitária

## Casos de uso

_Cobre: US001, US002, US003, US004, US005_

```mermaid
flowchart LR
%% refs: US001, US002, US003, US004, US005
    A1(["Bibliotecária"])
    A2(["Sócio"])
    subgraph EP001["Acervo e sócios"]
        UC_US001(("US001 Cadastrar livro"))
        UC_US002(("US002 Cadastrar sócio"))
    end
    subgraph EP002["Empréstimos"]
        UC_US003(("US003 Registrar empréstimo"))
        UC_US004(("US004 Registrar devolução com multa"))
        UC_US005(("US005 Consultar meus empréstimos"))
    end
    A1 --> UC_US001
    A1 --> UC_US002
    A1 --> UC_US003
    A1 --> UC_US004
    A2 --> UC_US005
```

## Modelo ER

_Cobre: US001, US002, US003, RN002_

```mermaid
%% refs: US001, US002, US003, RN002
erDiagram
    LIVRO ||--o{ EMPRESTIMO : "é emprestado em"
    SOCIO ||--o{ EMPRESTIMO : "realiza"
    LIVRO { string codigo PK
            string titulo
            string autor
            string status }
    SOCIO { int carteirinha PK
            string nome
            string telefone }
    EMPRESTIMO { int id PK
                 date retirada
                 date vencimento
                 date devolucao
                 decimal multa }
```

## Sequência: emprestimo

_Cobre: US003, RN001, RN002_

```mermaid
%% refs: US003, RN001, RN002
sequenceDiagram
    actor B as Bibliotecária
    participant UI as Interface web
    participant API as API
    participant DB as PostgreSQL
    B->>UI: informa livro e sócio
    UI->>API: POST /emprestimos
    API->>DB: conta empréstimos ativos do sócio
    DB-->>API: total
    alt total menor que 3 e livro disponível
        API->>DB: grava empréstimo (vencimento = hoje + 14 dias)
        API-->>UI: 201 vencimento
    else limite ou indisponível
        API-->>UI: 422 motivo
    end
```

