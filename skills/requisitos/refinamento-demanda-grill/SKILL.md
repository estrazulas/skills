---
name: refinamento-demanda-grill
description: 'Refina demandas mal especificadas com questionamento intensivo (modo sabatina). Glossario de dominio, cadeia de dependencias entre decisoes, varredura de codigo, e confirmacao final antes de gerar arquivos. Use quando precisar de refinamento mais profundo que o refinamento-demanda ou quando o solicitante costuma responder "nao sei".'
argument-hint: 'Cole ou anexe o texto da demanda a ser refinada (opcional na chamada — a skill vai pedir se nao vier)'
user-invocable: true
inclusion: manual
---

# Refinamento de Demanda — Modo Grill

Siga o fluxo base do [`refinamento-demanda`](../refinamento-demanda/SKILL.md) com as alteracoes abaixo. Onde nao houver delta, vale o que esta na skill base.

## Deltas

### Principios (adiciona 6, 7 apos o 5 da base)

Adicione apos o principio 5 da base:

6. **Modo sabatina.** 3 "nao sei" consecutivos disparam grill mode.
7. **Conecte decisoes.** Apos cada resposta, sinalize impactos nas perguntas futuras.
8. **Mantenha o output no nivel de questionamento.** Os dois arquivos de saida sao a unica entrega.

### Controle de estado interno (novo)

Mantenha silenciosamente:

- **Contador de "nao sei"**: incrementa a cada resposta vaga consecutiva. Reseta com decisao concreta. Ao atingir 3, dispara modo sabatina.
- **Glossario de dominio**: cada termo novo e registrado com definicao. Incluido no arquivo tecnico final.
- **Mapa de dependencias**: cada decisao tomada registra quais perguntas futuras foram impactadas.

### Modo sabatina (novo)

Dispara apos 3 "nao sei" consecutivos:

> "Percebi que varias perguntas ficaram sem resposta. Voce consegue descobrir? Quem saberia? Se preferir, registro tudo como pergunta em aberto — mas quero confirmar que nao ha como resolver aqui antes de seguir."

Se usuario insistir em nao saber, registre como aberto e resete o contador.

### Fluxo de execucao

Siga as etapas 1-8 da skill base com estas alteracoes:

#### Etapa 1.5 — Varredura de codigo (nova, entre Etapas 1 e 2)

Se o usuario mencionou repositorio na Etapa 1:

> "O repositorio esta visivel para mim? Se sim, quer que eu faca uma varredura para validar premissas do tipo 'como ja tem no sistema'? (s/n)"

So execute com autorizacao explicita.

**Criterio de conclusao**: usuario autorizou ou negou. Se autorizou, varredura concluida.

#### Etapa 3 — Confirmacao do formato de saida (modificada)

Mesmo script, mas informe que o arquivo tecnico incluira **glossario** e **mapa de dependencias** alem do conteudo base.

#### Etapa 5 — Espelho de entendimento (modificada)

Mesmo script da base, mas **sem** o fallback de "registre como primeiro problema". O grill trata ambiguidade como lacuna a ser perguntada, nao como evidencia pre-classificada.

#### Etapa 7 — Perguntas de refinamento (modificada)

Mesmo processo da base, com adicoes:

- Apos cada decisao, verifique o mapa de dependencias:

> "Ok, [alternativa]. Isso impacta as perguntas sobre [topicos]. Ajusto e sigo."

- Mantenha o glossario atualizado a cada termo novo
- **Modo sabatina**: se o contador de "nao sei" atingir 3, dispare antes da proxima pergunta

**Criterio de conclusao**: todas as lacunas criticas tratadas. Contador de "nao sei" zerado.

#### Etapa 7.5 — Confirmacao final (nova, entre Etapas 7.6 e 8)

> "Antes de gerar os arquivos, confirma o resumo:
> **Decisoes tomadas (N):** [lista]
> **Perguntas em aberto (M):** [lista]
> **Glossario (K termos):** [lista]
> **Premissas:** X confirmadas, Y refutadas, Z parciais, W nao verificaveis.
> Gero os arquivos?"

**Criterio de conclusao**: usuario confirma com "sim", "ok", "pode gerar". So prossiga para Etapa 8 apos confirmacao.

#### Etapa 8 — Geracao dos arquivos (modificada)

Mesmo processo da base. No arquivo **tecnico**, inclua adicionalmente: glossario de dominio e mapa de dependencias. No sumario pos-geracao, inclua "Glossario com X termos."

### Referências

- [`criar-mermaid`](../criar-mermaid/SKILL.md) — fluxograma Mermaid.js a partir de requisitos.
- [`refinamento-demanda`](../refinamento-demanda/SKILL.md) — skill base da qual este grill deriva.

### Regras (adicionais as da base)

- **Confirmacao obrigatoria.** So gere arquivos apos Etapa 7.5 aprovada.
- **Varredura so com autorizacao.** Aguarde confirmacao explicita da Etapa 1.5.
