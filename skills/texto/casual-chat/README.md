# casual-chat

Rewrite text into informal, casual English — real dev group chat style. No AI patterns, no polish, no corporate tone.

## What it does

Takes any text (English or translated from other languages) and rewrites it to sound like a real person typing in a dev/tech Discord/Telegram group chat. Strips all the AI tells: no capitalization, no formal grammar, no robotic politeness, no over-explaining. Short messages. Casual slang. The way people actually talk.

## How to invoke

```
/casual-chat <your text here>
```

Also triggers on phrases like "write like the group", "translate to casual English", "make it sound human", "informal mode", "chat style".

## Example

**Input:** "Hello! I noticed that when running the proxy with code-aware mode enabled, the compression ratio seems to be lower than expected. Has anyone else experienced this issue? I'd appreciate any guidance you can provide."

**Output:**
anyone else getting low compression with proxy --code-aware? mine barely does anything. not sure if its my setup or what

## See also

- [`SKILL.md`](./SKILL.md) — full LLM-facing instructions
- [Skills README](../../README.md) — repo overview
