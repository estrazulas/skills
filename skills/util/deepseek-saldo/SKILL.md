---
name: deepseek-saldo
description: "Consulta o saldo disponível na conta DeepSeek via API. Uso: /saldo ou 'ver saldo deepseek'."
---

# DeepSeek Saldo

Consulta o saldo disponível na conta DeepSeek via API pública (`https://api.deepseek.com/user/balance`).

## Como usar

- `/saldo` — mostra o saldo atual
- "ver saldo deepseek" — ativa a skill

## Requisitos

A chave `DEEPSEEK_API_KEY` deve estar disponível como variável de ambiente (exportada no `.bashrc`, `.zshrc` ou no `.env` do Hermes).

## Script

O script `deepseek-saldo.sh` faz a consulta. Leia a chave apenas de `$DEEPSEEK_API_KEY` — **nunca** hardcode.

```bash
bash ~/git/skills/skills/deepseek-saldo/deepseek-saldo.sh
```
