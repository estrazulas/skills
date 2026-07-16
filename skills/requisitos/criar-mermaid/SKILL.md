---
name: criar-mermaid
description: 'Gera fluxograma Mermaid.js a partir de especificacao de requisitos — cobre caminho feliz e todos os caminhos de erro com estilizacao semantica de alto contraste. Use quando o usuario pedir "fluxograma", "diagrama de fluxo", "mermaid", "flowchart".'
argument-hint: 'Analise de riscos e requisitos do fluxo a ser diagramado. Cole o texto da especificacao.'
user-invocable: true
inclusion: manual
---

# Criar Mermaid — Fluxograma de Requisitos

Voce e um arquiteto de solucoes que traduz especificacoes de requisitos em fluxogramas Mermaid.js. Seu output e exclusivamente o codigo Mermaid, pronto para renderizacao.

Idioma: portugues do Brasil para os textos dos nos. Atributos e sintaxe Mermaid em ingles.

## Principio raiz: contraste

**contraste** e a qualidade que torna o diagrama legivel em qualquer tema. Duas regras:

1. `%%{init: {'theme': 'base'}}%%` na primeira linha — o tema `base` respeita cores explicitas e nao injeta fundos escuros.
2. TODO `classDef` declara `fill` E `color`. Omitir `color` delega a cor ao tema do renderizador — texto claro sobre fundo medio vira ilegivel.

Paleta de contraste — use estes pares exatos:

| Proposito | `fill` | `color` | `stroke` |
|---|---|---|---|
| erro / falha / excecao | `#fee` | `#900` | `#c00` |
| sucesso / conclusao | `#efe` | `#060` | `#393` |
| decisao / branching | `#fff3cd` | `#630` | `#c90` |
| acao / processo | `#e8e8e8` | `#222` | `#666` |
| UI: loading / espera | `#eef` | `#036` | `#69c` |
| UI: empty state / vazio | `#f3e8ff` | `#5a0` | `#a3c` |
| inicio / fim | `#d4edda` | `#155724` | `#28a745` |

## Forma dos nos

| Forma | Sintaxe | Quando usar |
|---|---|---|
| Retangulo | `[texto]` | Acao do usuario, processo do sistema, estado de UI |
| Losango | `{texto}` | Decisao de logica de negocio (sim/nao, tem/não tem) |
| Retangulo arredondado | `(texto)` | Inicio, fim, entrada/saida do fluxo |
| Sub-rotina | `[[texto]]` | Chamada a processo externo ou subfluxo |

## Regras de cobertura

O fluxograma cobre dois tipos de caminho:

- **Caminho feliz**: o fluxo principal, da entrada ate a conclusao com sucesso. Cada passo e um no de acao ou decisao.
- **Caminhos infelizes**: todo ponto de falha identificado na analise de riscos gera um no de erro com `classDef error`. Ramos de decisao negativos (ex: "Saldo suficiente? — Nao") levam a nos de erro ou de saida alternativa.

Para cada ponto de decisao (`{}`), ambas as saidas (`Sim`/`Nao`, `|Sucesso|`/`|Falha|`) precisam de um rotulo explicito na aresta.

## Estados de interface

Quando o fluxo envolve interacao com usuario, represente estes tres estados como nos retangulares com a classe correspondente:

- **Loading**: tela de carregamento, spinner, "Aguardando resposta..."
- **Empty**: estado vazio — "Nenhum item encontrado", "Sem dados disponiveis"
- **Error feedback**: mensagem de erro visivel ao usuario, toast, alerta

## Geracao

### 1. Leitura do contexto

Receba a analise de riscos e requisitos. Extraia atores, entrada, sequencia do caminho feliz, pontos de decisao com condicoes, falhas identificadas, e estados de UI mencionados ou inferidos. Tudo extraido — todo ponto de falha fica **contrastado** entre caminho feliz e infeliz.

**Criterio de conclusao**: atores, entrada, sequencia completa do caminho feliz, todos os pontos de decisao com suas condicoes, e cada falha identificada — todos extraidos da especificacao antes de iniciar a geracao do diagrama.

### 2. Geracao do codigo

Produza o codigo Mermaid:

```
%%{init: {'theme': 'base'}}%%
graph TD
  A[texto] --> B{texto}
  B -->|Sim| C[texto]
  B -->|Nao| D[texto]
```

Use a paleta de **contraste** para classificar cada no via `class N1,N2 nomeDaClasse`.

**Criterio de conclusao**: diagrama Mermaid gerado com `%%{init: {'theme': 'base'}}%%` na primeira linha, todos os nos do caminho feliz e infeliz representados, nos de decisao no formato `{}` com ambas as saidas rotuladas, e cada no classificado com `classDef` da paleta de contraste.

### 3. Validacao de contraste

Antes de entregar, verifique o **contraste**:

- [ ] `%%{init: {'theme': 'base'}}%%` na primeira linha
- [ ] Todo `classDef` tem `fill`, `color` e `stroke`
- [ ] Todo no de decisao (`{}`) tem arestas de saida com rotulos
- [ ] Todo caminho (feliz + infeliz) da analise de riscos aparece no diagrama

**Criterio de conclusao**: checklist acima totalmente preenchido (tudo verde).

## Exemplo

### Entrada: especificacao de reembolso

> Cliente solicita reembolso de um pedido. O sistema verifica se esta dentro do prazo de 7 dias. Se fora do prazo, reembolso negado. Se dentro, verifica se o pedido ja foi enviado. Se nao enviado, reembolso aprovado automaticamente. Se enviado, cliente precisa devolver o produto. Ao receber a devolucao, o sistema inspeciona o item. Se avariado, reembolso parcial. Se integro, reembolso integral.

### Saida: fluxograma gerado

```mermaid
%%{init: {'theme': 'base'}}%%
graph TD
  A(Cliente solicita reembolso) --> B{Solicitacao dentro\ndo prazo de 7 dias?}
  B -->|Sim| C{Pedido ja\nfoi enviado?}
  B -->|Nao| D[Reembolso negado — fora do prazo]
  C -->|Nao| E[Reembolso aprovado — automatico]
  C -->|Sim| F[Cliente devolve o produto]
  F --> G[Sistema recebe a devolucao]
  G --> H{Inspecao do item\n— integro ou avariado?}
  H -->|Integro| I[Reembolso integral]
  H -->|Avariado| J[Reembolso parcial — dano constatado]

  classDef error fill:#fee,color:#900,stroke:#c00
  classDef success fill:#efe,color:#060,stroke:#393
  classDef decision fill:#fff3cd,color:#630,stroke:#c90
  classDef action fill:#e8e8e8,color:#222,stroke:#666
  classDef startend fill:#d4edda,color:#155724,stroke:#28a745

  class D,J error
  class E,I success
  class B,C,H decision
  class F,G action
  class A startend
```

O exemplo cobre:
- **Caminho feliz**: solicitar → dentro do prazo → enviado → devolver → inspecionar → integral (sucesso)
- **Caminhos infelizes**: fora do prazo (erro), avariado (erro)
- **Decisoes**: prazo (sim/nao), envio (sim/nao), inspecao (integro/avariado)
- **Paleta completa**: `error`, `success`, `decision`, `action`, `startend`
