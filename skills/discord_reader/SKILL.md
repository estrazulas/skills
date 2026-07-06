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

## Entrega no WhatsApp

Por padrao o resultado vem para o chat atual. Para receber no WhatsApp:
/discord-reader --whatsapp
/discord-reader --resumo --whatsapp

O agente vai criar uma entrega unica via cron para o WhatsApp.

## Fluxo interativo de topicos

Quando o usuario pedir o resumo padrao (`--resumo`), o agente deve:

1. Executar o script com `--resumo` e mostrar o resultado
2. Perguntar: "Quer que eu detalhe algum topico quente? (1, 2, 3... ou 'nao')"
3. Se o usuario escolher um numero, pegar as mensagens BRUTAS do canal (sem --resumo) e fazer uma analise aprofundada especifica daquele topico, mostrando:
   - Quem falou o que (com timestamps)
   - A sequencia cronologica da discussao
   - Decisoes tomadas ou pontos em aberto
4. Apos detalhar, perguntar se quer detalhar outro topico ou se esta bom

## Canais favoritos

A skill mantem uma lista de canais favoritos em `.favorite_channels`.

### Listar canais salvos

```
/discord-reader --lista
```

Mostra os canais com numeros pra escolher.

### Escolher um canal salvo

```
/discord-reader 1
/discord-reader 2 --resumo
```

Passa o numero do canal da lista.

### Adicionar novo canal

```
/discord-reader --add-canal "https://discord.com/channels/S/G/C" "Nome do canal - Descricao"
```

Salva na lista pra usar depois.

### Canal padrao (FreeStuff)

Se nao passar nada, usa o primeiro da lista. Ou configure no .env:
```
DISCORD_DEFAULT_CHANNEL="ID_DO_CANAL"
```

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
| `--lista` | Lista canais favoritos |
| `--add-canal LINK DESCR` | Adiciona canal favorito |
| `--cron` | Modo cron: so mostra mensagens NAO lidas |

## Cron job automatico

Para monitorar um canal a cada 5h sem receber mensagens repetidas:

```
/discord-reader --cron
```

Na primeira execucao, o script salva um checkpoint (ultimo ID lido) e sai em silencio.
Nas proximas execucoes, ele pega SOMENTE mensagens depois daquele ID.
Se nao houver nada novo, nao entrega nada.

### Exemplo de cron criado

O job `Discord Headroom - monitor 5h` ja esta rodando:
- Canal: Headroom General
- Frequencia: a cada 5h
- Entrega: WhatsApp (se tiver novidades)
- Silencio se nao tiver nada novo
