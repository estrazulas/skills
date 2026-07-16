# Skills Repo — Instruções

## Regra de ouro: symlinks

Toda skill nova ou modificada neste repo deve ser referenciada como symlink em **dois** lugares:

```bash
ln -s /home/estrazulas/git/skills/skills/<categoria>/<skill> ~/.claude/skills/<skill>
ln -s /home/estrazulas/git/skills/skills/<categoria>/<skill> ~/.hermes/skills/<skill>
```

- **Claude Code**: `~/.claude/skills/` — skills disponíveis no Claude Code
- **Hermes**: `~/.hermes/skills/` — skills disponíveis no Hermes Agent

## Workflow

1. Criar/modificar skill em `skills/<categoria>/<skill>/SKILL.md`
2. Criar/verificar symlink em `~/.claude/skills/<skill>`
3. Criar/verificar symlink em `~/.hermes/skills/<skill>`

## Estrutura

```
skills/
├── requisitos/       # Skills de engenharia de requisitos
│   ├── criar-mermaid/
│   ├── criar-prd/
│   ├── refinamento-demanda/
│   └── refinamento-demanda-grill/
├── ...               # Outras categorias
```
