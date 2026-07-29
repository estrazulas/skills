---
name: headroom-auth
description: Gerencia o sistema de auth do HeadroomGate — times, usuários, chaves API, roles e provider keys via Neo4j. Use para onboarding/offboarding de devs, criar times, gerar chaves, revogar acesso, ou inspecionar o estado do auth.
---

# Headroom Auth — Gerenciamento de Times, Usuários e Chaves

## Pré-requisito crítico

**Antes de qualquer comando `headroom auth`, as variáveis de ambiente do Neo4j precisam estar exportadas.** O CLI lê de `os.environ`, não do arquivo `~/.config/headroom/env`.

```bash
source ~/.config/headroom/env
```

Se esquecer, todos os comandos falham com:
```
neo4j.exceptions.AuthError: Unsupported authentication token, missing key `credentials`
```

---

## Comandos de Diagnóstico (read-only)

Use para inspecionar o estado atual antes de fazer mudanças.

### Listar usuários
```bash
source ~/.config/headroom/env
headroom auth list-users                # tabela formatada
headroom auth list-users --team admin   # filtrar por time
headroom auth list-users --json         # JSON para scripts
```

### Listar times
```bash
source ~/.config/headroom/env
headroom auth list-teams
headroom auth list-teams --json
```

### Listar roles
```bash
source ~/.config/headroom/env
headroom auth list-roles
```
Roles built-in: `admin` (Full access), `team_lead` (Gerencia próprio time), `developer` (Usa proxy com providers), `viewer` (Read-only).

### Listar chaves API
```bash
source ~/.config/headroom/env
headroom auth list-keys                  # todas as chaves
headroom auth list-keys --user admin     # filtrar por username
headroom auth list-keys --json           # JSON com key_id, prefix, status, expires_at
```

### Listar provider keys por role
```bash
source ~/.config/headroom/env
headroom auth list-provider-keys admin   # providers com key configurada
```

### Resolver identidade de uma chave
```bash
source ~/.config/headroom/env
headroom auth whoami   # prompt interativo para colar a key
```

---

## Comandos de Criação

### Criar time
```bash
source ~/.config/headroom/env
headroom auth create-team <nome-do-time>
```
Exemplos: `backend`, `frontend`, `data-science`, `mobile`.

### Criar usuário
```bash
source ~/.config/headroom/env
headroom auth create-user <username> --role <role> --team <team>
```
- `--role`: `admin`, `team_lead`, `developer`, ou `viewer`
- `--team`: nome do time (precisa existir — crie antes com `create-team`)
- Exemplo: `headroom auth create-user joao --role developer --team backend`

### Gerar chave API para um usuário
```bash
source ~/.config/headroom/env
headroom auth create-key <username>                    # expira em 90 dias (default)
headroom auth create-key <username> --ttl-days 365     # expira em 1 ano
```
**A chave é exibida UMA ÚNICA VEZ.** Salve imediatamente. Formato: `hr_<64 hex chars>`.

### Criar role customizada
```bash
source ~/.config/headroom/env
headroom auth create-role <nome> --description "<descrição>"
```

### Adicionar usuário a time existente
```bash
source ~/.config/headroom/env
headroom auth add-user-to-team <username> <team>
```
Use quando um dev muda de time ou precisa pertencer a múltiplos times.

### Configurar provider key para uma role
```bash
source ~/.config/headroom/env
headroom auth set-provider-key <role> <provider>
```
- Providers comuns: `anthropic`, `openai`, `deepseek`, `gemini`
- A CLI pede a key interativamente (não fica no histórico)
- Com `--stdin`: `echo "$KEY" | headroom auth set-provider-key admin anthropic --stdin`

---

## Comandos de Manutenção

### Revogar uma chave específica
```bash
source ~/.config/headroom/env
headroom auth revoke-key <key_id>    # key_id aparece no list-keys
```
A chave é desativada imediatamente. O proxy rejeita requisições com ela.

