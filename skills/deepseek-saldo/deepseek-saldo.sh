#!/bin/bash
# deepseek-saldo.sh — consulta saldo DeepSeek via API
# Uso: bash deepseek-saldo.sh
# A chave DEEPSEEK_API_KEY deve estar exportada no ambiente
# (ex: no ~/.bashrc: export DEEPSEEK_API_KEY="sk-...")

set -euo pipefail

if [ -z "${DEEPSEEK_API_KEY:-}" ]; then
  # Fallback: tenta ler do .bashrc
  if [ -f "$HOME/.bashrc" ]; then
    KEY=$(grep -E "^export DEEPSEEK_API_KEY=" "$HOME/.bashrc" | head -1 | sed 's/^export DEEPSEEK_API_KEY=//' | tr -d '"'"'"')
    if [ -n "$KEY" ]; then
      export DEEPSEEK_API_KEY="$KEY"
    fi
  fi
fi

if [ -z "${DEEPSEEK_API_KEY:-}" ]; then
  echo "❌ DEEPSEEK_API_KEY não encontrada. Exporte a variável no ~/.bashrc."
  exit 1
fi

BALANCE=$(curl -s -H "Authorization: Bearer $DEEPSEEK_API_KEY" https://api.deepseek.com/user/balance)
TOTAL=$(echo "$BALANCE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['balance_infos'][0]['total_balance'])" 2>/dev/null)

echo "☀️ Saldo DeepSeek - $(date '+%d/%m/%Y %H:%M')"
echo "Saldo disponível: \$${TOTAL} USD"
