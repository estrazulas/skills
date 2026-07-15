# refinamento-demanda-grill

Transforma demandas mal especificadas em questionarios estruturados. Voce cola o email vago do cliente, a skill conduz uma entrevista e gera dois arquivos prontos pra enviar: um tecnico (pra equipe) e um pro solicitante (linguagem acessivel, com wireframes).

> Inspirada nos conceitos de entrevista implacavel da `grill-me` do Matt Pocock.

## Quando usar

Voce recebeu uma demanda e nao tem todas as respostas. Exemplos:

- "Preciso de uma tela de renovacao de matricula" (quem acessa? qual o prazo? precisa de aprovacao?)
- "O sistema tem que gerar relatorio de notas" (quem ve? em qual formato? filtros?)
- "Vamos adicionar notificacoes push no app" (quais eventos? agrupadas ou individuais? silenciosas?)

A skill e para quando voce precisa **descobrir o que perguntar** — nao quando voce ja sabe tudo e so quer documentar.

## Como usar

```
/refinamento-demanda-grill
```

A skill conduz 9 etapas. Voce so responde — uma pergunta por vez.

## Exemplo de sessao

### Entrada

> "O sistema precisa permitir que o coordenador aprove ou rejeite a matricula de alunos que solicitaram revisao de nota."

### Etapa 1 — Fontes

> "Existe documentacao, wiki ou codigo que eu possa consultar? Se sim, me informa os caminhos."

Usuario: `Nao, so esse texto mesmo.`

### Etapa 2 — Issues

> "Existe base de issues ou tickets ja criada pra esse sistema? GitLab, Jira, GitHub?"

Usuario: `Nao.`

### Etapa 3 — Formato

> "Ao final vou gerar dois arquivos: tecnico (pra equipe) e solicitante (linguagem acessivel). Ok?"

Usuario: `Ok.`

### Etapa 4 — Demanda

> "Agora cola ou anexa o texto."

Usuario cola o texto.

### Etapa 5 — Espelho

> "Entendi que o coordenador precisa de uma tela onde visualiza solicitacoes de revisao de nota, consulta a nota original, a justificativa do aluno, e decide aprovar ou rejeitar. Esta fiel?"

Usuario: `Sim, mas tambem precisa poder pedir mais informacoes antes de decidir.`

> "Ajustado: o coordenador tambem pode solicitar esclarecimentos ao aluno antes da decisao final."

### Etapa 7 — Perguntas

> "Sobre quem pode solicitar revisao:
> A) Apenas o aluno que recebeu a nota **(recomendado)**
> B) Aluno + professor da disciplina
> C) Qualquer pessoa com vinculo
>
> Qual?"

Usuario: `A.`

> "Ok, A: apenas o proprio aluno. Isso impacta a pergunta sobre visibilidade — se so o aluno solicita, o professor nao precisa ver as revisoes pendentes. Ajusto."

> "Sobre o prazo para solicitar revisao:
> A) Ate 7 dias corridos apos a publicacao da nota **(recomendado)**
> B) Ate 15 dias
> C) Sem prazo — a qualquer momento
>
> Qual?"

Usuario: `A.`

...continua por detecao automatica de vaguidade e 15 dimensoes obrigatorias (ator, escopo, autorizacao, fluxo principal, alternativo, notificacao, auditoria...)

### Etapa 7.5 — Confirmacao

> "Resumo: 7 decisoes tomadas, 2 perguntas em aberto, glossario com 4 termos. Gero os arquivos?"

Usuario: `Sim.`

### Etapa 8 — Arquivos

```
questionamentos/revisao-nota/
├── revisao-nota_tecnico.md       ← linguagem interna, estimativas, glossario
└── revisao-nota_solicitante.md   ← linguagem acessivel, wireframes
```

## O que ela gera

| Arquivo | Para quem | Conteudo |
|---|---|---|
| `_tecnico.md` | Equipe de dev | Perguntas com alternativas, referencias a codigo, estimativas, glossario de dominio, mapa de dependencias |
| `_solicitante.md` | Cliente/solicitante | Perguntas faceis, alternativas com recomendacao, wireframes, zero jargao |

## Principais funcionalidades

- **Detecta 7 tipos de vaguidade** automaticamente (comparacao sem definicao, sujeito omitido, verbos sem estado...)
- **Checklist de 15 dimensoes** (ator, escopo, autorizacao, fluxo principal, alternativo, auditoria, encerramento...)
- **Alternativas com recomendacao** — cada pergunta sugere a melhor opcao pra acelerar a decisao
- **Cadeia de dependencias** — apos cada resposta, sinaliza quais perguntas futuras foram impactadas
- **Modo sabatina** — 3 "nao sei" consecutivos disparam uma entrevista mais incisiva
- **Glossario de dominio** — acumula termos durante a sessao e entrega no arquivo tecnico
- **Confirmacao final** — resume tudo antes de gerar os arquivos

## Instalacao

```bash
# Hermes (ja instalada)
/hermes/skills/refinamento-demanda-grill/

# Claude Code
ln -s ~/git/skills/skills/refinamento-demanda-grill ~/.claude/skills/refinamento-demanda-grill
```
