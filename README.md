# Claude Code — Skills & Agents Examples

This project demonstrates how to extend [Claude Code](https://claude.ai/code) with **custom skills** and **specialized agents**, following the open [agent skills ecosystem](https://skills.sh/).

## 📁 Project Structure

```
.
├── .agents/skills/          # Installed skill packages (managed by npx skills)
│   ├── caveman-commit/
│   ├── ffmpeg/
│   ├── find-skills/
│   ├── supabase/
│   └── supabase-postgres-best-practices/
├── .claude/
│   ├── agents/              # Claude-specific agent overrides
│   └── skills/              # Symlinked skills for Claude Code
├── .github/agents/          # Custom agent definitions
│   ├── developer.agent.md
│   ├── playwright-test-generator.agent.md
│   ├── playwright-test-healer.agent.md
│   └── playwright-test-planner.agent.md
├── .mcp.json                # MCP server configuration
├── seed.spec.ts             # Playwright seed file for test generation
├── skills-lock.json          # Lockfile for installed skill versions
└── video.mp4                # Sample media for ffmpeg demos
```

## 🎯 Skills

Skills are reusable packages that give Claude Code specialized knowledge, workflows, and tool integrations. They are installed via the `npx skills` CLI from [skills.sh](https://skills.sh/).

### Installed Skills

| Skill | Source | Installs | Description |
|---|---|---|---|
| **caveman-commit** | `juliusbrussee/caveman` | 115K+ | Ultra-compressed Conventional Commits generator. Subject ≤50 chars, body only when needed. |
| **ffmpeg** | `digitalsamba/claude-code-video-toolkit` | 3.7K+ | Video/audio processing: format conversion, resizing, compression, trimming, speed adjustment, and platform-specific optimization. |
| **find-skills** | `vercel-labs/skills` | — | Discover and install skills from the open agent skills ecosystem. |
| **supabase** | `supabase/agent-skills` | 96K+ | Supabase development guide: changelog awareness, verification discipline, API exposure, error recovery. |
| **supabase-postgres-best-practices** | `supabase/agent-skills` | 199K+ | PostgreSQL optimization playbook from Supabase: indexes, connection pooling, RLS, schema design, locking, and tuning. |

### Installing a Skill

```bash
# Search for skills
npx skills find <keyword>

# Install globally (available in all projects)
npx skills add <owner/repo@skill> -g -y

# Install locally (project-level)
npx skills add <owner/repo@skill> -y
```

## 🤖 Agents

Agents are specialized sub-agents with specific tools, models, and instructions. They are defined as markdown files with YAML frontmatter in `.github/agents/`.

### Available Agents

| Agent | Purpose |
|---|---|
| **developer** | Node.js + TypeScript coding agent. Implements features, fixes bugs, and refactors with TDD discipline using SOLID principles and dependency injection. |
| **playwright-test-generator** | Creates automated browser tests from test plan items using Playwright. |
| **playwright-test-healer** | Debugs and fixes failing Playwright tests by inspecting console messages, network requests, and page snapshots. |
| **playwright-test-planner** | Creates comprehensive end-to-end test plans for web applications by exploring pages interactively. |

### Agent Anatomy

Each agent file defines:

```markdown
---
name: agent-name
description: When to use this agent
tools: ['list', 'of', 'allowed', 'tools']
model: Claude Sonnet 4        # optional
mcp-servers:                   # optional
  server-name:
    type: stdio
    command: npx
---

## Mission
...
```

### How to Invoke an Agent

From within Claude Code, the agent is automatically invoked based on the `description` field when the task matches. You can also dispatch tasks to agents explicitly using the `Agent` tool.

## 🔌 MCP Configuration

The `.mcp.json` file configures Model Context Protocol servers, giving Claude Code access to external tools and data sources like Playwright for browser automation and Context7 for documentation.

## 🧪 Playwright Integration

The `seed.spec.ts` file serves as a starting point for Playwright test generation. The three Playwright agents work together:

1. **planner** explores the app and creates a test plan
2. **generator** writes individual test specs from plan items
3. **healer** debugs and fixes any failing tests

## 🎬 FFmpeg Examples

The project includes `video.mp4` (1080p, 60fps, 10s) as sample media. Example operations:

```bash
# Get video metadata
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4

# Convert to black & white
ffmpeg -i video.mp4 -vf "hue=s=0" video-bw.mp4

# Compress for web
ffmpeg -i video.mp4 -c:v libx264 -crf 26 -vf "scale=1280:720" video-web.mp4
```

## 📚 Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Agent Skills Ecosystem](https://skills.sh/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Playwright Documentation](https://playwright.dev/)

---

Built as part of the **Engenharia de Software com IA Aplicada** course — Module 03: MCP in Practice.
