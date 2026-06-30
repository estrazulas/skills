---
name: headroom-doctor
description: Diagnostica problemas no proxy Headroom — verifica serviço systemd, containers Docker (Neo4j/Qdrant), portas, variáveis de ambiente, logs e endpoints de saúde. Use quando o proxy parou de responder, o deepclaudehr não conecta, ou o Claude Code reporta erros de auth.
---

# Headroom Doctor — Diagnóstico do Proxy

## Triggers

| Frase | Ação |
|---|---|
| `headroom caiu`, `proxy parou`, `headroom não conecta` | Diagnóstico completo |
| `diagnostica headroom` | Diagnóstico completo |
| `deepclaudehr não funciona` | Diagnóstico completo + verificação do wrapper |
| `headroom doctor` | Diagnóstico completo |

---

## Fluxo de Diagnóstico

Execute os passos abaixo **em ordem**, parando ao encontrar a causa raiz. Cada passo tem o comando exato e a interpretação do resultado.

### Passo 1 — Status do serviço systemd

```bash
systemctl --user status headroom.service --no-pager -l
```

**O que olhar:**
- `Active: active (running)` → ✅ serviço rodando, vá para Passo 2
- `Active: inactive (dead)` → serviço parado, tente iniciar: `systemctl --user start headroom.service`
- `Active: failed` → serviço crashou, vá para Passo 5 (logs)
- `Loaded: not-found` → serviço não instalado, rode `install.sh` novamente

### Passo 2 — Porta do proxy ouvindo

```bash
ss -tlnp | grep 8787
```

**O que olhar:**
- Saída com `0.0.0.0:8787` e `headroom` → ✅ proxy ouvindo
- Sem saída → proxy pode estar rodando mas sem bindar a porta, vá para Passo 5

### Passo 3 — Containers Docker (Neo4j + Qdrant)

```bash
cd ~/git/deepclaude_with_headroom && docker compose ps
```

**O que olhar:**
- Ambos com `Up` → ✅ vá para Passo 4
- Qualquer um com `Exited` → **causa mais comum de queda!** Suba com:

```bash
docker compose up -d
```

- `command not found: docker` → Docker não está no PATH ou não instalado
- Container `neo4j` com `Exited (0)` → desligamento limpo (alguém rodou `docker compose stop` ou o daemon reiniciou)
- Container `qdrant` com `Exited (143)` → recebeu SIGTERM (desligamento em cascata)

**Após subir os containers, aguarde o Neo4j ficar pronto (~10-15s):**
```bash
docker compose logs neo4j --tail 5
# Procure por "Started." no log
```

Depois reinicie o proxy para ele reconectar:
```bash
systemctl --user restart headroom.service
```

### Passo 4 — Portas dos containers ouvindo

```bash
ss -tlnp | grep -E '7687|6333'
```

**O que olhar:**
- `0.0.0.0:7687` → ✅ Neo4j Bolt ouvindo
- `0.0.0.0:6333` → ✅ Qdrant REST ouvindo
- Portas ausentes → containers subiram mas não bindaram (verifique logs do container)

### Passo 5 — Logs do proxy

```bash
journalctl --user -u headroom.service --no-pager -n 60
```

**Padrões críticos nos logs:**

| Padrão | Significado | Ação |
|---|---|---|
| `auth-middleware: Neo4j query failed ... Connection refused` | Neo4j não está ouvindo na 7687 | Voltar ao Passo 3 |
| `Failed to obtain server version ... qdrant` | Qdrant inacessível ou lento | Verificar container Qdrant |
| `MemoryMax=2G` atingido | Proxy comendo RAM demais | `systemctl --user restart headroom.service` |
| `ModuleNotFoundError: No module named 'headroom_auth'` | Plugin auth não instalado | `pipx inject headroom-ai headroom-auth` |
| `HEADROOM_API_KEY not set` | Env não carregado | Verificar Passo 6 |
| `exit-code` ou `failed` | Crash por outro motivo | Examinar as 20 linhas ao redor do erro |

### Passo 6 — Variáveis de ambiente

```bash
cat ~/.config/headroom/env
```

**Valores esperados:**
```
HEADROOM_API_KEY="hr_..."           # Deve começar com hr_
HEADROOM_ENCRYPTION_KEY="..."       # Base64, ~44 chars
HEADROOM_PROXY_URL="http://localhost:8787"
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="devpassword"
QDRANT_URL="http://localhost:6333"
```

