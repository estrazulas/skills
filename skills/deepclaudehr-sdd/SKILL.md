---
name: deepclaudehr-sdd
description: Extensão do deepclaudehr-bridge para Spec-Driven Development com OpenSpec. O fluxo começa com /openspec (explore → propose → apply → archive) e o usuário define os requisitos via WhatsApp antes da implementação. O Hermes é orquestrador — nunca implementa.
tags:
  - coding
  - claude-code
  - sdd
  - openspec
triggers:
  - usuário pede spec-driven development, SDD, ou "com spec"
  - usuário menciona openspec + implementação
  - usuário quer definir requisitos antes de codar
---

# DeepClaudeHR SDD — Spec-Driven Development com OpenSpec

Extensão da skill `deepclaudehr-bridge`. Tudo que não está escrito aqui segue o fluxo base (spawn, monitoramento de stream, SendMessage, result). Esta skill adiciona apenas o que é específico do ciclo SDD com OpenSpec.

## Diferença do fluxo base

| | Base (`deepclaudehr-bridge`) | SDD (`deepclaudehr-sdd`) |
|---|---|---|
| Entrada | Prompt livre de código | Prompt de funcionalidade + `/openspec` |
| Fase 1 | — | **Explore**: Claude analisa codebase existente |
| Fase 2 | — | **Propose**: Claude especifica o que vai fazer |
| Fase 3 | Implementação direta | **Apply**: Claude implementa conforme spec aprovada |
| Fase 4 | — | **Archive**: Claude arquiva a spec concluída |
| Perguntas | Durante implementação | Principalmente na fase Propose (definição de escopo) |
| Permissão | `--permission-mode auto` | **Explore/Propose**: `deepclaudehr-ask` (acceptEdits) · **Apply/Archive**: `deepclaudehr` (bypassPermissions) |

## Pré-requisitos

Além dos pré-requisitos da skill base:
- Skills OpenSpec carregadas (`openspec-explore`, `openspec-propose`, `openspec-apply-change`, `openspec-archive-change`)
- `deepclaudehr-ask` instalado em `/usr/local/bin/deepclaudehr-ask` (wrapper que força `acceptEdits`)
- Projeto existente com codebase para o Explore analisar (se for projeto novo, pular Explore)

## Passos (delta sobre a base)

### 1. Classificar o ponto de entrada

**Critério**: fase OpenSpec inicial definida e prompt montado.

O usuário pode entrar em qualquer fase do ciclo:

| O que o usuário diz | Fase inicial | Prompt para o deepclaudehr |
|---|---|---|
| "explore o projeto X" ou "analisa o código" | Explore | `/opsx:explore` |
| "propõe uma feature Y" ou "spec para Z" | Propose | `/opsx:propose <funcionalidade>` |
| "implementa a spec Y" ou "aplica a mudança" | Apply | `/opsx:apply` |
| "arquiva a spec Y" | Archive | `/opsx:archive` |

Se o usuário não especificar, perguntar: "Qual fase do OpenSpec? Explore (analisar codebase), Propose (especificar feature), Apply (implementar), ou Archive (finalizar)?"

Se for funcionalidade nova em projeto existente, o padrão é **Propose → Apply**.

### 2. Informar o ciclo ao usuário

**Critério**: usuário sabe em qual fase está e o que esperar.

Antes de spawnar, informar:

```
🔍 SDD — OpenSpec: fase <nome>
📂 Projeto: <workdir>
🤖 Modelo: deepclaudehr pro (SDD sempre usa pro — especificação exige qualidade)
⏳ O Claude Code vai analisar o código e fazer perguntas de escopo.
   Responda aqui no WhatsApp quando ele perguntar.
```

### 3. Spawnar com o wrapper e prompt corretos

**Critério**: processo iniciado com o comando OpenSpec e modo de permissão adequado à fase.

**Wrapper por fase** (o `~/.claude/settings.json` tem `defaultMode: bypassPermissions` — usar o wrapper que força o modo correto):

