---
prd_number: "NNN"
status: rascunho | pronto | em-progresso | concluido
priority: baixa | media | alta | critica
created: YYYY-MM-DD
issue: "#numero (opcional)"
depends_on: []
references: []
---

# PRD NNN: [Titulo descritivo da feature]

## 1. Contexto

[Descricao autocontida que permite implementar a feature sem consultar outros documentos. Incluir:]

- **Sistema/produto**: [em qual sistema esta feature se insere, stack tecnologica relevante]
- **Estado atual**: [o que ja existe, como funciona hoje]
- **Problema**: [qual dor esta feature resolve, quem e afetado, qual o impacto de nao resolver]
- **Achados da pesquisa**: [3-5 bullets do codebase + mercado, se disponivel]

[O objetivo e dar ao implementador (humano ou IA) contexto suficiente para tomar decisoes tecnicas alinhadas com o sistema existente.]

## 2. Solucao Proposta

### Visao geral

[3-5 bullets descrevendo a abordagem em alto nivel — o "como" sem entrar em detalhes de implementacao]

### Decisoes-chave

[Referencie os ADRs gerados — nao duplique o conteudo]
- ADR-001: [titulo] — [1 frase]
- ADR-002: [titulo] — [1 frase]

### Fora do escopo

- [O que NAO sera feito e por que]
- [O que NAO sera feito e por que]

## 3. Funcionalidades

### US01: [Titulo objetivo]

Como [persona], quero [acao], para [beneficio].

**Rules:**
- [Regra de negocio ou comportamento esperado]
- [Limite, restricao ou condicao]

**Edge cases:**
- [Situacao anomala] → [comportamento esperado]
- [Situacao anomala] → [comportamento esperado]

**Notas de implementacao:** (opcional)
- [Detalhe tecnico relevante que nao e obvio]

### US02: [Titulo objetivo]

Como [persona], quero [acao], para [beneficio].

**Rules:**
- [Regra de negocio ou comportamento esperado]

**Edge cases:**
- [Situacao anomala] → [comportamento esperado]

[Repetir para cada funcionalidade. Cada US deve ter pelo menos uma Rule e um Edge case.]

## 4. Visao de Arquitetura

[Diagrama de alto nivel mostrando o fluxo entre componentes/servicos. Marcar o que e novo vs. o que ja existe quando aplicavel.]

[Secao opcional — incluir apenas quando a feature envolver multiplos componentes ou integracoes.]

## 5. Criterios de Aceite

### Tecnicos

| Criterio | Metodo de verificacao |
|----------|----------------------|
| [requisito de performance, seguranca ou infra aplicavel a feature] | [como testar] |

### De negocio (se aplicavel — ver Etapa 3 da skill)

| Metrica | Baseline (fonte) | Meta | Prazo | Min. aceitavel | Responsavel |
|---------|-------------------|------|-------|-----------------|-------------|
| [nome] | [valor atual + de onde vem o dado] | [valor alvo] | [data ou periodo] | [threshold abaixo do qual a entrega falhou] | [quem mede] |

**Regras:**
- Baseline sem fonte confiavel deve ser marcado como "A levantar" com responsavel e prazo para obtencao
- Min. aceitavel define o ponto de corte entre sucesso e fracasso — sem ele, a meta e aspiracional, nao um criterio de aceite

## 6. Milestones

### Milestone 1: [Verbo + Substantivo]

**Objetivo:** [Uma frase descrevendo o valor entregue por este marco.]

**Funcionalidades:** US01, US02

- [ ] [Tarefa concreta referenciando a US]
- [ ] [Tarefa concreta referenciando a US]
- [ ] [Tarefa concreta referenciando a US]

**Criterio de conclusao:**
- Condicao: [o que precisa ser verdade para considerar concluido]
- Verificacao: [como confirmar — teste, deploy em staging, code review, demo]
- Aprovador: [quem da o OK — papel ou pessoa]

### Milestone 2: [Verbo + Substantivo]

**Objetivo:** [Uma frase.]

**Funcionalidades:** US03

- [ ] [Tarefa concreta referenciando a US]
- [ ] [Tarefa concreta referenciando a US]

**Criterio de conclusao:**
- Condicao: [o que precisa ser verdade para considerar concluido]
- Verificacao: [como confirmar]
- Aprovador: [quem da o OK]

[Repetir para 3-6 milestones no total. Cada milestone deve ser independentemente entregavel quando possivel.]

## 7. Riscos e Dependencias

| Risco | Impacto | Mitigacao | Status |
|-------|---------|-----------|--------|
| [descricao do risco] | Alto/Medio/Baixo | [plano de mitigacao] | Pendente/Monitorando/Mitigado |

**Dependencias:**

| Dependencia | Tipo | Status | Impacto se bloqueado |
|-------------|------|--------|----------------------|
| [sistema/equipe/PRD] | Interna/Externa | [estado atual] | [quais milestones sao afetados] |

## 8. Referencias

- [Descricao do recurso](link) — [por que e relevante]
- [Descricao do recurso](link) — [por que e relevante]

[Links para documentacao, issues, PRDs relacionados, APIs, designs, ou qualquer recurso externo que embasou decisoes ou e necessario para a implementacao.]

## 9. ADRs

- [ADR-001](adrs/adr-001.md): [titulo] — [1 frase]
- [ADR-002](adrs/adr-002.md): [titulo] — [1 frase]
