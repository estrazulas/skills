---
name: estudos
description: "Update studies: scans YouTube playlists (with topic filter), processes video directly via link or playlist, generates mind map in markdown + Mermaid diagram, saves to ~/Desktop/conteudoestudos/"
---

# Update Studies — YouTube → Mind Map

## Triggers

This skill has **three modes**, activated by different trigger phrases:

| Mode | Trigger phrase | Example |
|---|---|---|
| **Mode 1 — Normal playlist listing all available** | `update studies` | `update studies` |
| **Mode 2 — Playlist about a topic** | `update studies about <topic>` | `update studies about AI` |
| **Mode 3 — Direct video link, no playlist selection** | `update studies from video <url>`, `/estudos <url>`, or URL alone | `/estudos https://www.youtube.com/watch?v=abc123` |

> **Note:** Portuguese / Hermes-style triggers `atualizar estudos` and `/estudos` also work for all modes. Accept the URL **before or after** the trigger phrase (e.g. `<url> /estudos` or `/estudos <url>` both trigger Mode 3). Match all variants: `update studies`, `atualizar estudos`, `/estudos`.

---

IMPORTANT RULE:
**NEVER** process more than one video in the same conversation. One video per session.

## Mode 1 — Normal playlist

Classic interactive flow: choose playlist → choose video → process.

### Step 1 — Choose a playlist

1. List playlists from the channel using `mcp_youtube_management_youtube_get_playlists` with `channel_id=UCpFVltB83TFgign3AHLP6rA`
2. Show numbered playlists and ask: **"Which playlist do you want to use?"**

### Step 2 — Show recent videos

1. Get videos from the chosen playlist with `mcp_youtube_management_youtube_get_playlist_items`
2. Read `~/Desktop/conteudoestudos/.processed` to know which `video_id`s have already been processed
3. Show a numbered list with the most recent videos first, removing all the processed ones
4. Ask: **"Which video do you want to process? (number)"**

### Step 3 — Process the chosen video

