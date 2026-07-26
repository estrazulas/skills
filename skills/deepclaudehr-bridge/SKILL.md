---
name: deepclaudehr-bridge
description: Orquestra o deepclaudehr (Claude Code) a partir do Hermes com comunicação bidirecional via WhatsApp. O Hermes atua como orquestrador — NUNCA implementa código. Use quando o usuário pede para programar, criar apps, ou delegar tarefas de código ao Claude Code.
tags:
  - coding
  - claude-code
  - automation
triggers:
  - usuário pede para criar/implementar uma aplicação ou projeto
  - usuário menciona "claude code", "deepclaudehr", "programa isso", "codar"
  - tarefa de código delegada via WhatsApp
---

# DeepClaudeHR Bridge

O Hermes é o **orquestrador** — não o implementador. Quem escreve código, cria arquivos, e toma decisões técnicas é o deepclaudehr rodando no terminal. O Hermes apenas: recebe a tarefa, spawna o processo, monitora o stream, retransmite perguntas ao usuário, injeta respostas de volta, e reporta o resultado final.

## Modelos

| Comando | Modelo | Custo | Quando usar |
|---------|--------|-------|-------------|
| `deepclaudehr pro` | deepseek-v4-pro | $$$ | Apps completos, OpenSpec, tarefas complexas |
| `deepclaudehr` | deepseek-v4-flash | $ | Ajustes simples, testes, debugging rápido |

O Hermes pergunta ao usuário qual modelo usar se não estiver claro. O padrão é `pro` para tarefas que envolvem OpenSpec ou projetos novos completos.

## Pré-requisitos

- deepclaudehr instalado em `/usr/local/bin/deepclaudehr`
- Skills do OpenSpec em `~/.claude/skills/openspec-*` (já estão lá)
- WhatsApp conectado ao Hermes

## Passos

### 1. Receber e classificar a tarefa

**Critério de conclusão**: prompt de código extraído, modelo escolhido, diretório definido.

- Extrair o prompt de código da mensagem do usuário
- Se o usuário mencionar "pro" → `deepclaudehr pro`; se mencionar "barato"/"simples"/"flash" → `deepclaudehr`
- Se não especificar, perguntar: "Uso deepclaudehr pro (modelo top) ou normal (mais barato)?"
- Para projeto novo: `mkdir -p /tmp/claude-bridge/<slug>` e usar como workdir
- Para projeto existente: usar o diretório informado pelo usuário
- Informar o caminho ao usuário antes de começar

### 2. Spawnar o deepclaudehr

**Critério de conclusão**: processo background iniciado, session_id capturado do evento `init`.

Comando (ajustar `pro` conforme passo 1):

```bash
cd <workdir> && deepclaudehr pro -p --verbose \
  --output-format stream-json \
  --input-format stream-json \
  --brief \
  --permission-mode auto \
  "<prompt>"
```

Rodar com `terminal(background=true, notify_on_complete=true)`.

Flags essenciais:
- `--brief` → habilita `SendMessage` tool (mecanismo de pergunta ao usuário)
- `--output-format stream-json` + `--input-format stream-json` → comunicação bidirecional parseável
- `--permission-mode auto` → aprova npm install, git commit, etc. sem interromper

### 3. Monitorar o stream

**Critério de conclusão**: evento `type: "result"` recebido, ou `SendMessage` detectado.

Usar `process(action='poll')` para ler novas linhas do stdout. Cada linha é um JSON.

Três tipos de evento relevantes:

| Evento | Ação |
|--------|------|
| `type: "assistant"` com `text` | Enviar como atualização de progresso ao usuário |
| Tool call `name: "SendMessage"` | **Pergunta detectada** → ir para passo 4 |
| `type: "result"` | **Concluído** → ir para passo 5 |

Eventos de `thinking`, `tool_use` (que não SendMessage), `tool_result` são ignorados — não poluir o chat do usuário com detalhes internos.

### 4. Retransmitir pergunta ao usuário

**Critério de conclusão**: usuário respondeu, resposta injetada no stdin, processo continua.

Quando `SendMessage` aparece no stream:

1. Extrair `input.message` do tool call (é a pergunta que o Claude Code quer fazer)
2. Extrair também `input.summary` (resumo curto, se disponível)
3. Enviar ao usuário: "Claude Code pergunta: <mensagem>"
4. Aguardar resposta do usuário
5. Escrever no stdin do processo (`process(action='submit', data=...)`):

```json
{"type":"user","message":{"role":"user","content":"<resposta do usuário>"}}
```

6. Voltar ao passo 3 (continuar monitorando)

### 5. Reportar conclusão

**Critério de conclusão**: resultado final entregue ao usuário com métricas.

Extrair do evento `type: "result"`:
- `result` → texto final de resposta
- `total_cost_usd` → custo em dólares
- `duration_ms` → duração total
- `num_turns` → número de turnos
- `is_error` → se true, reportar o erro

Formato da mensagem ao usuário:

```
✅ deepclaudehr concluiu (X turnos, Ys, US$ Z)

<resultado>

Arquivos em: <workdir>
```

## O que o Hermes NUNCA faz

- **NÃO escreve código** — zero implementações, zero patches, zero Write/Edit
- **NÃO toma decisões técnicas** — se o Claude Code perguntar "React ou Vue?", a pergunta vai para o usuário, não para o Hermes
- **NÃO interpreta o stream além do necessário** — só extrai SendMessage e result; thinking/tool_use internos são ignorados
- **NÃO modifica arquivos do projeto** — o workdir é território exclusivo do deepclaudehr

## Pitfalls

- **SendMessage vs texto comum**: o Claude Code pode usar `SendMessage` tool (parseável) ou incluir a pergunta no texto da resposta. Monitorar ambos. Se o texto contiver "?" e o tom for de pergunta ao usuário, retransmitir.
- **`--verbose` obrigatório**: `--output-format stream-json` sem `--verbose` falha com erro.
- **Stdin precisa de newline**: ao escrever JSON no stdin, garantir `\n` no final (o `process(action='submit')` já adiciona).
- **Timeout em tarefas longas**: apps completos podem levar 5-10 minutos. O `notify_on_complete=true` cuida disso, mas monitorar com `poll` periódico para SendMessage.
- **Primeira linha é stderr**: deepclaudehr imprime `model=deepseek-v4-flash` no stderr antes do stream JSON começar. Ignorar essa linha.
- **Permissões residuais**: `--permission-mode auto` cobre a maioria, mas `rm -rf` ou `git push --force` podem gerar `permission_denials` no evento `result`. Se acontecer, reportar ao usuário.

## Verificação

- [ ] deepclaudehr spawnou e o stream JSON está fluindo
- [ ] SendMessage tool calls são detectados e retransmitidos ao usuário
- [ ] Respostas do usuário são injetadas corretamente e o Claude Code continua
- [ ] Resultado final inclui custo (USD), duração e caminho dos arquivos
- [ ] Hermes não escreveu nenhuma linha de código
