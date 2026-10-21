# 🧭 specMap — Harness de Desenvolvimento Orientado a Especificações

> **Transforme uma ideia em uma especificação clara e um backlog organizado antes de começar a programar.**

O **specMap** é um harness de **Spec-Driven Development (SDD)** que orienta agentes de IA, etapa por etapa, na descoberta, definição e validação de um projeto de software.

Você descreve o sistema em linguagem natural. O harness ajuda a organizar as informações e produzir requisitos, decisões técnicas, diagramas, tarefas, plano de testes e arquivos que podem apoiar a importação do backlog em ferramentas de gestão.

**Importante:** o objetivo deste projeto é produzir **especificações e planejamento**, não implementar o código da aplicação. A IA propõe; **as decisões e aprovações finais continuam sendo suas**.

---

## ✨ O que você consegue fazer com o specMap?

- 🗣️ **Começar com uma ideia em linguagem natural**, mesmo que ela ainda esteja incompleta.
- 🔎 **Descobrir o que falta decidir**, registrando dúvidas, suposições e riscos.
- 🧰 **Comparar tecnologias por camada** e registrar escolhas técnicas em ADRs.
- 📝 **Organizar requisitos**, regras de negócio, histórias de usuário e critérios de aceitação.
- 🧩 **Descrever a solução** com diagramas UML/Mermaid, modelo de dados e contratos de API.
- 🗂️ **Dividir o trabalho em tarefas** adequadas a Scrum ou Kanban.
- ✅ **Validar consistência e rastreabilidade** entre requisitos, tarefas e testes.
- 📦 **Gerar artefatos de backlog** em formatos que podem ser adaptados para Jira, Linear, Trello, GitHub Issues e CSV.
- 📚 **Gerar documentação final** em Markdown, HTML e PDF.

## 🧠 Como funciona o fluxo?

O specMap avança por fases. Cada etapa produz documentos que alimentam as seguintes.

| Fase | O que acontece | Principais resultados |
|---|---|---|
| **0. Intake** | Registra seu pedido original, sem alterá-lo. | Descrição inicial do projeto |
| **1. Discovery** | Identifica usuários, objetivos, limites, riscos, suposições e dúvidas. | Contexto, perguntas abertas e avaliação de suficiência |
| **2. Stack** | Compara tecnologias e registra decisões. | Recomendações por camada e ADRs |
| **3. Requisitos** | Define funcionalidades e regras do sistema. | Épicos, histórias de usuário, critérios de aceitação, RN e RNF |
| **4. Design** | Organiza a solução e suas interfaces. | Diagramas, modelo de dados e contratos de API |
| **5. Planejamento** | Divide o escopo em trabalho executável. | Tarefas, dependências, riscos e plano Scrum/Kanban |
| **6. Qualidade** | Revisa a especificação e planeja a verificação. | Plano de testes, rastreabilidade e revisão independente |
| **7. Export** | Organiza os resultados para uso em ferramentas de gestão. | Backlog estruturado, CSV e JSON |
| **Opcional. Docs** | Reúne os artefatos em documentação de consulta. | Especificação, casos de uso, diagramas, HTML e PDF |

### O que é um *gate*?

Um **gate** é um ponto de verificação. Ao concluir uma fase, os validadores verificam regras estruturais e consistência dos arquivos. O agente apresenta o resultado e solicita sua aprovação antes de avançar.

Passar na validação automática **não garante, por si só, que a especificação esteja correta**. Leia os documentos e confirme se eles refletem o que você deseja construir.

---

## 🚀 Comece em poucos passos

### 1. Prepare o ambiente

Você precisará de:

- **Python 3.9 ou superior** para executar os scripts de validação. O harness não exige bibliotecas Python externas para seu uso básico.
- **Claude Code**, para o fluxo de comandos `/sdd-*` disponibilizado pelo projeto. O uso em outro agente depende de ele conseguir ler e seguir as instruções compatíveis.
- **Git** é recomendado para acompanhar as alterações e recuperar versões anteriores.

Confira a versão do Python no terminal:

```bash
python3 --version
```

No Windows, caso `python3` não esteja disponível, tente:

```powershell
python --version
```

### 2. Coloque o specMap no computador

