---
name: resumo-tarefas
description: "Gera um resumo diario das tarefas criadas ou modificadas nos ultimos 2 dias. Usa um script Python standalone (sem LLM) para economizar tokens. Cron job configurado para rodar todo dia as 21h."
---

# Resumo de Tarefas

## Quando usar

- Quando quiser ver um resumo das tarefas criadas ou alteradas recentemente
- O cron job diario as 21h roda automaticamente

## Script

O script `scripts/resumo-tarefas.py` faz o trabalho:

1. Varre `~/Desktop/tarefas-todo/` por arquivos `.md` modificados nas ultimas 48h
2. Exclui o subdiretorio `done/`
3. Para cada arquivo, extrai o titulo e as primeiras linhas de contexto/objetivo
4. Monta uma mensagem formatada e imprime no stdout

O cron job usa `no_agent=True`, entao o stdout do script e entregue verbatim — zero tokens de LLM gastos.

## Estrutura

```
/home/estrazulas/git/skills/skills/resumo-tarefas/
├── SKILL.md
└── scripts/
    └── resumo-tarefas.py
```

## Links simbolicos

- `~/.hermes/skills/resumo-tarefas` -> `/home/estrazulas/git/skills/skills/resumo-tarefas/`
- `~/.hermes/scripts/resumo-tarefas.py` -> `/home/estrazulas/git/skills/skills/resumo-tarefas/scripts/resumo-tarefas.py`

## Cron job associado

ID: `04d8f35df31e` (se precisar alterar)
Schedule: `0 21 * * *` (todo dia as 21h)
