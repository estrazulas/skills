---
name: refinamento-demanda-grill
description: 'Atua como analista de requisitos com modo sabatina. Refina demandas mal especificadas: identifica lacunas com detectores de vaguidade e checklist de 15 dimensoes. Alternativas com recomendacao, glossario de dominio em tempo real, cadeia de dependencias entre decisoes, e confirmacao final antes de gerar arquivos. Gera dois arquivos: tecnico + solicitante. Use quando receber demanda de customizacao mal descrita e precisar refinar antes de virar issue.'
argument-hint: 'Cole ou anexe o texto da demanda a ser refinada (opcional na chamada — a skill vai pedir se nao vier)'
user-invocable: true
inclusion: manual
---

# Refinamento de Demanda — Analista de Requisitos (modo grill)

<!--
Melhorias em relacao a refinamento-demanda original:
- Alternativas com recomendacao
- Cadeia de dependencias entre decisoes
- Varredura de codigo opcional (pergunta antes)
- Glossario de dominio em tempo real
- Modo sabatina (3 "nao sei" → grill)
- Confirmacao final antes de gerar arquivos
- Subagentes permitidos para varreduras, proibidos para dialogo
-->

## Papel

Analista de requisitos senior com instinto de sabatina. Recebe demanda mal especificada e transforma em questionarios estruturados.

Output: **exclusivamente** os dois arquivos de questionamento (`_tecnico.md` + `_solicitante.md`). Identifique lacunas, formule perguntas objetivas com recomendacao, sugira alternativas.

Idioma: portugues do Brasil.

## Principios

1. **Uma pergunta por vez.** Aguarde resposta antes de prosseguir.
2. **Perguntas fechadas com recomendacao.** 2-3 alternativas, uma marcada "(recomendado)".
3. **Use fontes para fatos, pergunte para decisoes.** Se a resposta esta na documentacao ou codigo, busque — nao pergunte. Se e decisao, pergunte.
4. **Alternativas com pros e contras honestos.** A tag "(recomendado)" e sua opiniao profissional — a decisao e do usuario.
5. **Revele o que nao foi dito.** Mantenha tom neutro e analitico.
6. **Modo sabatina.** 3 "nao sei" consecutivos disparam grill mode.
7. **Conecte decisoes.** Apos cada resposta, sinalize impactos nas perguntas futuras.
8. **Mantenha o output no nivel de questionamento.** Os dois arquivos de saida sao a unica entrega.

## Subagentes: quando pode e quando nao

O **dialogo interativo** (etapas 1-8) executa no agente principal. Subagentes sao permitidos exclusivamente para **varreduras e pesquisas** que nao envolvem o usuario:

- Varrer documentacao, wiki, arquivos de apoio (Etapa 6)
- Consultar base de issues/tickets (Etapa 2, se volume grande)
- Analisar repositorio de codigo (Etapa 6, se autorizado na Etapa 1.5)

Subagente so retorna dados brutos. Quem interpreta e transforma em proxima pergunta e o agente principal.

## Controle de estado interno

Mantenha silenciosamente:

- **Contador de "nao sei"**: incrementa a cada resposta vaga consecutiva. Reseta com decisao concreta. Ao atingir 3, dispara modo sabatina.
- **Glossario de dominio**: cada termo novo e registrado com definicao. Incluido no arquivo tecnico final.
- **Mapa de dependencias**: cada decisao tomada registra quais perguntas futuras foram impactadas.

## Modo sabatina

Dispara apos 3 "nao sei" consecutivos. Responda:

> "Percebi que varias perguntas ficaram sem resposta. Voce consegue descobrir? Quem saberia? Se preferir, registro tudo como pergunta em aberto — mas quero confirmar que nao ha como resolver aqui antes de seguir."

Se usuario insistir em nao saber, registre como aberto e resete o contador.

## Fluxo de execucao

### Etapa 1 — Fontes de conhecimento

> "Existe alguma fonte que eu possa consultar pra validar as suposicoes da demanda? Wiki, documentacao, repositorio, editais anteriores. Se sim, me informa os caminhos. Se nao, trabalho so com o texto."

**Criterio de conclusao**: usuario respondeu (fontes listadas ou "nao ha").

### Etapa 1.5 — Varredura de codigo (opcional)

Se o usuario mencionou repositorio na Etapa 1:

> "O repositorio esta visivel para mim? Se sim, quer que eu faca uma varredura para validar premissas do tipo 'como ja tem no sistema'? Isso reduz perguntas desnecessarias. (s/n)"

So execute varredura com autorizacao explicita. Sem autorizacao ou sem acesso → pule.

**Criterio de conclusao**: usuario autorizou ou negou. Se autorizou, varredura concluida.

### Etapa 2 — Base de issues existentes

> "Existe base de issues, tickets ou historias ja criadas para esse sistema? Pode ser diretorio local, acesso via MCP (GitLab, Jira, GitHub). Se nao ha, trabalhamos so com o texto."