Baixe ou clone este repositório e extraia os arquivos, se necessário. Abra a **pasta raiz do specMap** na ferramenta de IA — a pasta que contém `AGENTS.md`, `CLAUDE.md`, `harness/` e `.claude/`.

Se estiver clonando do GitHub, use o endereço real do repositório no lugar de `<URL-DO-REPOSITORIO>`:

```bash
git clone <URL-DO-REPOSITORIO>
cd specMap
```

> **Dica:** não abra apenas a pasta `harness/` ou `.claude/`. A ferramenta precisa enxergar a estrutura completa para seguir o fluxo corretamente.

### 3. Inicie seu projeto

Com a pasta raiz aberta na ferramenta compatível, comece com:

```text
/sdd-init
```

O agente deve ajudar a definir as informações iniciais:

- nome do projeto;
- tipo: sistema novo (`greenfield`) ou evolução de um sistema existente (`evolucao`);
- metodologia: Scrum ou Kanban;
- tamanho e perfil da equipe.

O comando cria a estrutura de trabalho em `.sdd/`. Se essa pasta já existir, não a sobrescreva sem entender o que já foi produzido.

### 4. Descreva sua ideia

Depois da inicialização, registre o pedido original com:

```text
/sdd-intake Quero criar um sistema para [descreva sua ideia em linguagem natural].
```

Não precisa escrever como um especialista. Explique qual problema deseja resolver, quem usará o sistema e o que espera alcançar. Você também pode descrever a ideia em texto livre.

### 5. Siga as etapas

Para um projeto novo, o caminho recomendado é:

```text
/sdd-discover
/sdd-stack
/sdd-spec
/sdd-design
/sdd-plan
/sdd-quality
/sdd-export
/sdd-docs
```

Execute **uma etapa por vez** e leia os documentos gerados. `/sdd-docs` é opcional e serve para reunir os artefatos em uma documentação final.

### ⚡ Quer começar com uma única solicitação?

Você também pode pedir ao agente para conduzir o fluxo completo:

```text
/sdd-run "Quero criar um sistema para [descreva sua ideia]."
```

O comando orquestra as etapas em ordem, mas **não deve pular os gates**: vai parar para apresentar verificações, tirar dúvidas bloqueantes e solicitar aprovações humanas.

---

## 📂 Onde ficam os arquivos?

### Arquivos do harness

| Caminho | O que contém |
|---|---|
| `AGENTS.md` | Regras centrais e fluxo de trabalho para o agente |
| `CLAUDE.md` | Arquivo de referência para o ambiente Claude |
| `.claude/skills/` | Instruções das etapas `/sdd-*` |
| `.claude/agents/` | Agentes auxiliares para revisão, ambiguidade, stack e sistemas legados |
| `harness/scripts/` | Scripts de inicialização, status, validação, exportação e documentação |
| `harness/templates/` | Modelos usados para criar os documentos do projeto |
| `harness/stacks/` | Packs de referência para Django, Next.js, Spring Boot e .NET, além de um modelo |
| `harness/schemas/` | Esquemas para validar arquivos estruturados |
| `examples/biblioteca-comunitaria/` | Exemplo preenchido de um projeto, útil para aprender pelo modelo |
| `evals/` | Cenários para avaliar o comportamento e a robustez do harness |
| `docs/ARQUITETURA.md` | Detalhes técnicos sobre a arquitetura e as decisões do próprio harness |

### Arquivos gerados para o seu projeto

Os artefatos ficam normalmente em **`.sdd/`**. Entre eles:

- `project.yaml`: configuração do projeto, metodologia, tamanho e fase atual;
- `STATE.md`: estado e histórico do fluxo;
- `LESSONS.md`: aprendizados registrados durante o trabalho;
- `GLOSSARIO.md`: termos importantes do domínio;
- `00-intake/`: pedido original;
- `01-discovery/`: contexto, suposições, perguntas abertas e suficiência;
- `02-stack/`: análise da stack e registros de decisão (ADRs);
- `03-requisitos/`: especificação de requisitos;
- `04-design/`: design, diagramas, dados e contratos;
- `05-planejamento/`: tarefas, dependências, metodologia e riscos;
- `06-qualidade/`: testes, revisão e rastreabilidade;
- `07-export/`: backlog e arquivos exportáveis;
- `08-docs/`: documentação consolidada, quando gerada.

