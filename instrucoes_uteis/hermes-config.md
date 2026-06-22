# Hermes Agent — Configuração de Providers e Modelos

> Última atualização: 2026-06-22  
> Equipamento: Desktop Ubuntu  
> Caminho base: `~/.hermes/`

---

## Providers configurados

| Provider | API | Custo | Default model |
|---|---|---|---|
| `deepseek` | api.deepseek.com (nativa) | pago (key própria) | `deepseek-v4-flash` |
| `openrouter/free` | openrouter.ai (proxy) | **grátis** | `nvidia/nemotron-3-super-120b-a12b:free` |

---

## Aliases (atalhos via `/model`)

| Alias | Provider | Modelo |
|---|---|---|
| `ds` | deepseek | `deepseek-v4-flash` |
| `ds-pro` | deepseek | `deepseek-v4-pro` |
| `free` | openrouter/free | `nvidia/nemotron-3-super-120b-a12b:free` |

### Outros modelos free disponíveis no `openrouter/free`

Qualquer um pode ser usado com `/model <id>`:

- `qwen/qwen3-coder:free` — Qwen3 Coder 480B (excelente pra código)
- `google/gemma-4-31b-it:free` — Gemma 4 31B
- `meta-llama/llama-3.3-70b-instruct:free` — Llama 3.3 70B
- `deepseek/deepseek-chat:free` — DeepSeek Chat grátis
- `openai/gpt-oss-120b:free` — OpenAI OSS 120B
- `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` — Nemotron Nano com reasoning

---

## Modelo padrão ao iniciar

Definido em `~/.hermes/config.yaml`:

```yaml
model:
  default: deepseek-v4-pro   # ← modelo que sobe com o gateway
  provider: deepseek         # ← provider padrão
```

Ou seja, ao ligar o PC e o gateway subir, o WhatsApp/CLI já responde com **DeepSeek V4 Pro**.

---

## Como trocar de modelo no dia a dia

**NÃO precisa reiniciar o gateway.** A troca é dinâmica e instantânea.

### Pelo WhatsApp
Mande o comando `/model` seguido do alias ou id:
```
/model ds        → DeepSeek Flash
/model ds-pro    → DeepSeek Pro
/model free      → Nemotron 120B grátis
/model qwen/qwen3-coder:free   → Qwen Coder grátis
```

### Pela CLI
```bash
cd ~/.hermes/hermes-agent
./venv/bin/python -m hermes_cli.main chat --provider deepseek --model deepseek-v4-flash -q "sua pergunta"
```

---

## Como adicionar novos modelos free

Editar `~/.hermes/config.yaml`:

1. Adicionar o id do modelo na lista `models:` do provider `openrouter/free`
2. Opcional: criar um alias em `model_aliases:`

Depois:
```bash
cd ~/.hermes/hermes-agent
./venv/bin/python -m hermes_cli.main gateway restart
```

---

## Como trocar o provider padrão permanentemente

Editar `~/.hermes/config.yaml`:

```yaml
model:
  default: nvidia/nemotron-3-super-120b-a12b:free   # modelo padrão novo
  provider: openrouter/free                          # provider padrão novo
```

Rodar `gateway restart` e o novo padrão assume.

---

## Arquivos relevantes

| Arquivo | Função |
|---|---|
| `~/.hermes/config.yaml` | Providers, modelos, aliases, parâmetros do agente |
| `~/.hermes/.env` | API keys (não versionar!) |
| `~/.hermes/gateway_state.json` | Status do gateway e plataformas conectadas |
| `~/.hermes/channel_directory.json` | Canais/conversas ativas por plataforma |