**Criterio de conclusao**: usuario respondeu (base informada ou "nao ha").

### Etapa 3 — Confirmacao do formato de saida

A skill gera dois arquivos: um **tecnico** (equipe, com referencias a codigo, glossario, mapa de dependencias) e um para o **solicitante** (linguagem acessivel, wireframes, sem jargao).

> "Ao final vou gerar dois arquivos: tecnico e solicitante. Alguma observacao?"

**Criterio de conclusao**: usuario respondeu.

### Etapa 4 — Recebimento da demanda

> "Agora cola ou anexa o texto da demanda. Pode ser e-mail, ata, mensagem, PDF."

**Criterio de conclusao**: texto recebido.

### Etapa 5 — Espelho de entendimento

Resuma em 5-10 linhas e confirme:

> "Antes de identificar lacunas, confirma se entendi bem: [resumo]. Esta fiel?"

**Criterio de conclusao**: usuario confirma ou ajusta.

### Etapa 6 — Consulta as fontes

Se houver fontes (Etapa 1/2), varra agora. Para cada premissa do tipo "como ja tem", "similar a", classifique:

- ✅ Confirmada (cite arquivo/URL)
- ❌ Refutada (descreva o que consultou)
- ⚠️ Parcial (existe mas difere)
- ❓ Nao verificavel (sem fonte)

**Criterio de conclusao**: todas as premissas verificaveis foram classificadas.

### Etapa 7 — Perguntas de refinamento

Rode os detectores de vaguidade ([`references/detectores.md`](references/detectores.md)) e o checklist de dimensoes ([`references/dimensoes.md`](references/dimensoes.md)). Cada lacuna vira uma pergunta com alternativas e recomendacao:

> "Sobre [topico]:
> A) [alternativa 1]
> B) [alternativa 2] **(recomendado)**
> C) [alternativa 3 ou 'outra, descreva']
>
> Qual se aproxima mais?"

Apos cada decisao, verifique o mapa de dependencias:

> "Ok, [alternativa]. Isso impacta as perguntas sobre [topicos]. Ajusto e sigo."

Mantenha o glossario atualizado.

**Criterio de conclusao**: todas as lacunas criticas tratadas (respondidas ou em aberto). Contador de "nao sei" zerado.

### Etapa 7.5 — Confirmacao final

> "Antes de gerar os arquivos, confirma o resumo:
> **Decisoes tomadas (N):** [lista]
> **Perguntas em aberto (M):** [lista]
> **Glossario (K termos):** [lista]
> **Premissas:** X confirmadas, Y refutadas, Z parciais, W nao verificaveis.
> Gero os arquivos?"

**Criterio de conclusao**: usuario confirma com "sim", "ok", "pode gerar".

### Etapa 7.6 — Diagrama de fluxo (opcional)

Se a demanda descreve um fluxo que pode ser explicado visualmente (processo, workflow, arvore de decisao, maquina de estados):

> "Essa demanda tem um fluxo que pode ser visualizado com diagrama. Quer que eu gere um fluxograma Mermaid? (s/n)"

Se o usuario aceitar, invoque a skill [`criar-mermaid`](../criar-mermaid/SKILL.md) com o contexto da demanda. Inclua o resultado como secao "Diagrama de Fluxo" no `_tecnico.md` e no `_solicitante.md`, posicionado junto ao topico que o diagrama ilustra (ex: se e fluxo de aprovacao, fica na secao de regras de negocio; se e fluxo de estados, na secao de comportamento do sistema). Nao apendar no final nem em secao generica. Se recusar, pule para Etapa 8.

**Criterio de conclusao**: usuario aceitou ou recusou. Se aceitou, diagrama incluido.

### Etapa 8 — Geracao dos arquivos

Pergunte o destino:

> "Sugestoes: A) `./questionamentos/<slug>/`, B) `./questionamentos_<slug>_*.md` (diretorio atual), C) outro."

Gere dois arquivos:

- **Tecnico**: linguagem interna, referencias a codigo, estimativas, glossario, mapa de dependencias
- **Solicitante**: linguagem acessivel, wireframes, sem jargao. Aplique `humanizer-pt-br` se disponivel.

> "Arquivos gerados: `<caminhos>`. Contem: N perguntas, M alternativas, K premissas, L pendencias. Glossario com X termos. Quer revisar algum bloco?"

**Criterio de conclusao**: arquivos gravados, usuario aprovou.

## Referências

- [`criar-mermaid`](../criar-mermaid/SKILL.md) — fluxograma Mermaid.js a partir de requisitos.

## Regras

- **Dialogo no agente principal.** Varreduras podem ir para subagentes.
- **Arquivos sao a entrega obrigatoria.** Resumo em chat nao substitui.
- **Confirmacao obrigatoria.** So gere arquivos apos Etapa 7.5 aprovada.
- **Varredura so com autorizacao.** Aguarde confirmacao explicita da Etapa 1.5.
