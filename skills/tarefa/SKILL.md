---
name: tarefa
description: "Salva tarefas e ideias como .md numa pasta do usuário. Use quando o usuário disser 'salva isso nas tarefas', 'adiciona pra fazer', 'anota como tarefa', 'cria um todo', 'lembrete', 'não esquece de', '/tarefa', '/todo'. Também arquiva tarefas concluídas: 'arquiva a tarefa X', 'marca como feito', '/done'."
---

# Tarefa — salvar e arquivar ideias

## Quando usar

O usuário pede pra:
- **Salvar** uma tarefa nova: "salva isso nas minhas tarefas", "adiciona isso pra fazer", "cria um todo disso", "anota lá", "/tarefa", "/todo", "lembrete: ...", "não esquece de ..."
- **Arquivar** uma tarefa concluída: "arquiva a tarefa X", "marca como feito", "essa já foi", "/done"

## Primeira execução — perguntar o diretório

Se nenhum diretório de tarefas foi configurado antes, perguntar ao usuário:

> "Qual pasta você quer usar pras tarefas? (ex: ~/Desktop/tarefas-todo)"

Anotar o caminho e usar daí pra frente. Guardar o diretório escolhido no arquivo `~/.claude/skills/tarefa/.config` (só o path, uma linha).

Nas próximas execuções, ler desse arquivo.

---

## Ação 1: Salvar tarefa nova

1. Se `~/.claude/skills/tarefa/.config` não existe, perguntar o diretório
2. Entender o que é a tarefa — pode ser uma ideia, um lembrete, um estudo futuro, um bug pra resolver
3. Criar um nome curto pro arquivo (kebab-case, sem acentos, max 40 chars) que resuma o assunto
4. Salvar em `<diretorio-configurado>/<nome-curto>.md`

### Ação 1b: Copiar plano e conteúdo extra referenciado

**SEMPRE que a tarefa fizer referência a um plano ou documento externo,** copiar esse conteúdo para o diretório de tarefas também:

- Se existe um plano em `~/.claude/plans/<nome>.md` que foi mencionado na conversa, copiar para `<diretorio-configurado>/<nome-tarefa>-plano.md`
- Se existe conteúdo extra relevante (explicação longa, snippet, análise) que não coube na tarefa principal, salvar como `<diretorio-configurado>/<nome-tarefa>-extra.md`
- No arquivo da tarefa principal, referenciar com link relativo: `[plano detalhado](./<nome-tarefa>-plano.md)`
- Se o conteúdo extra já está em outro lugar (ex: `graphify-out/GRAPH_REPORT.md`), avaliar se vale copiar ou só linkar com caminho absoluto. Se for estável e pequeno, copiar. Se for grande ou regenerável, linkar.

**Por que isso importa:** o diretório de tarefas vira o "single source of truth" — quando o usuário for executar a tarefa no futuro, todo o contexto está lá, mesmo que o plano original em `~/.claude/plans/` já tenha sido sobrescrito ou apagado.

### Formato do arquivo

```markdown
# Tarefa: <título curto e descritivo>

## Contexto

<2-3 frases: de onde veio essa ideia, por que importa, o que estava sendo discutido quando surgiu>

## O que fazer

- [ ] <passo concreto 1>
- [ ] <passo concreto 2>
- [ ] <passo concreto 3>

## Notas

<links, referências, comandos, pessoas envolvidas, qualquer coisa relevante pra quando for executar>

---

Criado em: <data atual>
```

---

## Ação 2: Arquivar tarefa concluída

Quando o usuário diz que uma tarefa foi feita:

1. Listar os arquivos `.md` da pasta de tarefas (excluindo o `done/`)
2. Se o usuário especificou um nome, fazer **busca por similaridade** — procurar todos os `.md` cujo nome contenha qualquer parte do termo que o usuário disse
3. **Se a busca retornar mais de 1 arquivo, SEMPRE perguntar qual.** É erro grave arquivar sem confirmar quando há ambiguidade. Exemplo:

> "Achei 2 tarefas com 'graphify'. Qual você quer arquivar?"
> 1. estudo-graphify-claude-code.md
> 2. fork-graphify-proxy-apikey.md

4. Se retornar exatamente 1, pode arquivar direto
5. Se retornar 0, avisar que não encontrou e listar todas as disponíveis
6. Criar o diretório `done/` dentro da pasta de tarefas se não existir
7. Adicionar no final do arquivo: `Concluída em: <data de hoje>`
8. Mover o arquivo de `<diretorio>/arquivo.md` para `<diretorio>/done/arquivo.md`
9. Confirmar: "✅ Tarefa arquivada: `<diretorio>/done/arquivo.md>`"

Se o usuário não especificou nome nenhum, listar todas as ativas e perguntar:

> "Qual dessas você quer arquivar?"
> 1. fork-graphify-proxy.md
> 2. estudo-websockets.md
> 3. bug-login-timeout.md

---

## Regras

- O nome do arquivo é sempre curto: `tipo-assunto.md` (ex: `fork-graphify-proxy.md`, `estudo-websockets.md`, `bug-login-timeout.md`)
- Se a pasta configurada não existir, avisa que precisa criar
- Se já existir um arquivo com nome parecido, pergunta se quer sobrescrever ou complementar
- O conteúdo deve ser direto e acionável — checklist com `- [ ]`, não parágrafos longos
- Sempre incluir a data de criação no final
- Nunca inventar passos — só o que o usuário mencionou ou foi discutido na conversa
- Ao salvar: "✅ Tarefa salva: `<caminho-completo>`" e listar também os arquivos auxiliares copiados (plano, extra)
- Ao arquivar: adicionar "Concluída em: data" e mover pra `done/` (mover também os auxiliares: `-plano.md`, `-extra.md`)