1. Get the transcript — follow the **[Transcript Retrieval Fallback Strategy](#transcript-retrieval---fallback-strategy)** below
   - If there is **NO transcript** after trying both tools: say "⏭️ no transcript: <title>" and go back to step 2
2. **Confirmation** — show the video title and duration, then ask: **"Process this video? (y/n)"**
   - Wait for the user to respond. If "n" or "no", go back to step 2
3. Using the transcript, generate the mind map content (BOTH markdown mind map AND multiple small Mermaid treeview diagrams). Keep it in memory — do NOT save to disk yet. The output must include:

```markdown
# <Video Title>

**Link:** https://www.youtube.com/watch?v=<video_id>

## Mind Map
### <Main Topic 1>
- detail
- detail
### <Main Topic 2>
- detail

## Interesting Topics
- relevant concept or insight
- idea to explore later

## Tools & Technologies
- `tool` — brief usage description

## Resumo Geral
> One paragraph synthesizing the core insight of the video. What is the main takeaway? Why does it matter?

## Mind Map (Mermaid)

### Context Group 1
```mermaid
flowchart TD
    G1["Group Title"]
    G1 --> G1A["Node A"]
    G1 --> G1B["Node B"]
    G1B --> G1C["detail"]
```

&nbsp;

### Context Group 2
```mermaid
flowchart TD
    G2["Group Title"]
    G2 --> G2A["Node A"]
    G2 --> G2B["Node B"]
    G2 --> G2C["Node C"]
```
```

**Mermaid treeview rules:**
- Use **multiple ` ```mermaid ` blocks**, one per topic group, separated by `###` headings
- Between closing ` ``` ` and the next `###` heading, add `&nbsp;` on its own line — this forces MarkText and other editors to create separate rendering containers instead of merging blocks
- **Max 7 nodes per diagram** (hard limit — keeps them readable and prevents render failures)
- If a topic has 7+ sub-items, split into 2+ diagrams
- First line must be `flowchart TD`
- **Every node MUST have a UNIQUE ID with a 2-char prefix** per diagram (e.g. `PQ`, `HW`, `OL`). Never reuse plain `R` across diagrams. Avoid `IN` as prefix (reserved in Mermaid 11.x)
- Each node: `ID["Label"]` (unique ID + quoted label in straight ASCII quotes)
- Connections: `ID1 --> ID2` for parent-child
- See `references/mermaid-treeview-example.md` for a concrete approved example

**Mermaid label rules (critical — failures here cause blank/invisible diagrams):**
- **NO accented characters** — replace `á`→`a`, `é`→`e`, `í`→`i`, `ó`→`o`, `ú`→`u`, `ã`→`a`, `ç`→`c`, `â`→`a`, `ê`→`e`, `ô`→`o`, `ü`→`u`
- **NO special quotes** — use straight `"` (ASCII 34), not curly/typographic quotes
- **Keep labels short** — ideally under 25 characters, hard max 40
- **Avoid emoji in labels** ✅❌ may not render in Mermaid — describe status with text (e.g. "- APROVADO" or "- FALHOU")
- **NO question marks (?), exclamation marks (!), angle brackets (< >), dollar signs ($), forward slashes (/), tildes (~), commas (,), or colons (:)** in labels — these break Mermaid 11.x parsers
- **NO `+` or `-` at the very start of a label** — Mermaid may interpret them as operators
- **NO parentheses `(` `)`** in labels — can be confused with Mermaid syntax
- Good: `R["O problema: ficou bom nao e avaliacao"]`
- Bad: `R["O problema: 'Ficou bom' não é avaliação?!!!!"]` — has curly quotes, accent, special chars
- Bad: `R["Resposta: <45 tok/s>"]` — angle brackets break rendering
- Bad: `R["+B = +inteligencia"]` — plus at start is risky
- Bad: `R["78 tok/s - Rapido"]` — forward slash breaks rendering
- Bad: `R["Custo ~16k USD"]` — tilde breaks rendering

**Pre-save Mermaid verification checklist** — run this on the generated Mermaid blocks BEFORE saving the file:

1. Scan every `["..."]` label in all mermaid code blocks
2. Check for: `?` `!` `<` `>` `$` `/` `~` `,` `:` `(` `)` `á` `é` `í` `ó` `ú` `ã` `ç` in labels — if found, rewrite without them
3. Check labels starting with `+` or `-` — rephrase to avoid leading operators
4. Confirm every diagram has ≤7 nodes (hard limit)
5. Confirm ALL node IDs are unique across all diagrams — use a 2-char prefix per diagram
6. Confirm `&nbsp;` separator is present between closing ` ``` ` and next `###` heading
7. Run `python3 ~/.hermes/skills/estudos/scripts/verify-mermaid.py <output-path>` to auto-verify — fix any violations it reports
8. If any violation found, FIX IT in the content before writing the file

4. **Show and confirm before saving** — present the full mind map content (including the YouTube link at the top) to the user and explain what will happen:
   > \"Here's the generated mind map for **<title>** — shall I save it to `~/Desktop/conteudoestudos/<video-title>.md` and mark it as processed?\"

5. Wait for the user's response. If they say \"n\" or \"no\", ask what to change — do NOT save anything yet.
   - If they approve (\"y\", \"yes\", \"sim\", \"ok\"): save the file as `~/Desktop/conteudoestudos/<video-title>.md`

6. Save as `~/Desktop/conteudoestudos/<video-title>.md`
7. Add the `video_id` to `~/Desktop/conteudoestudos/.processed`
8. Confirm: "✅ <title> processed and saved!"

### Step 3b — Improve text for leigos (optional)

After saving the file and marking as processed, ask the user **exactly** this question:

> "Deseja que eu melhore o texto do arquivo com exemplos e explicacoes mais faceis para leigos usando o modelo DeepSeek v4 Pro? (s/n)"

- If they say "s", "sim", "yes", "y":
  1. Read the saved file
  2. Download the transcript again from the video (you still have the `video_id`)
  3. Switch the session model to `deepseek-v4-pro` (provider will be determined by current config)
  4. Regenerate the file with:
     - Same core content and structure (topicos, diagramas Mermaid, tabelas, resumo geral)
     - **Texto mais fluido e didatico** — linguagem simples, analogias do dia a dia
     - **Exemplos concretos pra cada conceito** — situacoes que um leigo consegue visualizar
     - Menos jargão técnico, mais explicacoes
     - Mantenha os diagramas Mermaid (com as mesmas regras de labels sem acentos)
  5. Replace the file content (overwrite)
  6. Confirm: "✅ Texto melhorado com DeepSeek v4 Pro!"

- If they say "n", "nao", "no", skip this step

### Step 4 — Clear context and continue

After confirming the video was saved, **always** end with this exact message:

> ✅ `<title>` saved to `~/Desktop/conteudoestudos/`
> 🧹 **Type `/new` to clear context**, then send `update studies` again to process the next one.

**NEVER** process more than one video in the same conversation. One video per session.

---

## Mode 2 — Playlist with topic filter

When the user specifies a topic (e.g. `update studies about AI`, `update studies about blockchain`), follow the Mode 1 flow with the adaptations below.

### Topic extraction

From the trigger `update studies about <topic>`, extract the topic. Examples:
- `update studies about AI` → topic = `AI`
- `update studies about machine learning` → topic = `machine learning`
- `update studies about autonomous agents` → topic = `autonomous agents`
- Also match Portuguese: `atualizar estudos de IA` → topic = `IA`

### Step 1 — Choose a playlist

Same as Mode 1: list playlists, ask the user to pick one.

### Step 2 — Filter videos by topic

1. Get videos from the chosen playlist with `mcp_youtube_management_youtube_get_playlist_items`
2. Read `~/Desktop/conteudoestudos/.processed`
3. **Filter videos**: keep only those whose **title** contains the given topic (case-insensitive). Match flexibly:
   - `AI` should match `AI`, `Artificial Intelligence`, `Inteligência Artificial`, `IA`
   - `machine learning` should match `machine learning`, `ML`, `aprendizado de máquina`
   - `agents` should match `agents`, `agent`, `agentes`, `agente`
   - Use obvious variations and common synonyms in both English and Portuguese
4. If **no video** matches the topic:
   - Say: `⚠️ No videos about "<topic>" found in playlist "<name>".`
   - Go back to Step 1 for the user to choose another playlist
5. Show the numbered list **only with topic-matching videos**, marking ✅ and 🆕 as in Mode 1
6. Ask: **"Which video do you want to process? (number)"**

### Steps 3 and 4

Same as Mode 1.

---

## Mode 3 — Direct video via link

When the user provides a direct link (e.g. `update studies from video https://www.youtube.com/watch?v=abc123`, `/estudos https://youtu.be/abc123`, or just a bare URL like `https://www.youtube.com/watch?v=abc123`), **skip playlist selection** entirely and go straight to processing.

**URL may appear before or after the trigger** — e.g. `<url> /estudos` or `/estudos <url>`. If a URL is present anywhere in the message, treat it as Mode 3 regardless of word order.

### Extracting the video_id

From the trigger message, find the URL. Parse the `video_id`:
- `https://www.youtube.com/watch?v=<video_id>` → extract `<video_id>`
- `https://youtu.be/<video_id>` → extract `<video_id>`
- `https://www.youtube.com/watch?v=<video_id>&list=...` → extract only `<video_id>`
- Any other format: try extracting with regex `[?&]v=([^&]+)` or `youtu\.be/([^?&]+)`

If unable to extract the `video_id`, respond:
> `⚠️ Could not extract video ID from the URL. Please send the link in the format https://www.youtube.com/watch?v=<id> or https://youtu.be/<id>`

### Direct processing

1. Get video metadata with `mcp__youtube-management__youtube_get_video` for the title (use `video_id` parameter)
2. Get the transcript — follow the **[Transcript Retrieval Fallback Strategy](#transcript-retrieval---fallback-strategy)** below
   - If there is **NO transcript** after trying both tools: say `⏭️ no transcript for video <video_id>. Cannot process this one.`
3. Generate the mind map content using the same format as Mode 1 (including the YouTube link at the top). Keep it in memory — do NOT save to disk yet.
4. **Show and confirm before saving** — present the full mind map content:
   > "Here's the generated mind map for **<title>** — shall I save it to `~/Desktop/conteudoestudos/<video-title>.md` and mark it as processed?"
5. Wait for the user's response. If they say "n" or "no", ask what to change — do NOT save anything yet.
   - If they approve ("y", "yes", "sim", "ok"): save the file and proceed
6. Save as `~/Desktop/conteudoestudos/<video-title>.md`
7. Add the `video_id` to `~/Desktop/conteudoestudos/.processed`
8. Confirm: "✅ `<title>` processed from direct link and saved!"
9. End with the context cleanup message:

> ✅ `<title>` saved to `~/Desktop/conteudoestudos/`
> 🧹 **Type `/new` to clear context**, then send `update studies` again to process the next one.

**NEVER** process more than one video in the same conversation. One video per session — even in direct mode.

---

## Transcript Retrieval — Fallback Strategy

Two different MCP servers provide transcript access. If one fails, try the other. **Always try both before giving up.**

### Tool A — `mcp__youtube-transcript__get-transcript` (try first)

- Parameter: `url` (full YouTube URL or youtu.be short URL)
- Optional: `lang` (language code, e.g. `"pt"`, `"en"`)
- Known failure mode: returns `"Video unavailable"` even for valid, accessible videos
- If it fails → move to Tool B

### Tool B — `mcp__youtube-management__youtube_get_transcript` (fallback, more robust)

- Parameter: `video_id` (just the 11-char ID, not the full URL)
- Optional: `language` (language code, e.g. `"pt"`, `"en"`)
- **Key advantage**: when transcript exists but not in the default language, it returns an error listing the available languages (e.g. `"No transcript available in language 'en'. Available languages: pt"`)
- If you get the "available languages" hint → retry with the listed language

### Recommended cascade

```
1. mcp__youtube-transcript__get-transcript(url=<full_url>)
   ↓ fails with "Video unavailable"?
2. mcp__youtube-transcript__get-transcript(url=<youtu.be short URL>)  ← try alternate URL format
   ↓ fails?
3. mcp__youtube-management__youtube_get_transcript(video_id=<id>)
   ↓ error lists available languages (e.g. "Available languages: pt")?
4. mcp__youtube-management__youtube_get_transcript(video_id=<id>, language=<available_lang>)
   ✅
```

> **IMPORTANT:** Tool B's `language` parameter is **required** when the video's transcript is not in English — even if you omit it and get the "available languages" error, you MUST retry with the correct language.

### Real example (video `hh6N9knL_Ng`)

| Step | Tool | Params | Result |
|---|---|---|---|
| 1 | `mcp__youtube-transcript__get-transcript` | `url=https://www.youtube.com/watch?v=hh6N9knL_Ng` | ❌ Video unavailable |
| 2 | `mcp__youtube-transcript__get-transcript` | `url=https://youtu.be/hh6N9knL_Ng` | ❌ Video unavailable |
| 3 | `mcp__youtube-management__youtube_get_transcript` | `video_id=hh6N9knL_Ng` | ⚠️ "Available languages: pt" |
| 4 | `mcp__youtube-management__youtube_get_transcript` | `video_id=hh6N9knL_Ng, language=pt` | ✅ Full transcript |

---

## Tools

| Tool | Usage |
|---|---|
| `mcp_youtube_management_youtube_get_playlists` | List channel playlists |
| `mcp_youtube_management_youtube_get_playlist_items` | Get videos from a playlist |
| `mcp_youtube_management_youtube_get_video` | Get video metadata (Mode 3) |
| `mcp__youtube-transcript__get-transcript` | Get transcript (Tool A — try first, use `url` + optional `lang`) |
| `mcp__youtube-management__youtube_get_transcript` | Get transcript (Tool B — fallback, use `video_id` + optional `language`) |

## Rules

- **NEVER** process more than one video in the same conversation. One video per session.
- **Always use** `channel_id=UCpFVltB83TFgign3AHLP6rA` for playlists (Modes 1 and 2)
- **Always read** `.processed` first to show correct status
- **Always save** `.md` to `~/Desktop/conteudoestudos/`
- Videos without transcripts: notify and offer another choice (Modes 1 and 2) or report as not possible (Mode 3)
- **Mode 2**: be flexible in topic matching — expand to synonyms and common variations (both English and Portuguese)
- **Mode 3**: skip all playlist interaction entirely
- **Always**: one video per session, end by asking user to `/new` after each processing
- **Trigger matching**: accept English (`update studies`), Portuguese (`atualizar estudos`), and Hermes-prefix (`/estudos`) trigger phrases for all modes
