#!/usr/bin/env python3
"""Gera resumo das tarefas criadas/modificadas nas ultimas 48h.

Uso: python resumo-tarefas.py

Varre ~/Desktop/tarefas-todo/ por .md modificados nas ultimas 48h,
exclui done/, extrai titulo e objetivo, imprime mensagem formatada.
Pensado para rodar via cronjob com no_agent=True.
"""

import os
import glob
import time
from datetime import datetime, timedelta

TASKS_DIR = os.path.expanduser("~/Desktop/tarefas-todo")
HOURS_BACK = 48
CUTOFF = time.time() - (HOURS_BACK * 3600)


def get_task_files():
    """Retorna lista de .md fora de done/ modificados nas ultimas 48h."""
    all_md = glob.glob(os.path.join(TASKS_DIR, "*.md"))
    result = []
    for path in all_md:
        mtime = os.path.getmtime(path)
        if mtime >= CUTOFF:
            result.append(path)
    result.sort(key=os.path.getmtime)
    return result


def extract_title_and_context(path):
    """Extrai titulo e paragrafo de contexto/objetivo do arquivo."""
    basename = os.path.splitext(os.path.basename(path))[0]
    title = basename.replace("-", " ").title()
    context_lines = []
    reading_context = False
    title_found = False

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            # Titulo markdown "# Tarefa: ..." ou "# ..."
            if stripped.startswith("# ") and not title_found:
                title = stripped.lstrip("# ").strip()
                title_found = True
                continue

            # Secao de Contexto
            if stripped.startswith("## Contexto"):
                reading_context = True
                continue

            # Secao "O que fazer" ou "Notas" ou outra — para se estiver no contexto
            if reading_context and stripped.startswith("##"):
                break

            if reading_context and stripped:
                context_lines.append(stripped)

    # Se nao achou secao Contexto, pega as primeiras linhas nao vazias apos o titulo
    if not context_lines:
        with open(path, "r", encoding="utf-8") as f:
            after_title = False
            for line in f:
                stripped = line.strip()
                if stripped.startswith("# "):
                    after_title = True
                    continue
                if after_title and stripped and not stripped.startswith("#"):
                    context_lines.append(stripped)
                    if len(context_lines) >= 4:
                        break

    context = " ".join(context_lines[:4])
    return title, context


def format_message(tasks):
    """Monta a mensagem formatada."""
    today = datetime.now().strftime("%d/%m/%Y")
    lines = [f"== Tarefas dos ultimos 2 dias ({today}) ==", ""]

    for title, context in tasks:
        lines.append(f"📌 {title}")
        if context:
            lines.append(context)
        else:
            lines.append("(sem descricao disponivel)")
        lines.append("")

    lines.append(f"Total: {len(tasks)} tarefa(s) com alteracoes.")
    return "\n".join(lines)


def main():
    if not os.path.isdir(TASKS_DIR):
        print(f"Pasta de tarefas nao encontrada: {TASKS_DIR}")
        return

    files = get_task_files()
    if not files:
        today = datetime.now().strftime("%d/%m/%Y")
        print(f"Nenhuma tarefa nova ou alterada nos ultimos 2 dias ({today}).")
        return

    tasks = []
    for path in files:
        title, context = extract_title_and_context(path)
        tasks.append((title, context))

    print(format_message(tasks))


if __name__ == "__main__":
    main()
