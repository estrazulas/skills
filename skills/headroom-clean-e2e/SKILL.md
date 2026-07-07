---
name: headroom-clean-e2e
description: Limpa usuários, chaves e times criados pelos testes e2e/admin do HeadroomGate sem afetar o admin real. Use após rodar testes que sujam o banco (crud_*, login_*, store_*, usage_*).
---

# Headroom Clean E2E — Limpeza de dados de teste

Remove todos os usuários, chaves API e times criados pelos testes de admin
(`tests/test_admin/test_api.py`, `tests/test_admin/test_e2e.py`,
`tests/test_admin/test_security.py`) sem afetar o usuário `admin` real,
suas chaves, ou as roles base.

## Prefixos de teste

Os testes usam `_unique(prefixo)` → gera `prefixo_<hex8>`. Todos os prefixos:

```
crud_admin_create, crud_admin_dup, crud_admin_list, crud_admin_mkteam,
crud_admin_req, crud_admin_teams, crud_admin_toggle, crud_cross, crud_dup,
crud_key_admin, crud_key_admin2, crud_key_user, crud_lead_dev, crud_lead_forbid,
crud_lead_list, crud_lead_noteam, crud_lead_ok, crud_list_a, crud_list_b,
crud_new_dev, crud_team_a, crud_team_b, crud_toggle, e2e-team, e2e-user,
login_access, login_logout, login_redir, login_revoked, login_store_valid,
login_valid, store_filter_a, store_filter_b, store_key_owner, store_scope_a,
store_scope_b, team_illegal, team_list_a, team_list_b, team_new,
usage_admin_noq, usage_admin_search, usage_admin_sess, usage_admin_sum,
usage_admin_top, usage_lead_scope, usage_lead_sum
```

Filtro seguro: `crud_`, `login_`, `store_`, `usage_`, `e2e-`, `team_list_`, `team_new_`, `team_illegal_`.

---

## Passo 1 — Diagnosticar (read-only)

```bash
source ~/.config/headroom/env

# Quantos usuários de teste existem?
headroom auth list-users --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
prefixes = ('crud_','login_','store_','usage_','e2e-')
test = [u for u in data if u['username'].startswith(prefixes)]
print(f'Test users: {len(test)}, Real users: {len(data) - len(test)}')
"

# Quantas chaves de teste?
headroom auth list-keys --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
prefixes = ('crud_','login_','store_','usage_','e2e-')
test = [k for k in data if k.get('username','').startswith(prefixes)]
print(f'Test keys: {len(test)}, Real keys: {len(data) - len(test)}')
"
```

---

## Passo 2 — Revogar via CLI (camada de aplicação)

```bash
source ~/.config/headroom/env

# Extrair e revogar todos os usuários de teste
headroom auth list-users --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
prefixes = ('crud_','login_','store_','usage_','e2e-')
for u in data:
    if u['username'].startswith(prefixes):
        print(u['username'])
" > /tmp/e2e_users.txt

while IFS= read -r user; do
  echo -n "Revoking $user... "
  headroom auth revoke-user "$user" 2>&1
done < /tmp/e2e_users.txt
```

---

## Passo 3 — Remover do Neo4j (camada de banco)

O `revoke-user` só desativa (soft-delete). Para remover os nós de fato:

```bash
source ~/.config/headroom/env
NEO4J_PASS="$NEO4J_PASSWORD"  # já exportada pelo source

# 3a. Deletar ApiKeys de teste
docker exec deepclaude_with_headroom-neo4j-1 cypher-shell -u neo4j -p "$NEO4J_PASS" "
MATCH (u:User)-[:OWNS_KEY]->(k:ApiKey)
WHERE u.username STARTS WITH 'crud_'
   OR u.username STARTS WITH 'login_'
   OR u.username STARTS WITH 'store_'
   OR u.username STARTS WITH 'usage_'
   OR u.username STARTS WITH 'e2e-'
DETACH DELETE k
RETURN count(k) AS deleted_keys
"

# 3b. Deletar Users de teste
docker exec deepclaude_with_headroom-neo4j-1 cypher-shell -u neo4j -p "$NEO4J_PASS" "
MATCH (u:User)
WHERE u.username STARTS WITH 'crud_'
   OR u.username STARTS WITH 'login_'
   OR u.username STARTS WITH 'store_'
   OR u.username STARTS WITH 'usage_'
   OR u.username STARTS WITH 'e2e-'
DETACH DELETE u
RETURN count(u) AS deleted_users
"

# 3c. Deletar Teams de teste
docker exec deepclaude_with_headroom-neo4j-1 cypher-shell -u neo4j -p "$NEO4J_PASS" "
MATCH (t:Team)
WHERE t.name STARTS WITH 'team_list_'
   OR t.name STARTS WITH 'team_new_'
   OR t.name STARTS WITH 'team_illegal_'
   OR t.name STARTS WITH 'e2e-'
DETACH DELETE t
RETURN count(t) AS deleted_teams
"
```

---

## Passo 4 — Verificar

```bash
source ~/.config/headroom/env

echo "=== Users (should be ONLY admin) ==="
headroom auth list-users

echo ""
echo "=== Keys (should be ONLY admin's 2 keys) ==="
headroom auth list-keys

echo ""
echo "=== Neo4j nodes ==="
docker exec deepclaude_with_headroom-neo4j-1 cypher-shell -u neo4j -p "$NEO4J_PASSWORD" "
MATCH (n) RETURN DISTINCT labels(n) AS labels, count(n) AS cnt ORDER BY cnt DESC
"
```

Estado esperado após limpeza:

| Nó | Esperado |
|---|---|
| `User` | 1 (`admin`) |
| `ApiKey` | 2 (`k_7031cd24e789` ativa + antiga revogada) |
| `Role` | 4 (admin, team_lead, developer, viewer) |
| `Team` | 0 |
| `RequestLog` | inalterado |

---

## O que NUNCA remover

- ❌ `admin` (username) — seu usuário
- ❌ `k_7031cd24e789` (hr_bdcc5de) — chave ativa usada no proxy e admin UI
- ❌ Roles base (admin, developer, team_lead, viewer) — criadas pelo `init-db`
- ❌ RequestLog — dados reais de uso

## Troubleshooting

| Erro | Causa | Solução |
|---|---|---|
| `AuthError: missing key 'credentials'` | Env não exportado | `source ~/.config/headroom/env` |
| `neo4j: command not found` | Cypher-shell não está no PATH | Use `docker exec <container> cypher-shell` |
| Container Neo4j parado | Docker compose down | `cd ~/git/deepclaude_with_headroom && docker compose up -d neo4j` |
