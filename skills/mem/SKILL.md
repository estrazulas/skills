---
name: mem
description: Lista e busca nas memórias persistentes do projeto
---

# Mem — Memórias Persistentes

Lista e busca nas memórias salvas via `memory_save` e arquivos `.md` no diretório de memórias do projeto.

## Uso

- `/mem` — lista todas as memórias salvas
- `/mem <termo>` — busca por um termo específico e exibe o conteúdo da primeira correspondência

## Script auxiliar

Para listar/buscar memórias via linha de comando:

```bash
bash ~/.claude/skills/mem/scripts/mem.sh [termo]
```

Ou use diretamente o comando `mem` se o script estiver no PATH.
