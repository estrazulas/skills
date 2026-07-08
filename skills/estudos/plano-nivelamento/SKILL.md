---
name: plano-nivelamento
description: "Creates progressive learning plans combining multiple YouTube videos into leveled paths with timestamps. User says 'plano de nivelamento', 'nivelamento', 'criar um plano'."
---

# Plano de Nivelamento — Multi-Video Learning Path

Combina múltiplos vídeos do YouTube em níveis progressivos de aprendizado, cada um com timestamps e links diretos.

## Triggers

- `plano de nivelamento`
- `nivelamento`
- `criar um plano de estudos`
- `roteiro de estudos` (com múltiplos vídeos)

## Format Rules (CRITICAL)

O usuário rejeita conteúdo com cara de "gerado por IA". Siga estritamente:

- **ZERO emojis** no arquivo de saída. Nada de 📺 ▶ ⏱ ✅ ❌.
- **ZERO travessões longos (—)**. Use hífens normais (-) ou dois-pontos.
- **Um vídeo por nível** sempre que possível. Se o usuário reclamar de "vai e volta" entre vídeos no mesmo nível, reestruture.
- **Timestamps como links diretos:** `[MM:SS](https://youtu.be/<id>?t=SSS)`. Para lives: `https://www.youtube.com/live/<id>?t=SSS`.
- **Tabelas com timestamps** quando o nível tem múltiplos subtópicos — permite pular direto.
- **Tom de conversa entre devs**, não de documentação corporativa.
- **Committar no git local** de `~/Desktop/conteudoestudos/` após salvar.

## Estrutura do Arquivo

```markdown
# Plano de Nivelamento: <tema>

<resumo: quantos vídeos, duração total>

---

Lista dos vídeos usados (título, canal, link)

---

## Nível 1 — <título curto>
**Video X - [título](link com timestamp) [MM:SS]**
<parágrafo explicando o que cobre>
<tabela com timestamps se tiver subtópicos>
**~X minutos**

## Nível 2 — ...
...

## Ordem Recomendada
<progressão textual>

**Total: ~XhXX de vídeo**

---

## Para o Tech Lead (ou equivalente)
<notas práticas>
```

## Workflow

1. **Entender o pedido**: quais vídeos, qual audiência (devs, devops, etc.), qual progressão desejada
2. **Propor estrutura**: apresentar os níveis ANTES de gerar o arquivo, pedir feedback
3. **Buscar timestamps**: usar `mcp_youtube_management_youtube_get_video` para metadados, e a biblioteca Python `youtube_transcript_api` para timestamps precisos via `execute_code()`
4. **Gerar arquivo**: um nível por vídeo, progressão do básico ao avançado
5. **Salvar e commitar** em `~/Desktop/conteudoestudos/`

## Buscando Timestamps Precisos

Quando o vídeo tem descrição com capítulos, os timestamps já vêm nos metadados. Senão:

```python
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
transcript = api.fetch('<video_id>', languages=['pt'])
segs = list(transcript)
# seg.start = segundos, seg.text = texto
```

Busque palavras-chave no transcript para achar onde cada tópico começa. Formate o timestamp em segundos no link (`?t=SSS`).

## Pitfalls

- O transcript MCP (`mcp__youtube-transcript__get-transcript`) quebra com `AttributeError: 'list_transcripts'`. Sempre use a biblioteca Python direto.
- Lives do YouTube usam URL diferente: `https://www.youtube.com/live/<id>`.
- O usuário detecta padrões de IA (emojis, travessões, estrutura repetida, "O que você vai aprender:") e rejeita. Varie a estrutura entre níveis.
- Se o vídeo referenciado for de DevOps mas a audiência for de devs, busque vídeo complementar de outro autor para a parte prática.
- Nunca referencie dois vídeos diferentes no mesmo nível sem aprovação explícita do usuário.
