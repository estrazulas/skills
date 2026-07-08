---
name: quiz-diario-estudos
description: "Daily quiz cron job for estudos: randomly selects 5 unstudied files from the estudos folder, generates 5 varied questions, tracks history to avoid repeats"
---

# Quiz Diario de Estudos

## Overview

A daily cron job that:
1. Lists all .md files in `~/Desktop/conteudoestudos/`
2. Reads `.quiz-tracker.json` to know which topics were asked recently
3. **Randomly selects 5 files**, prioritizing topics NOT asked in the last 7 days
4. Reads the content of ONLY those 5 files
5. Generates 5 questions (one per file, mixed types)
6. Saves to `.quiz-today.json` and updates `.quiz-tracker.json`
7. Sends the quiz to the user via WhatsApp

## Cron job configuration

- Name: "Quiz diario estudos"
- Job ID: fbf9c3bac120
- Schedule: `30 13 * * *` (daily at 13:30)
- Model: deepseek-v4-flash
- Deliver: origin (whatsapp)

## How it works

The cron job prompt instructs the agent to:

### Step 1 — List all study files
Use `find ~/Desktop/conteudoestudos/ -name "*.md" | sort` to get all files

### Step 2 — Read the quiz tracker
Read `~/Desktop/conteudoestudos/.quiz-tracker.json` to see:
- What topics were asked (history)
- When each topic was last asked (last_topics)

### Step 3 — Randomly select 5 files
- Exclude files whose topics were asked in the last 7 days (from last_topics)
- If there are fewer than 5 eligible files, include some from 7+ days ago
- Randomly pick 5 from the eligible pool
- DO NOT read all files — only the selected ones

### Step 4 — Read ONLY the 5 selected files
Use `read_file` for each selected file. This keeps context small.

### Step 5 — Generate questions
- 5 questions, one per source file
- Mix types: multiple_choice, free_answer, true_false
- Each question tests REAL knowledge from that specific file

### Step 6 — Save outputs
- `.quiz-today.json`: today's questions
- `.quiz-tracker.json`: updated history and last_topics

### Step 7 — Deliver
Send formatted quiz message to WhatsApp

## Output format (no emojis, hyphen instead of dash)

```
== QUIZ DE ESTUDOS ==
Data: YYYY-MM-DD

Pergunta 1 de 5 - [TIPO] - [ARQUIVO]
[pergunta]
[alternativas se houver]

...

Respostas:
1. [RESPOSTA] — [explicacao curta]
```

## Key rules
- NEVER read all files — only the 5 selected ones
- Always check quiz-tracker first to avoid topic repetition
- Random selection, not sequential
