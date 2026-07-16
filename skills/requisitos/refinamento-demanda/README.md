# refinamento-demanda

Transforma demandas mal especificadas em questionarios estruturados. Voce cola o email vago do cliente, a skill conduz uma entrevista e gera dois arquivos prontos pra enviar: um tecnico (pra equipe) e um pro solicitante (linguagem acessivel, com wireframes).

## Quando usar

Voce recebeu uma demanda e nao tem todas as respostas. Exemplos:

- "Preciso de uma tela de renovacao de matricula"
- "O sistema tem que gerar relatorio de notas"
- "Vamos adicionar notificacoes push no app"

A skill e para quando voce precisa **descobrir o que perguntar** — nao quando voce ja sabe tudo e so quer documentar.

## Como usar

```
/refinamento-demanda
```

A skill conduz 8 etapas. Voce so responde — uma pergunta por vez.

## Exemplo de sessao

### Entrada

> "O sistema precisa permitir que o coordenador aprove ou rejeite a matricula de alunos que solicitaram revisao de nota."

### Etapa 1 — Fontes

> "Existe documentacao, wiki ou codigo que eu possa consultar?"

Usuario: `Nao.`

### Etapa 2 — Issues

> "Existe base de issues ou tickets? GitLab, Jira, GitHub?"

Usuario: `Nao.`

### Etapa 3 — Formato

> "Ao final vou gerar dois arquivos: tecnico e solicitante. Ok?"

Usuario: `Ok.`

### Etapa 4 — Demanda

> "Agora cola ou anexa o texto."

Usuario cola o texto.

### Etapa 5 — Espelho

> "Entendi que o coordenador precisa visualizar solicitacoes de revisao de nota, consultar a nota original, a justificativa, e decidir aprovar ou rejeitar. Esta fiel?"

Usuario: `Sim, mas tambem precisa poder pedir mais informacoes.`

> "Ajustado."

### Etapa 7 — Perguntas

> "Sobre quem pode solicitar revisao:
> A) Apenas o proprio aluno
> B) Aluno + professor
> C) Qualquer pessoa com vinculo
>
> Qual?"

Usuario: `A.`

> "Sobre o prazo para solicitar:
> A) 7 dias corridos apos publicacao da nota
> B) 15 dias
> C) Sem prazo
>
> Qual?"

Usuario: `A.`

...continua por mais 10-15 perguntas cobrindo ator, escopo, autorizacao, fluxo principal, alternativo, notificacao, auditoria, encerramento...

### Etapa 8 — Arquivos

```
questionamentos/revisao-nota/
├── revisao-nota_tecnico.md       ← linguagem interna, estimativas
└── revisao-nota_solicitante.md   ← linguagem acessivel, wireframes
```

## O que ela gera

| Arquivo | Para quem | Conteudo |
|---|---|---|
| `_tecnico.md` | Equipe de dev | Perguntas com alternativas, referencias a codigo, estimativas |
| `_solicitante.md` | Cliente/solicitante | Perguntas faceis, wireframes, zero jargao |

## Principais funcionalidades

- **Detecta 7 tipos de vaguidade** automaticamente (comparacao sem definicao, sujeito omitido, verbos sem estado...)
- **Checklist de 15 dimensoes** (ator, escopo, autorizacao, fluxo principal, alternativo, auditoria, encerramento...)
- **Uma pergunta por vez** — nunca empilha, espera sua resposta
- **Perguntas fechadas** — "A, B ou C?" em vez de perguntas abertas, pra agilizar
- **Tom neutro** — alternativas com pros e contras, sem empurrar solucao
- **Varredura de fontes** — se houver documentacao ou codigo, valida premissas antes de perguntar
- **Dois arquivos** — um tecnico pra equipe, um pro solicitante em linguagem acessivel

## Instalacao

```bash
# Hermes (ja instalada)
/hermes/skills/refinamento-demanda/

# Claude Code
ln -s ~/git/skills/skills/requisitos/refinamento-demanda ~/.claude/skills/refinamento-demanda
```
