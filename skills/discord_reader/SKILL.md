---
name: discord-reader
description: "Le as ultimas mensagens de um canal do Discord e opcionalmente gera resumo com IA. Uso: /discord-reader [canal] [--resumo]"
---

# Discord Reader — Leitor de canais

Le as ultimas mensagens de qualquer canal do Discord que voce tenha acesso, usando o token salvo no `.env`.

## Como usar

### Com o canal padrao (FreeStuff)

```
/discord-reader
```

Mostra as ultimas 24h de mensagens do canal configurado no `.env`.

### Com resumo

```
/discord-reader --resumo
```

### De outro canal

```
/discord-reader https://discord.com/channels/SERVIDOR/CANAL
/discord-reader https://discord.com/channels/12345/67890 --resumo
```

### Com token novo (se o salvo expirou)

```
/discord-reader --token "MTA5MjI4NTM3MzA2MTg4Njg5Ng.Gb..." --resumo
```

## Como renovar o token

Quando o token expirar (o script vai mostrar "Token invalido ou expirado"):

1. Abra https://discord.com/app no navegador e faca login
2. F12 > aba Network
3. Clique em qualquer requisicao (ou F5 pra recarregar)
4. Em Request Headers, procure o campo `authorization`
5. Copie o valor e atualize no `.env` da skill:
   ```
   DISCORD_TOKEN="token_novo_aqui"
   ```
6. Salve o arquivo

## Como configurar outro canal padrao

Edite `.env` na pasta da skill e altere:

```
DISCORD_DEFAULT_CHANNEL="ID_DO_CANAL"
```

O ID esta no link do canal: `discord.com/channels/SERVIDOR/CANAL` — o ultimo numero.

## Estrutura de arquivos

```
~/git/skills/skills/discord_reader/
├── SKILL.md              # Esta skill
├── discord-reader.py     # Script principal
├── .env                  # Token e config (GITIGNORED)
└── .env.example          # Exemplo para outros usuarios
```

## Script

O script `discord-reader.py` esta na mesma pasta. Aceita:

| Parametro | Descricao |
|-----------|-----------|
| `--canal URL` | Link do canal do Discord |
| `--token TOKEN` | Token (sobrescreve .env) |
| `--resumo` | Gera resumo com IA |
| `--horas N` | Janela de horas (padrao: 24) |
| `--ultimas N` | Ultimas N msgs (padrao: 50) |
