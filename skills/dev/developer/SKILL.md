---
name: developer
description: Launch a developer agent to implement features, fix bugs, or refactor code with test-driven discipline. Uses SOLID principles, dependency injection, and immutable patterns. Prompts stay in files, external calls are mocked in tests.
---

When invoked, delegate ALL implementation work to a specialized developer sub-agent via the Agent tool.

## How to Execute

Call `Agent` with:

- `subagent_type`: `"developer"`
- `description`: A short 3-5 word summary of the task
- `prompt`: The full implementation request — include the user's original ask plus any relevant context about files, constraints, or patterns already observed in the codebase

## What the Developer Agent Does

The developer agent is equipped for:

- **Node.js / TypeScript** implementation, bug fixes, and refactors
- **Test-Driven Development** — writes tests first, then implements
- **SOLID principles** and dependency injection patterns
- **Immutable data patterns** — avoids mutation where possible
- **LLM prompts in files** — never hardcoded inline
- **All external calls mocked** in test suites

## Guidelines

- Pass the user's exact request through to the agent prompt verbatim
- Include relevant file paths and architectural context so the agent doesn't have to re-discover them
- Let the agent return results directly — don't second-guess its work unless something looks off