**Problemas comuns:**
- `HEADROOM_API_KEY="YOUR_HEADROOM_API_KEY_HERE"` → placeholder, nunca foi configurado
- `HEADROOM_ENCRYPTION_KEY="YOUR_ENCRYPTION_KEY_HERE"` → placeholder, nunca foi gerado
- Arquivo não existe → setup incompleto, rode `install.sh` novamente
- Permissão errada → `chmod 600 ~/.config/headroom/env`

### Passo 7 — Health check HTTP

```bash
curl -s http://localhost:8787/health | python3 -m json.tool
```

**Resposta esperada:**
```json
{"status": "healthy", ...}
```

Se retornar erro ou vazio mas o serviço está `active` no Passo 1, o proxy pode estar em boot loop. Verifique os logs (Passo 5).

### Passo 8 — Wrapper deepclaudehr

```bash
ls -la ~/.local/bin/deepclaudehr
file ~/.local/bin/deepclaudehr
cat ~/.config/headroom/env | grep HEADROOM_API_KEY | head -1
```

**O que olhar:**
- Symlink quebrado → `ln -sf ~/git/deepclaude_with_headroom/files/deepclaude/deepclaudehr.sh ~/.local/bin/deepclaudehr`
- Script ausente → `sudo cp ~/git/deepclaude_with_headroom/files/deepclaude/deepclaudehr.sh /usr/local/bin/deepclaudehr`
- `HEADROOM_API_KEY` placeholder → bootstrap não concluído (veja seção "Auth Bootstrap")

---

## Cenários Comuns e Soluções

### Cenário A: "O proxy parou do nada"

**Causa mais provável:** Docker reiniciou e os containers não sobem automaticamente (não têm `restart: always`).

```bash
cd ~/git/deepclaude_with_headroom
docker compose up -d
sleep 5
systemctl --user restart headroom.service
```

### Cenário B: "Auth middleware — Neo4j connection refused"

O Neo4j caiu ou nunca foi iniciado.

```bash
cd ~/git/deepclaude_with_headroom
docker compose up -d neo4j
# Aguarde "Started." no log:
docker compose logs neo4j -f  # Ctrl+C quando aparecer "Started."
systemctl --user restart headroom.service
```

### Cenário C: "Qdrant version warning"

Qdrant não subiu corretamente ou está com versão incompatível.

```bash
cd ~/git/deepclaude_with_headroom
docker compose up -d qdrant
curl -s http://localhost:6333/healthz  # Deve retornar "ok"
```

### Cenário D: "HEADROOM_API_KEY placeholder — nunca bootstrapei"

O auth bootstrap nunca foi concluído. Execute (com Neo4j rodando):

```bash
# O export carrega todas as vars do env no shell atual — necessário para
# o CLI headroom auth conectar no Neo4j e acessar o HEADROOM_ENCRYPTION_KEY.
export $(grep -v '^#' ~/.config/headroom/env | xargs)
headroom auth init-db -y
headroom auth create-user admin --role admin --team admin
headroom auth create-key admin  # ← salva o hr_... gerado
headroom auth generate-key      # ← salva a chave gerada
headroom auth set-provider-key admin anthropic
# Edite ~/.config/headroom/env com as chaves geradas
systemctl --user restart headroom.service
```

> ⚠️ **Importante:** `export $(grep -v '^#' ~/.config/headroom/env | xargs)` é essencial antes de QUALQUER comando `headroom auth`. Sem isso, o CLI não tem `NEO4J_PASSWORD` nem `HEADROOM_ENCRYPTION_KEY` no ambiente e os comandos falham com `AuthError`.

### Cenário F: "headroom usage summary falha com Neo4j AuthError"

O CLI `headroom usage` **não** carrega automaticamente `~/.config/headroom/env`. Ele só lê `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` e `HEADROOM_API_KEY` do ambiente do shell. Sem essas vars, `NEO4J_PASSWORD` vira `""` (string vazia) e o Neo4j rejeita com:

```
neo4j.exceptions.AuthError: Unsupported authentication token, missing key `credentials`
```

O proxy **systemd** funciona porque o serviço tem `EnvironmentFile=~/.config/headroom/env` — o arquivo é carregado automaticamente. Mas o CLI roda no seu shell, não no systemd, então depende de você.

**Solução — carregue o env antes:**

```bash
source ~/.config/headroom/env && headroom usage summary
source ~/.config/headroom/env && headroom usage top
source ~/.config/headroom/env && headroom usage team admin
source ~/.config/headroom/env && headroom usage search "consulta"
```

