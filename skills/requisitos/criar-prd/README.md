# criar-prd

Gera PRDs (Product Requirements Documents) prontos pra implementacao. Voce descreve uma feature, a skill entrevista voce, pesquisa o que ja existe no codigo, e entrega um PRD completo + catalogo de user stories + ADRs.

> Melhorias desenvolvidas em conjunto com conceitos da skill `cy-create-prd` do framework Compozy (pesquisa de codebase, business focus, ADRs separados, user-story catalog, update mode).

## Quando usar

Voce tem uma ideia de feature e precisa de uma spec que qualquer dev (ou IA) consiga implementar sem perguntar mais nada. Exemplos:

- "Preciso de um sistema de notificacoes push no app"
- "Vamos adicionar exportacao de relatorios em PDF"
- "O cliente quer um portal do professor com lancamento de notas"

A skill e para **criar a spec** — se voce ainda esta na fase de descobrir o que perguntar, use antes uma skill de refinamento de demanda.

## Como usar

```
/criar-prd
```

A skill conduz 8 etapas. Voce so responde — uma pergunta por vez.

## Exemplo de sessao

### Entrada

> "Preciso de notificacoes push no app. Usuario recebe alerta quando tem nova mensagem, nova curtida e quando alguem menciona ele."

### Etapa 0 — Detecta update mode

> (Nao existe PRD anterior → novo PRD)

### Etapa 1 — Um PRD ou varios?

> "Isso me parece uma feature so: notificacoes push. PRD unico."

### Etapa 2a — Codebase

A skill varre o codigo e traz:

> "Encontrei:
> - `NotificationService` com suporte a email — push precisa ser adicionado
> - Firebase Cloud Messaging configurado no Android
> - `user_preferences` ja tem `notifications_enabled`
> - WebSocket do chat pode ser reutilizado como fallback"

### Etapa 2b — Mercado (opcional)

> "Quer que eu pesquise o mercado? (s/n)"

Usuario: `s`

> "Pesquisei:
> - Usuarios esperam notificacao em < 30s
> - Concorrentes agrupam eventos similares ('Joao e mais 3 curtiram')
> - Reclamacao comum: clicou na notificacao e nao abriu nada — deeplink e essencial"

### Etapa 3 — Metricas (opcional)

> "Quer incluir criterios numericos (baseline, meta, prazo)? (s/n)"

Usuario: `s`

### Etapa 5 — Entrevista

> "Sobre o timing: usuarios precisam de resposta em menos de 30 segundos ou 2 minutos e aceitavel?"

Usuario: `< 30s para mensagens, < 2min para curtidas.`

> "Otimo. Quando varios eventos chegam em sequencia (5 curtidas na mesma foto):
> A) Uma notificacao por evento
> B) Agregar: 'Joao e mais 4 curtiram' **(recomendado — reduz spam)**
> C) Usuario escolhe nas preferencias
>
> Qual?"

Usuario: `B.`

> "B: agregado. Isso implica que nao precisamos de configuracao granular por tipo de evento. Simplifica as preferencias."

...continua cobrindo contexto, problema, solucao, funcionalidades, decisoes, escopo negativo, criterios, milestones, riscos, referencias.

### Etapa 6 — ADRs

A skill registra decisoes como arquivos separados:

```
adrs/
├── adr-001.md  ← Agregacao de notificacoes por entidade
└── adr-002.md  ← Firebase + WebSocket como fallback
```

### Etapa 7 — Arquivos

```
.compozy/tasks/notificacoes-push/
├── _prd.md              ← PRD completo, 9 secoes
├── _user_stories.md     ← Catalogo de US com edge cases
└── adrs/
    ├── adr-001.md
    └── adr-002.md
```

### Etapa 8 — Revisao

> "Arquivos gerados. PRD com 5 user stories, 4 milestones, 2 ADRs. Quer revisar?"

Usuario: `Ajusta o milestone 3 — inclui teste A/B antes de liberar pra 100%.`

> "Ajustado."

## O que ela gera

| Arquivo | Para quem | Conteudo |
|---|---|---|
| `_prd.md` | Tech lead, dev, IA | PRD completo: contexto, user stories, edge cases, milestones, riscos, ADRs |
| `_user_stories.md` | Dev, IA | Catalogo de historias com acceptance criteria e edge cases varridos |
| `adrs/adr-NNN.md` | Time, futuro | Decisoes arquiteturais registradas, referenciveis por outros PRDs |

## Principais funcionalidades

- **Analisa escopo primeiro** — decide se e um PRD ou varios, um por vez ate aprovacao
- **Pesquisa codebase** — varre o que ja existe antes de perguntar (nunca pergunta o obvio)
- **Pesquisa mercado** — opcional, busca tendencias e concorrentes pra enriquecer as perguntas
- **Business focus** — toda pergunta e sobre experiencia do usuario, nao sobre implementacao
- **Metricas opcionais** — se quiser, criterios de aceite sao numericos (baseline, meta, prazo, responsavel)
- **ADRs em arquivos separados** — decisoes registradas como documentos independentes
- **Catalogo de user stories** — cada US com rules, edge cases e notas de implementacao
- **Milestones com criterio de conclusao** — 3-6 fases, cada uma com condicao + verificacao + aprovador
- **Update mode** — se o PRD ja existe, atualiza preservando secoes nao alteradas

## Instalacao

```bash
# Hermes (ja instalada)
/hermes/skills/criar-prd/

# Claude Code
ln -s ~/git/skills/skills/criar-prd ~/.claude/skills/criar-prd
```
