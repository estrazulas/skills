# Questionamentos ao Solicitante — [Título da demanda] (versão para o setor)

**Data:** DD/MM/YYYY
**Autor do parecer:** [nome]
**Público-alvo:** setor solicitante

## O que entendemos da sua demanda

[Resumo em linguagem clara, sem jargão. Enumera os grandes blocos do que foi pedido.]

## Decisões que tomamos juntos

Para cada bloco funcional, um sub-título com decisão em linguagem funcional:

### [Bloco X]

- Decisão 1 em linguagem acessível.
- Decisão 2 em linguagem acessível.

#### Como fica na tela (protótipo sugestivo)

Sempre que uma decisão envolver campos novos, fluxos condicionais de formulário, uploads ou selects, incluir um wireframe textual (ASCII art ou Markdown formatado) que mostre:
- Os inputs novos e seus rótulos
- Comportamento condicional (ex.: checkbox marcado → abre select)
- Feedback visual ao usuário (soma acumulada, mensagens de erro)

Exemplo de formato:

```
┌─────────────────────────────────────────────────┐
│ Critério de seleção: [ Análise Documental  ▼ ]  │
│                                                 │
│ ☑ Terá entrevista?                              │
│   Peso da análise documental: [ 60 ]%           │
│   Peso da entrevista:         [ 40 ]%           │
│   Calendário da entrevista:   [ Entrev. 2026 ▼] │
│                                                 │
│ ☐ Terá convocação para nivelamento?             │
│ ☑ Permitirá recursos?                           │
│   Calendário de recurso:      [ Recurso 01  ▼ ] │
└─────────────────────────────────────────────────┘
```

Regras:
- Não desenhe todas as telas do sistema, só as decisões que envolvem interação nova.
- Se o protótipo for extenso, quebre em blocos menores por seção.
- Use caixas ASCII simples (┌─┐│└─┘) para delimitar painéis.
- Use `[ texto ▼ ]` para selects, `[ ___ ]` para inputs, `☑`/`☐` para checkboxes, `○`/`●` para radio buttons, `[Botão]` para botões.

## O que ainda precisa de decisão do setor

Lista numerada das pendências, cada uma com contexto de negócio (não técnico) do que trava.

## Sugestões nossas

Recomendações em linguagem funcional — foco no impacto no processo/UX/decisão, sem detalhe técnico.

## O que muda na prática

Para cada ator do processo (candidato, coordenador, DEING, etc.), o que efetivamente será diferente.

## Próximos passos

Checklist funcional para o setor.