> ⚠️ **Isso NÃO está documentado** no `headroom usage --help`, no README, nem no código fonte. O código (`usage/store.py` linha 36) usa `os.environ.get("NEO4J_PASSWORD", "")` — sem `source` no env, o fallback `""` quebra a autenticação.

### Cenário G: "headroom auth quebra com Neo4j AuthError ou HEADROOM_ENCRYPTION_KEY not set"

`headroom auth` é afetado pelo **mesmo problema** do `headroom usage`: o CLI **não** carrega `~/.config/headroom/env` automaticamente. Cada comando lê vars específicas do ambiente do shell:

| Comando | Var necessária | Erro se faltar |
|---------|---------------|----------------|
| QUAISQUER comando `auth` | `NEO4J_URI` + `NEO4J_USER` + `NEO4J_PASSWORD` | `AuthError: Unsupported authentication token, missing key 'credentials'` |
| `auth set-provider-key` | `HEADROOM_ENCRYPTION_KEY` (além das de Neo4j) | `HEADROOM_ENCRYPTION_KEY is not set` |
| `auth whoami`, `auth list-users --self` | `HEADROOM_API_KEY` ou `HEADROOM_AUTH_USER` | Falha de autenticação ou "not found" |

**Solução — sempre carregue o env antes:**

```bash
source ~/.config/headroom/env && headroom auth init-db -y
source ~/.config/headroom/env && headroom auth create-user joao --role developer --team backend
source ~/.config/headroom/env && headroom auth list-users
source ~/.config/headroom/env && headroom auth create-key admin
source ~/.config/headroom/env && headroom auth set-provider-key admin anthropic
source ~/.config/headroom/env && headroom auth whoami
source ~/.config/headroom/env && headroom auth generate-key
```

> 💡 O Cenário D usa `export $(grep ...)` que também funciona (inclusive para a mesma sessão), mas o `source` é mais simples e legível.

### Cenário E: "Symlink deepclaudehr quebrado"

```bash
# O repo correto é deepclaude_with_headroom (não deepclaude)
ln -sf ~/git/deepclaude_with_headroom/files/deepclaude/deepclaudehr.sh ~/.local/bin/deepclaudehr
```

---

## Resumo de Comandos Úteis

```bash
# Status completo de um comando
systemctl --user status headroom.service --no-pager -l

# Logs recentes
journalctl --user -u headroom.service --no-pager -n 40

# Containers
cd ~/git/deepclaude_with_headroom && docker compose ps
cd ~/git/deepclaude_with_headroom && docker compose up -d

# Portas
ss -tlnp | grep -E '8787|7687|6333'

# Health
curl -s http://localhost:8787/health | python3 -m json.tool

# Env
cat ~/.config/headroom/env

# Reiniciar tudo
cd ~/git/deepclaude_with_headroom && docker compose up -d && sleep 10 && systemctl --user restart headroom.service
```

---

## Regras

- Execute **sempre** os 3 primeiros passos (serviço → porta proxy → containers) para qualquer diagnóstico
- Se containers Docker estão `Exited`, essa é a causa raiz em 80% dos casos
- O docker-compose.yml **não** tem `restart: always` — após reboot do host ou do daemon Docker, os containers **não** sobem automaticamente
- O proxy (`headroom.service`) tem `Restart=on-failure`, então ele tenta re-subir se crashar — mas falha silenciosamente se Neo4j/Qdrant estiverem offline
- A unidade systemd bloqueia ranges de IP privados (`IPAddressDeny`) — o proxy alcança a internet mas NÃO alcança `localhost` via `127.0.0.1`? Verifique: o Docker expõe as portas em `0.0.0.0`, então o proxy acessa via rede Docker (`172.22.0.x`) e NÃO por `localhost`. Se mudar as portas do docker-compose de `0.0.0.0` para `127.0.0.1`, o proxy não conseguirá alcançar os containers.
- O proxy depende dos containers Docker para funcionalidade completa (auth + busca semântica), mas consegue iniciar sem eles — apenas reporta erros quando requisições autenticadas chegam
- Use `headroom_usage` skill para ver estatísticas de economia do proxy quando ele estiver saudável
- O CLI `headroom usage` **não** carrega `~/.config/headroom/env` automaticamente — sempre faça `source ~/.config/headroom/env && headroom usage ...` no shell. Se o erro for `AuthError: missing key credentials`, é esse o motivo.