| Fase | Wrapper | Permissão | Por quê |
|------|---------|-----------|---------|
| Explore | `deepclaudehr-ask pro` | acceptEdits | Precisa perguntar sobre escopo da análise |
| Propose | `deepclaudehr-ask pro` | acceptEdits | Precisa perguntar requisitos, campos, decisões |
| Apply | `deepclaudehr pro` | bypassPermissions | Implementação direta, sem interrupções |
| Archive | `deepclaudehr pro` | bypassPermissions | Operação mecânica, sem decisões |

Comando (exemplo para Propose):

```bash
cd <workdir> && deepclaudehr-ask pro -p --verbose \
  --output-format stream-json \
  --input-format stream-json \
  --brief \
  "/opsx:propose adicionar sistema de autenticação com JWT"
```

**SDD sempre usa modelo `pro`** — especificação de requisitos exige o melhor modelo. Não perguntar qual modelo; usar pro direto.

**Nota**: `deepclaudehr-ask` já injeta `--permission-mode acceptEdits` internamente, não é necessário passar na linha de comando.

### 4. Fase Explore (se aplicável)

**Critério**: Claude Code terminou a análise e reportou estrutura/achados.

Durante o Explore:
- O Claude Code vai ler arquivos, analisar estrutura, dependências
- Pode usar `SendMessage` para perguntar: "Qual parte do sistema te interessa mais?"
- O Hermes retransmite e aguarda resposta (mesmo fluxo do passo 4 da skill base)
- Ao final, o Claude Code entrega um resumo da arquitetura

### 5. Fase Propose

**Critério**: spec escrita, revisada e aprovada pelo usuário.

Esta é a fase com mais interação. O Claude Code vai:
1. Analisar o que existe (ou partir do Explore)
2. Fazer perguntas de escopo: "Quais campos no JWT?", "Refresh token?", "Quantas roles?"
3. Escrever a spec (arquivos em `openspec/changes/<slug>/`)
4. Apresentar a spec para revisão

O Hermes retransmite cada `SendMessage` ao usuário. O usuário define os requisitos respondendo.

Quando a spec estiver pronta, o Claude Code vai perguntar se pode prosseguir para Apply. O Hermes pergunta ao usuário: "Spec pronta. Prosseguir para implementação?"

### 6. Fase Apply

**Critério**: código implementado conforme spec.

Mesmo fluxo de implementação da skill base. O Claude Code segue a spec aprovada.

### 7. Fase Archive

**Critério**: spec arquivada, código commitado.

O Claude Code move a spec para `openspec/changes/archive/` e faz o commit.

## O que o Hermes NUNCA faz (mesmo que a base)

Mesmas restrições da skill base, reforçadas:
- **NÃO escreve código** — zero implementações
- **NÃO toma decisões de escopo** — "Quantas roles?" vai para o usuário
- **NÃO edita a spec** — território exclusivo do Claude Code
- **NÃO pula fases** — o usuário decide quando avançar de Propose para Apply

## Pitfalls (adicionais à base)

- **`bypassPermissions` global**: o `~/.claude/settings.json` tem `defaultMode: bypassPermissions`. Se usar `deepclaudehr` (sem `-ask`) nas fases Explore/Propose, o Claude NUNCA pergunta — as perguntas de escopo serão puladas. SEMPRE usar `deepclaudehr-ask` para Explore e Propose.
- **Propose sem Explore em projeto novo**: se o usuário nunca rodou Explore no projeto, o Claude Code pode não ter contexto suficiente. Sugerir Explore primeiro se o projeto for grande ou desconhecido.
- **Spec muito vaga**: se o usuário responder com respostas curtas ("sim", "ok", "tanto faz"), o Claude Code pode gerar uma spec incompleta. O Hermes deve incentivar respostas detalhadas na fase Propose.
- **Pular Archive**: após Apply, lembrar o usuário de rodar Archive para manter o histórico de specs limpo.
- **Trocar de wrapper entre fases**: ao transitar de Propose para Apply, o Hermes deve spawnar uma NOVA sessão com `deepclaudehr` (não `-ask`), passando o contexto da spec aprovada. Não reusar o mesmo processo.
