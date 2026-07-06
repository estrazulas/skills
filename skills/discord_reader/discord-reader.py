#!/usr/bin/env python3
"""
Leitor generico de canais do Discord via API.
Usa .env da mesma pasta para token e canal padrao.

Uso: python discord-reader.py [opcoes]

Opcoes:
  --canal URL      Link do canal (ex: https://discord.com/channels/S/G/C)
  --token TOKEN    Token de autorizacao (sobrescreve o .env)
  --resumo         Gera resumo com IA
  --horas N        Janela de horas (padrao: 24)
  --ultimas N      Ultimas N mensagens (padrao: 50)
"""

import sys
import json
import re
import os
import requests
import argparse
from datetime import datetime, timezone

API_BASE = "https://discord.com/api/v9"
LLM_API = "https://api.deepseek.com/v1/chat/completions"
LLM_MODEL = "deepseek-chat"


def load_env():
    """Carrega variaveis do .env na mesma pasta do script."""
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    envs = {}
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    envs[key.strip()] = val.strip().strip("\"'")
    return envs


def get_deepseek_key():
    """Tenta ler a chave da DeepSeek."""
    key = os.environ.get("DEEPSEEK_API_KEY")
    if key:
        return key
    try:
        with open(os.path.expanduser("~/.bashrc")) as f:
            for line in f:
                if "DEEPSEEK_API_KEY" in line and "export" in line:
                    return line.split("=", 1)[1].strip().strip("'\"")
    except:
        pass
    return None


def parse_channel_arg(arg):
    """Extrai o channel_id de um link ou ID direto."""
    match = re.search(r'discord\.com/channels/\d+/(\d+)', arg)
    if match:
        return match.group(1)
    if re.match(r'^\d{17,20}$', arg):
        return arg
    return None


def fetch_messages(channel_id, token, limit=50):
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    }
    url = f"{API_BASE}/channels/{channel_id}/messages?limit={limit}"
    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code == 401:
        print("ERRO: Token invalido ou expirado.", file=sys.stderr)
        print("Pegue um novo: F12 > Network > authorization header", file=sys.stderr)
        sys.exit(1)
    elif r.status_code == 403:
        print("ERRO: Sem permissao para este canal.", file=sys.stderr)
        sys.exit(1)
    elif r.status_code != 200:
        print(f"ERRO: HTTP {r.status_code}", file=sys.stderr)
        sys.exit(1)
    return r.json()


def filter_by_hours(messages, horas=24):
    agora = datetime.now(timezone.utc)
    filtradas = []
    for msg in messages:
        ts = msg.get("timestamp", "")
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            if (agora - dt).total_seconds() < horas * 3600:
                filtradas.append(msg)
        except:
            filtradas.append(msg)
    return filtradas


def format_messages(messages):
    linhas = []
    for msg in reversed(messages):
        ts = msg.get("timestamp", "")
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            ts_str = dt.strftime("%d/%m %H:%M")
        except:
            ts_str = ts
        author = msg.get("author", {}).get("global_name") or msg.get("author", {}).get("username", "?")
        content = msg.get("content", "")
        attachments = msg.get("attachments", [])
        embeds = msg.get("embeds", [])
        components = msg.get("components", [])

        comp_text = ""
        if components:
            def extract_comp(obj):
                text = ""
                if isinstance(obj, dict):
                    val = obj.get("content", "")
                    if val and isinstance(val, str):
                        text += val + "\n"
                    for v in obj.values():
                        if isinstance(v, (dict, list)) and v is not obj.get("content"):
                            text += extract_comp(v)
                elif isinstance(obj, list):
                    for item in obj:
                        text += extract_comp(item)
                return text
            comp_text = extract_comp(components)
            comp_text = re.sub(r'https?://\S+\.(png|webp|jpg)\S*(?:\s|$)', '', comp_text)
            comp_text = re.sub(r'\b\d{18,20}\b', '', comp_text)
            comp_text = re.sub(r'\S+==\s*', '', comp_text)
            comp_text = re.sub(r'image/\w+\s*', '', comp_text)
            comp_text = re.sub(r'\n{3,}', '\n\n', comp_text)
            comp_text = comp_text.strip()

        if not content and not attachments and not embeds and not comp_text:
            continue

        linha = f"[{ts_str}] {author}: {content or comp_text}"
        for att in attachments:
            linha += f"\n    + {att.get('filename', 'arquivo')}"
        for emb in embeds:
            if emb.get("title") or emb.get("description"):
                desc = (emb.get("description") or "")[:150]
                linha += f"\n    * {emb.get('title', '')} - {desc}"
        linhas.append(linha)

    return "\n".join(linhas)


def resumir(texto):
    api_key = get_deepseek_key()
    if not api_key:
        return "[Resumo indisponivel: chave DeepSeek nao encontrada]"

    prompt = f"""Voce e um assistente que resume conversas de Discord em portugues brasileiro.
Analise as mensagens abaixo e produza um resumo objetivo destacando:
1. Principais topicos discutidos
2. Decisoes ou encaminhamentos
3. Links ou recursos compartilhados
4. Perguntas nao respondidas

Mensagens do canal:
---
{texto[:8000]}
---

Resumo em portugues brasileiro:"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.3
    }

    try:
        r = requests.post(LLM_API, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"[Erro no resumo: HTTP {r.status_code}]"
    except Exception as e:
        return f"[Erro no resumo: {e}]"


def main():
    parser = argparse.ArgumentParser(description="Leitor de canais do Discord")
    parser.add_argument("--canal", help="Link do canal ou ID numerico")
    parser.add_argument("--token", help="Token de autorizacao (sobrescreve .env)")
    parser.add_argument("--resumo", action="store_true", help="Gera resumo com IA")
    parser.add_argument("--horas", type=int, default=24, help="Janela de horas (padrao: 24)")
    parser.add_argument("--ultimas", type=int, default=50, help="Ultimas N mensagens (padrao: 50)")
    args = parser.parse_args()

    # Carrega .env
    env = load_env()
    token = args.token or env.get("DISCORD_TOKEN")
    channel_id = None

    if args.canal:
        channel_id = parse_channel_arg(args.canal)
        if not channel_id:
            print(f"ERRO: Nao foi possivel extrair o ID do canal de: {args.canal}", file=sys.stderr)
            sys.exit(1)
    else:
        channel_id = env.get("DISCORD_DEFAULT_CHANNEL")

    if not token:
        print("ERRO: Token nao encontrado.", file=sys.stderr)
        print("Configure o .env na pasta da skill ou use --token", file=sys.stderr)
        sys.exit(1)

    if not channel_id:
        print("ERRO: Canal nao informado.", file=sys.stderr)
        print("Use --canal LINK ou configure DISCORD_DEFAULT_CHANNEL no .env", file=sys.stderr)
        sys.exit(1)

    messages = fetch_messages(channel_id, token, args.ultimas)
    if not messages:
        print("Nenhuma mensagem encontrada.", file=sys.stderr)
        return

    filtradas = filter_by_hours(messages, args.horas)
    if not filtradas:
        print(f"Nenhuma mensagem nas ultimas {args.horas}h.", file=sys.stderr)
        return

    texto = format_messages(filtradas)

    if args.resumo:
        print(resumir(texto))
    else:
        print(texto)
        print(f"\n>> {len(filtradas)} mensagens nas ultimas {args.horas}h <<", file=sys.stderr)


if __name__ == "__main__":
    main()
