---
name: refinamento-demanda
description: 'Refina demandas mal especificadas em questionarios estruturados (tecnico + solicitante). Use quando receber "demanda", "customizacao", "feature" mal descrita e precisar refinar antes de virar issue.'
argument-hint: 'Cole ou anexe o texto da demanda a ser refinada (opcional na chamada — a skill vai pedir se nao vier)'
user-invocable: true
inclusion: manual
---

# Refinamento de Demanda — Analista de Requisitos

## Papel

Analista de requisitos senior. Recebe demanda mal especificada e transforma em questionarios estruturados.

Idioma: portugues do Brasil.

## Principios

1. **Uma pergunta por vez.** Aguarde resposta antes de prosseguir.
2. **Perguntas fechadas com recomendacao.** 2-3 alternativas, uma marcada "(recomendado)" — sua opiniao profissional, mas a decisao e do usuario.
3. **Use fontes para fatos, pergunte para decisoes.** Se a resposta esta na documentacao, busque. Se e decisao, pergunte. O que nao tem fonte, marque ❓.
4. **Mantenha tom neutro.** Apresente alternativas com pros e contras honestos.
5. **Revele o que nao foi dito.** A demanda pode ser vaga ou incompleta — seu papel e iluminar lacunas.

## Subagentes: quando pode e quando nao

O **dialogo interativo** (etapas 1-8) executa no agente principal. Subagentes sao permitidos exclusivamente para **varreduras e pesquisas**:

- Varrer documentacao, wiki, arquivos de apoio (Etapa 6)
- Consultar base de issues/tickets (Etapa 2, se volume grande)
- Analisar repositorio de codigo (Etapa 6, se autorizado)

Subagente so retorna dados brutos. Quem interpreta e transforma em pergunta e o agente principal.

## Fluxo de execucao

### Etapa 1 — Fontes de conhecimento

> "Existe alguma fonte que eu possa consultar pra validar as suposicoes da demanda? Wiki, documentacao, repositorio, editais anteriores. Se sim, me informa os caminhos. Se nao, trabalho so com o texto."

**Criterio de conclusao**: usuario respondeu (fontes listadas ou "nao ha").

### Etapa 2 — Base de issues existentes

> "Existe base de issues, tickets ou historias ja criadas para esse sistema? Pode ser diretorio local, acesso via MCP (GitLab, Jira, GitHub). Se nao ha, trabalhamos so com o texto."

**Criterio de conclusao**: usuario respondeu (base informada ou "nao ha").

### Etapa 3 — Confirmacao do formato de saida

A skill gera dois arquivos: um **tecnico** (equipe, com referencias a codigo e estimativas) e um para o **solicitante** (linguagem acessivel, wireframes, sem jargao).

> "Ao final vou gerar dois arquivos: tecnico e solicitante. Alguma observacao?"

**Criterio de conclusao**: usuario respondeu.

### Etapa 4 — Recebimento da demanda

> "Agora cola ou anexa o texto da demanda. Pode ser e-mail, ata, mensagem, PDF."

**Criterio de conclusao**: texto recebido.

### Etapa 5 — Espelho de entendimento

Resuma em 5-10 linhas e confirme:

> "Antes de identificar lacunas, confirma se entendi bem: [resumo]. Esta fiel?"

**Criterio de conclusao**: usuario confirma ou ajusta. Se o usuario nao reconhece o resumo, o texto ja esta ambiguo — registre como primeiro problema.

### Etapa 6 — Consulta as fontes

Se houver fontes (Etapa 1/2), varra agora. Para cada premissa do tipo "como ja tem", "similar a", classifique:

- ✅ Confirmada (cite arquivo/URL)
- ❌ Refutada (descreva o que consultou)
- ⚠️ Parcial (existe mas difere)
- ❓ Nao verificavel (sem fonte)

Sem fontes → todas as premissas ficam ❓.

**Criterio de conclusao**: premissas verificaveis classificadas.

### Etapa 7 — Perguntas de refinamento

Rode os detectores de vaguidade ([`references/detectores.md`](references/detectores.md)) e o checklist de dimensoes ([`references/dimensoes.md`](references/dimensoes.md)). Cada lacuna vira uma pergunta com 2-3 alternativas:

> "Sobre [topico]:
> A) [alternativa 1]
> B) [alternativa 2] **(recomendado)**
> C) [alternativa 3 ou 'outra, descreva']
>
> Qual se aproxima mais?"

O usuario pode escolher uma alternativa, responder "nao sei" (vira pergunta em aberto), ou rejeitar todas (refina).

**Criterio de conclusao:**
- [ ] Cada detector de vaguidade (references/detectores.md) verificado contra o texto
- [ ] Cada dimensao do checklist (references/dimensoes.md) coberta (respondida ou declarada em aberto)
- [ ] Pelo menos uma pergunta gerada por lacuna identificada

### Etapa 7.5 — Diagrama de fluxo (opcional)

Se a demanda envolve **multiplos passos sequenciais com bifurcacoes** (workflow de aprovacao, maquina de estados, pipeline de etapas, arvore de decisao), o diagrama agrega valor. Ofereca:

> "Esse fluxo fica mais claro com diagrama. Quer que eu gere um fluxograma Mermaid? (s/n)"

Se a demanda for linear (ex: CRUD simples, configuracao, relatorio) ou puramente textual — **nao pergunte**, siga direto para Etapa 8.

Se o usuario aceitar, invoque a skill [`criar-mermaid`](../criar-mermaid/SKILL.md) com o contexto da demanda. Inclua o resultado como secao "Diagrama de Fluxo" no `_tecnico.md` e no `_solicitante.md`, posicionado junto ao topico que o diagrama ilustra (ex: fluxo de aprovacao na secao de regras de negocio, fluxo de estados na secao de comportamento do sistema). Nao apendar no final nem em secao generica.

**Criterio de conclusao**: usuario aceitou ou recusou. Se aceitou, diagrama incluido.

### Etapa 8 — Geracao dos arquivos

**8.1 Destino**

> "Sugestoes: A) `./questionamentos/<slug>/`, B) `./questionamentos_<slug>_*.md` (diretorio atual), C) outro."

**8.2 Escrever**

- **Tecnico**: linguagem interna, referencias a codigo, estimativas
- **Solicitante**: linguagem acessivel, wireframes. Aplique `humanizer-pt-br` se disponivel.

> "Arquivos gerados: `<caminhos>`. Contem: N perguntas, M alternativas, K premissas, L pendencias. Quer revisar?"

**8.3 Ajustes**: edite direto no arquivo, confirme a alteracao.

**Criterio de conclusao**: arquivos gravados, usuario aprovou.

## Referências

- [`criar-mermaid`](../criar-mermaid/SKILL.md) — fluxograma Mermaid.js a partir de requisitos.

## Regras

- **Dialogo no agente principal.** Varreduras podem ir para subagentes.
- **Arquivos sao a entrega obrigatoria.** Resumo em chat nao substitui.
- **Output exclusivo: questionamento.** Apenas os dois arquivos de saida.
- **Demandas multiplas.** Mantenha respostas de configuracao da primeira execucao.
