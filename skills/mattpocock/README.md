# Matt Pocock Skills

Repositorio original: https://github.com/mattpocock/skills

## Como instalar

```bash
npx skills@latest add mattpocock/skills
```

O CLI interativo pergunta quais skills e para quais agentes. Instala no diretorio corrente:
- `.claude/skills/<nome>/SKILL.md` (Claude Code)
- `.cursor/skills/<nome>/SKILL.md` (Cursor)
- etc.

## Skills instaladas (30 skills)

| Skill | Descricao |
|---|---|
| ask-matt | Roteador: recomenda qual skill usar para cada situacao |
| caveman-commit | Commits ultra-comprimidos, remove ruido |
| codebase-design | Vocabulario para desenhar modulos profundos (interfaces, seams, testabilidade) |
| code-review | Revisa mudancas em dois eixos: Standards (padroes) e Spec (atende o que foi pedido?) |
| composio-cli | Opera a CLI do Composio: busca tools, conecta contas, executa, escuta triggers |
| design-an-interface | Gera multiplos designs de interface para um modulo com sub-agentes paralelos |
| diagnosing-bugs | Loop de diagnostico para bugs dificeis e regressoes de performance |
| domain-modeling | Constroi e refina o modelo de dominio do projeto (linguagem ubiqua, ADRs) |
| ffmpeg | Processamento de video/audio com FFmpeg: conversao, compressao, extracao |
| find-skills | Ajuda a descobrir e instalar skills quando o usuario pergunta "como faco X?" |
| frontend-design | Guia para design visual intencional e distinto (tipografia, direcao estetica) |
| git-guardrails-claude-code | Bloqueia comandos git perigosos (push, reset --hard, clean) no Claude Code |
| grill-me | Entrevista implacavel sobre plano/design + Modo 2: questiona decisoes de codigo |
| grill-me-melhorada | **Adaptacao nossa** — grill-me + revisao invertida (Lucas Montano) |
| grill-with-docs | grill-me que tambem gera ADRs e glossario durante a entrevista |
| grilling | Prompt interno de entrevista: pergunta por pergunta ate entendimento mutuo |
| handoff | Compacta a conversa atual em documento de handoff para outro agente |
| implement | Implementa uma feature baseado em spec ou tickets |
| improve-codebase-architecture | Scaneia o codebase por oportunidades de melhoria, gera relatorio HTML, faz grill |
| prototype | Constroi prototipo descartavel para validar design (modelo de estado, UI) |
| qa | Sessao interativa de QA: usuario reporta bugs, agente abre issues no GitHub |
| research | Investiga topicos contra fontes primarias e salva como Markdown no repo |
| resolving-merge-conflicts | Resolve conflitos de merge/rebase em andamento |
| setup-matt-pocock-skills | Configura o repo para as skills: issue tracker, labels de triagem, dominio |
| tdd | Test-driven development: red-green-refactor, testes de integracao |
| teach | Ensina uma skill ou conceito novo dentro do workspace |
| to-spec | Transforma a conversa atual em spec e publica no issue tracker |
| to-tickets | Quebra plano/spec em tickets tracer-bullet com dependencias declaradas |
| triage | Move issues e PRs por uma maquina de estados de triagem (categorizar, verificar) |
| wayfinder | Planeja trabalho grande como mapa de tickets de decisao, resolve um por vez |
| writing-great-skills | Referencia para escrever skills de qualidade: vocabulario e principios |

## Skills adaptadas

| Skill | O que mudou |
|---|---|
| grill-me-melhorada | Adicionado Modo 2: durante geracao de codigo, a IA para em cada `if`/validacao/regra de negocio e questiona o dev com recomendacoes (revisao invertida do Lucas Montano) |

## Para usar no Hermes

O `skills.sh` NAO conhece o Hermes. Copie manualmente:

```bash
cp .claude/skills/<nome>/SKILL.md ~/.hermes/skills/<nome>/SKILL.md
```

Depois ajuste o frontmatter e triggers para o formato Hermes.