Os diretórios e arquivos específicos podem variar conforme o modo do projeto e as etapas concluídas.

---

## 🧭 Comandos de consulta e recuperação

Esses comandos são úteis depois que o projeto já começou:

| Comando | Quando usar |
|---|---|
| `/sdd-status` | Para saber a fase atual, o que falta e qual é o próximo passo |
| `/sdd-back <fase>` | Para voltar a uma fase anterior e revisar decisões. Informe o motivo quando solicitado |
| `/sdd-adopt` | Para registrar a situação atual de um sistema existente antes de planejar mudanças |
| `/sdd-evolve` | Para especificar uma mudança em um sistema existente, identificando o que será alterado |
| `/sdd-run "descrição"` | Para orquestrar o fluxo completo, respeitando os gates |

### Qual fluxo devo escolher?

- **Vou criar um sistema do zero:** use `/sdd-init` e depois `/sdd-intake`.
- **Já tenho um sistema e quero evoluí-lo:** inicialize em modo `evolucao`; em seguida, use `/sdd-adopt` para documentar a situação atual antes de especificar a mudança.
- **Não sei em que etapa parei:** use `/sdd-status`.
- **Mudei de ideia sobre uma decisão importante:** discuta o impacto com o agente e, se necessário, volte à fase adequada com `/sdd-back`.

---

## ✅ Executar as validações manualmente

Execute os comandos a seguir a partir da raiz do projeto que contém a pasta `harness/` e os artefatos `.sdd/`.

Validar a estrutura inicial:

```bash
python3 harness/scripts/run_all.py --gate 0
```

Validar até uma etapa específica, por exemplo, a fase de requisitos:

```bash
python3 harness/scripts/run_all.py --gate 3
```

O número do gate vai de `0` a `7`. Cada gate inclui verificações cumulativas necessárias até aquela fase; por isso, erros anteriores também podem aparecer.

Consultar o estado resumido:

```bash
python3 harness/scripts/status.py
```

Validar os packs de stack:

```bash
python3 harness/scripts/validate_stacks.py
```

Executar o autoteste do harness em ambientes com Bash:

```bash
bash harness/scripts/selftest.sh
```

> No Windows, esses exemplos usam `python3` e Bash. Se necessário, use `python` no lugar de `python3` e execute scripts `.sh` pelo Git Bash ou WSL.

### O que fazer se uma validação falhar?

1. Leia a mensagem completa, incluindo o nome do arquivo e o tipo de erro.
2. Peça ao agente para explicar a falha em linguagem simples.
3. Corrija os documentos relacionados sem apagar decisões aprovadas sem necessidade.
4. Rode novamente o gate correspondente.
5. Revise se a mudança deixou outros artefatos desatualizados (*stale*).

Não ignore um erro só para avançar de fase. O objetivo dos validadores é encontrar inconsistências antes que se propaguem para os próximos documentos.

---

## 🧱 Instalar o harness em outro projeto

Você não precisa usar o repositório do specMap como pasta de trabalho. Também pode instalar o harness dentro de um projeto existente.

No Linux, macOS, Git Bash ou WSL, execute a partir da pasta do specMap:

```bash
./install.sh "/caminho/para/seu-projeto"
```

Substitua o caminho pelo diretório raiz do projeto que receberá o harness. O instalador copia as skills, os agentes auxiliares, os scripts, os templates, os exemplos, as avaliações e os arquivos de apoio do GitHub Actions. Ele preserva `AGENTS.md` e `CLAUDE.md` existentes, com os ajustes previstos no script.

Depois da instalação:

1. Abra a pasta do projeto de destino na ferramenta de IA.
2. Confira o `AGENTS.md` e as instruções do projeto.
3. Execute `/sdd-init` para criar os artefatos `.sdd/`.
4. Continue pelo fluxo recomendado.

**Atenção:** faça backup ou use Git antes de instalar em um projeto existente. Revise as alterações de arquivos antes de incorporá-las ao seu repositório.

---

## 🧰 Packs de stack

O harness inclui packs de referência para:

- Django;
- Next.js;
- Spring Boot;
- .NET;
- um `_template` para criar packs personalizados.