### Desativar usuário (revoga todas as chaves)
```bash
source ~/.config/headroom/env
headroom auth revoke-user <username>
```
Soft-delete: o usuário fica inativo mas não é removido do banco.

### Reativar usuário
```bash
source ~/.config/headroom/env
headroom auth reactivate-user <username>
```
Reativa o usuário. Chaves antigas continuam revogadas — gere novas com `create-key`.

### Gerar nova encryption key
```bash
source ~/.config/headroom/env
headroom auth generate-key
```
Gera uma Fernet key para `HEADROOM_ENCRYPTION_KEY`. Atualize `~/.config/headroom/env` com o valor gerado.

---

## Fluxos Completos (Receitas)

### Onboarding de novo desenvolvedor

```bash
source ~/.config/headroom/env

# 1. Criar time (se não existir)
headroom auth create-team backend

# 2. Criar usuário
headroom auth create-user joao --role developer --team backend

# 3. Gerar chave API
headroom auth create-key joao
# ← A chave hr_... aparece aqui. Copie e entregue ao dev.

# 4. Confirmar
headroom auth list-users --team backend
```

### Offboarding de desenvolvedor

```bash
source ~/.config/headroom/env

# Opção A: Revogar só uma chave (ex: chave vazada)
headroom auth list-keys --user joao    # descubra o key_id
headroom auth revoke-key k_XXXXXXXXXXXX

# Opção B: Desativar o usuário inteiro
headroom auth revoke-user joao
```

### Rotação de chave (chave vazada ou expirada)

```bash
source ~/.config/headroom/env

# 1. Gerar chave nova
headroom auth create-key joao
# ← Salve a nova hr_...

# 2. Revogar a antiga
headroom auth list-keys --user joao    # veja as chaves ativas
headroom auth revoke-key k_ANTIGA      # revogue a expirada/vazada

# 3. Atualizar config do dev com a nova chave
```

### Adicionar novo provider (ex: OpenAI)

```bash
source ~/.config/headroom/env

# 1. Configurar a key
headroom auth set-provider-key admin openai
# ← Cola a key quando solicitado

# 2. Verificar
headroom auth list-provider-keys admin
# Deve mostrar: openai  configured
```

---

## Troubleshooting

| Erro | Causa | Solução |
|---|---|---|
| `AuthError: missing key 'credentials'` | Env vars não exportadas | `source ~/.config/headroom/env` |
| `Connection refused` (porta 7687) | Neo4j não está rodando | Use `/headroom-doctor` para diagnosticar |
| `label does not exist` | `init-db` nunca foi executado | `headroom auth init-db -y` |
| `Team ... does not exist` | Time não foi criado antes do usuário | `headroom auth create-team <nome>` primeiro |
| `headroom: command not found` | CLI não instalada | Verifique `pipx list \| grep headroom` |

### Inicializar banco do zero

Se o Neo4j foi recriado (volume limpo) e o `init-db` nunca rodou:

```bash
source ~/.config/headroom/env
headroom auth init-db -y    # -y pula confirmação, é idempotente
```

Isso cria constraints, indexes e as 4 roles base. Pode rodar quantas vezes quiser.

---

## Referência Rápida

```
source ~/.config/headroom/env          # ← SEMPRE antes de qualquer comando

headroom auth list-users               # quem existe?
headroom auth list-teams               # quais times?
headroom auth list-roles               # quais roles?
headroom auth list-keys                # quais chaves? expiram quando?
headroom auth list-provider-keys ROLE  # quais providers têm key?

headroom auth create-team NOME
headroom auth create-user USER --role ROLE --team TEAM
headroom auth create-key USER [--ttl-days N]
headroom auth add-user-to-team USER TEAM
headroom auth set-provider-key ROLE PROVIDER
headroom auth create-role NOME --description DESC

headroom auth revoke-key KEY_ID
headroom auth revoke-user USER
headroom auth reactivate-user USER
headroom auth generate-key
headroom auth whoami
headroom auth init-db -y
```
