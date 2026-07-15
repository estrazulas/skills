# criar-prd

Gera PRDs (Product Requirements Documents) com pesquisa de codebase e mercado, entrevista estruturada, ADRs separados e catalogo de user stories.

## Quando usar

Voce tem uma ideia de feature e precisa de uma spec que qualquer dev (ou IA) consiga implementar sem perguntar mais nada. Exemplos:

- "Preciso de uma tela de renovacao de matricula"
- "Vamos adicionar exportacao de relatorios em PDF"
- "O cliente quer um portal do professor"

A skill conduz uma entrevista, pesquisa o que ja existe no codigo (e no mercado, se voce quiser), e gera dois arquivos prontos.

## O que ela gera

Dois arquivos na pasta `.compozy/tasks/<slug>/`:

| Arquivo | Para quem | Conteudo |
|---|---|---|
| `_prd.md` | Tech lead, dev, IA | PRD completo: contexto, user stories, edge cases, milestones, riscos |
| `_user_stories.md` | Dev, IA | Catalogo de historias com acceptance criteria e edge cases — insumo direto pra implementar |
| `adrs/adr-NNN.md` | Time, futuro | Cada decisao arquitetural vira um ADR numerado que outros PRDs podem referenciar |

## Como usar

```
/criar-prd
```

A skill vai te conduzir em 8 etapas. Voce so responde — uma pergunta por vez.

## Exemplo de sessao

### Entrada

> "Preciso de um sistema de notificacoes push no app. Usuario recebe alerta quando tem nova mensagem, nova curtida e quando alguem menciona ele."

### Etapa 0 — Detecta update mode

> (Nao existe PRD anterior → novo PRD)

### Etapa 1 — Um PRD ou varios?

> "Isso me parece uma feature so: sistema de notificacoes. Vou manter em um unico PRD."

### Etapa 2a — Codebase

A skill varre o codigo silenciosamente e traz:

> "Encontrei no codigo:
> - Ja existe `NotificationService` com suporte a email — push precisa ser adicionado
> - O app usa Firebase Cloud Messaging para Android
> - Preferencias de usuario ja tem tabela `user_preferences` com coluna `notifications_enabled`
> - O chat em tempo real usa WebSocket — podemos reutilizar o canal"

### Etapa 2b — Mercado (opcional)

> "Quer que eu pesquise o mercado antes? (s/n)"

Usuario: `s`

> "Pesquisei e encontrei:
> - Expectativa dos usuarios: notificacoes em < 30s apos o evento
> - Concorrentes agregam notificacoes similares em um unico card (ex: 'Joao e mais 3 curtiram sua foto')
> - Reclamacao comum: notificacao fantasma (clicou e nao tem conteudo) — precisa de deeplink funcional
> - Tendencia: silent notifications para eventos de baixa prioridade"

### Etapa 3 — Metricas (opcional)

> "Quer incluir criterios de aceite numericos? (s/n)"

Usuario: `s`

### Etapa 4-5 — Entrevista

> "Sobre o timing das notificacoes: os usuarios precisam receber o alerta em menos de 30 segundos ou 2 minutos e aceitavel? Recomendo < 30s para mensagens, < 2min para curtidas."

Usuario: `Concordo.`

> "Ok. Quando varios eventos acontecem em sequencia (ex: 5 curtidas na mesma foto), devemos:
> A) Enviar uma notificacao por evento **(recomendado para clareza)**
> B) Agregar: 'Joao e mais 4 curtiram sua foto' (recomendado para nao incomodar)
> C) O usuario escolhe nas preferencias
>
> Qual?"

Usuario: `B.`

> "Boa escolha — reduz spam de notificacoes. Isso impacta a US de preferencias: se e sempre agregado, nao precisa de configuracao por tipo de evento. Sigo."

... (continua ate esgotar as 10 dimensoes: contexto, problema, solucao, funcionalidades, decisoes, escopo negativo, criterios, milestones, riscos, referencias)

### Etapa 6 — ADRs

> "Registrei 2 decisoes como ADRs:
> - adr-001.md: Agregacao de notificacoes por evento — escolhido agrupamento por entidade
> - adr-002.md: Canal de entrega — Firebase Cloud Messaging reutilizando WebSocket existente para fallback"

### Etapa 7 — Arquivos gerados

```
.compozy/tasks/notificacoes-push/
├── _prd.md
├── _user_stories.md
└── adrs/
    ├── adr-001.md
    └── adr-002.md
```

### Etapa 8 — Revisao

> "Arquivos gerados. Quer revisar algum bloco antes de fechar?"

Usuario: `Muda o milestone 3 — inclui teste A/B antes de liberar pra 100%.`

> "Ajustado. Pronto."

## O que a skill NAO faz

- Nao escreve codigo nem da comandos tecnicos (ex: "crie a tabela X") — isso e pra implementacao
- Nao cria tasks/issues — o PRD e o insumo para outra skill fazer isso
- Nao define stack tecnologica — foca em comportamento do usuario, nao em implementacao
- Nao gera KPIs se voce nao pedir — metricas sao opcionais (Etapa 3)

## Dicas

- **Quanto mais vago o input, mais valor a skill entrega.** Se voce ja tem tudo especificado, ela so valida e organiza.
- **Responda "nao sei" sem medo.** A skill infere o mais provavel e marca "inferido — validar". Depois e so revisar.
- **Aproveite a pesquisa de mercado** quando for um produto voltado pra usuarios finais. Se for sistema legado interno, pule — nao faz sentido.
- **O catalogo de user stories** e o que voce vai colar no agente de codigo depois. Cada US ja tem edge cases — a IA nao precisa adivinhar.