Os packs ajudam a organizar opções por camada e comparar critérios como custo, manutenção, segurança, escala, ecossistema e familiaridade da equipe. As pontuações são avaliações de referência, **não uma verdade objetiva**. Confirme versões, compatibilidade, licenciamento e suporte nas fontes oficiais atuais antes de decidir.

Para consultar a documentação dos packs, veja [`harness/stacks/README.md`](harness/stacks/README.md).

---

## 📤 Sobre exportação e integrações

A fase `/sdd-export` gera arquivos estruturados que podem ser ajustados para ferramentas como Jira, Linear, Trello, GitHub Issues e CSV.

Isso **não significa que o specMap cria automaticamente itens em serviços externos**. Os arquivos gerados são um ponto de partida; o mapeamento e a importação dependem da configuração da ferramenta de destino. Revise os campos antes de importar.

---

## ⚠️ Limitações importantes

- O harness não gera o código da aplicação: ele prepara a especificação, o planejamento e os artefatos relacionados.
- A validação automática verifica estrutura, referências e regras definidas nos scripts. Ela não consegue garantir sozinha que todas as decisões de negócio estejam corretas.
- A qualidade das sugestões depende das informações fornecidas, do agente utilizado e da revisão humana.
- A recomendação de stack não substitui a verificação atual da documentação oficial das tecnologias.
- Sem o Mermaid CLI (`mmdc`), a validação de diagramas é principalmente estrutural. A renderização completa e a geração de PDF podem exigir ferramentas adicionais, como Mermaid CLI e Chrome.
- Os arquivos exportados não criam registros remotamente por conta própria.

---

## 🤝 Como contribuir

Contribuições, correções e sugestões são bem-vindas. Antes de enviar uma mudança:

1. Explique o problema ou a melhoria proposta.
2. Atualize as instruções ou os testes pertinentes.
3. Execute os validadores ou o autoteste aplicável.
4. Revise o diff para garantir que não incluiu arquivos gerados ou alterações não relacionadas.
5. Abra um Pull Request com o contexto, o motivo da mudança e como ela foi verificada.

O repositório inclui um modelo de Pull Request em `.github/pull_request_template.md` e um fluxo de validação em `.github/workflows/validate-spec.yml`.

---

## 📚 Documentação adicional

- [Arquitetura do specMap](docs/ARQUITETURA.md)
- [Exemplo completo: Biblioteca Comunitária](examples/biblioteca-comunitaria/)
- [Instruções dos packs de stack](harness/stacks/README.md)
- [Cenários de avaliação do harness](evals/README.md)

---

<p align="center">
  <strong>specMap</strong> · Clareza antes do código. Decisões explícitas. Qualidade verificável.
</p>

### Exportar arquivos para o SoftTracker

Ao concluir o Gate 7 com todos os validadores aprovados, o fluxo gera automaticamente os artefatos de exportação: `backlog.json`, `backlog.yml` e os dois arquivos para integração com o SoftTracker na pasta `softtracker/` da raiz do projeto (`spec.yaml` e `especificacao.yml`). A exportação é feita a partir dos documentos reais de `.sdd`, não de arquivos de exemplo.

Os dois YAMLs são **formatos alternativos da mesma especificação**. Para inicializar o SoftTracker, passe apenas um deles por vez em `--spec` (recomendado: `spec.yaml`). Não passe os dois juntos: ambos representam os mesmos casos de uso e tarefas, então isso duplicaria os IDs no grafo do SoftTracker. `especificacao.yml` mantém também os campos de requisitos legados para consumidores que usam esse formato.

Critérios derivados de descrições textuais não recebem nomes inventados de classes, funções ou rotas. Eles são marcados para análise semântica pelo SoftTracker; por isso, a validação pode exibir avisos sobre ausência de artefato determinístico, mas não deve falhar por tipo de artefato inválido.

Para gerar apenas os dois arquivos do SoftTracker manualmente:

```bash
python harness/scripts/export/build_softtracker.py --sdd .sdd --saida softtracker
```

Os arquivos são derivados dos documentos do `.sdd`; edite as fontes e regenere as exportações em vez de alterar os YAMLs manualmente. Se algum validador do Gate 7 falhar, a exportação final não é executada até que os problemas sejam corrigidos.
