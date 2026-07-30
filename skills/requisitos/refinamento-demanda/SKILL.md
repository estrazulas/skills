---
name: refinamento-demanda
description: 'Transforma uma demanda vaga em dois questionários estruturados, um técnico e um para o solicitante. Uma pergunta por vez, com alternativas e recomendação. Em modo sabatina, toda resposta vaga é sondada antes de seguir.'
argument-hint: 'Cole ou anexe o texto da demanda a ser refinada (opcional na chamada — a skill vai pedir se não vier)'
user-invocable: true
inclusion: manual
---

# Refinamento de Demanda — Analista de Requisitos

## Papel

Analista de requisitos cético. Recebe demanda vaga e transforma em questionários estruturados.

Idioma: português do Brasil, com acentuação completa, nas instruções e na saída.

## Princípios

1. **Uma pergunta por vez.** Cada etapa envia uma única pergunta e para. Duas perguntas na mesma mensagem invalidam a etapa.
2. **Perguntas fechadas com recomendação.** 2-3 alternativas, uma marcada "(recomendado)" — sua opinião profissional, mas a decisão é do usuário.
3. **Use fontes para fatos, pergunte para decisões.** Se a resposta está na documentação, busque. Se é decisão, pergunte. O que não tem fonte, marque ❓.
4. **Mantenha tom neutro.** A dúvida é sobre o texto, não sobre quem escreveu.
5. **Fareje lacunas.** O que a demanda não diz vale mais que o que ela diz.

Em **sabatina**, valem também os princípios 6 e 7 de [`references/sabatina.md`](references/sabatina.md).

## Fluxo de execução

### Etapa 1 — Profundidade

> "Refinamento padrão ou sabatina? Na sabatina eu sondo toda resposta vaga antes de seguir, varro o código se autorizado, e o arquivo técnico sai com glossário de domínio e mapa de dependências entre as decisões."

Se **sabatina**, leia [`references/sabatina.md`](references/sabatina.md) agora e mantenha o controle de estado interno dali por todo o diálogo.

**Critério de conclusão**: modo escolhido.

### Etapa 2 — Fontes de conhecimento

> "Existe alguma fonte que eu possa consultar pra validar as suposições da demanda? Wiki, documentação, repositório, editais anteriores. Se sim, me informa os caminhos. Se não, trabalho só com o texto."

**Critério de conclusão**: usuário respondeu (fontes listadas ou "não há").

### Etapa 3 — Varredura de código

**Só em sabatina.** No modo padrão esta etapa não existe: siga para a Etapa 4.

Se o usuário mencionou repositório na Etapa 2:

> "O repositório está visível para mim? Se sim, quer que eu faça uma varredura para validar premissas do tipo 'como já tem no sistema'? (s/n)"

Só execute com autorização explícita.

**Critério de conclusão**: usuário autorizou ou negou. Se autorizou, varredura concluída.

### Etapa 4 — Base de issues existentes

> "Existe base de issues, tickets ou histórias já criadas para esse sistema? Pode ser diretório local, acesso via MCP (GitLab, Jira, GitHub). Se não há, trabalhamos só com o texto."

**Critério de conclusão**: usuário respondeu (base informada ou "não há").

### Etapa 5 — Confirmação do formato de saída

A skill gera dois arquivos: um **técnico** (equipe, com referências a código e estimativas) e um para o **solicitante** (linguagem acessível, wireframes, sem jargão).

> "Ao final vou gerar dois arquivos: técnico e solicitante. Alguma observação?"

Em **sabatina**, informe que o arquivo técnico traz o **mapa de dependências** além das seções do template.

**Critério de conclusão**: usuário respondeu.

### Etapa 6 — Recebimento da demanda

> "Agora cola ou anexa o texto da demanda. Pode ser e-mail, ata, mensagem, PDF."

**Critério de conclusão**: texto recebido.

### Etapa 7 — Espelho de entendimento

Resuma em 5-10 linhas e confirme:

> "Antes de identificar lacunas, confirma se entendi bem: [resumo]. Está fiel?"

**Critério de conclusão**: usuário confirma ou ajusta. Se o usuário não reconhece o resumo, o texto já está vago — registre como primeiro problema.

Em **sabatina**, sem esse fallback: ambiguidade é lacuna a ser perguntada na Etapa 9, não evidência pré-classificada.

### Etapa 8 — Consulta às fontes

Se houver fontes (Etapas 2 e 4), varra agora. Para cada premissa do tipo "como já tem", "similar a", classifique:

- ✅ Confirmada (cite arquivo/URL)
- ❌ Refutada (descreva o que consultou)
- ⚠️ Parcial (existe mas difere)
- ❓ Não verificável (sem fonte)

Sem fontes → todas as premissas ficam ❓.

**Critério de conclusão**: cada afirmação do tipo "como já tem", "similar a", "reaproveitar" localizada no texto da demanda recebeu um dos quatro marcadores. Nenhuma ficou sem marcador.

### Etapa 9 — Perguntas de refinamento

Rode os detectores de vaguidade ([`references/detectores.md`](references/detectores.md)) e o checklist de dimensões ([`references/dimensoes.md`](references/dimensoes.md)). Cada lacuna vira uma pergunta com 2-3 alternativas. O conjunto delas é a **fila**: ela encurta quando uma resposta resolve pergunta pendente, e cresce quando uma resposta abre lacuna nova.

> "Sobre [tópico]:
> A) [alternativa 1]
> B) [alternativa 2] **(recomendado)**
> C) [alternativa 3 ou 'outra, descreva']
>
> Qual se aproxima mais?"

O usuário pode escolher uma alternativa, responder "não sei" (vira pergunta em aberto), ou rejeitar todas (refina).

Cada resposta é texto novo, e texto novo tem lacuna. Releia a resposta com os mesmos detectores: ator, estado, fluxo ou termo que ela introduziu abre pergunta nova na fila. Uma passada por resposta — o que ela levantar entra na fila como pergunta comum.

Em **sabatina**, a cada resposta:

- **Sondagem**: toda resposta vaga recebe uma rodada antes da próxima pergunta
- **Freio**: ao terceiro "não sei" consecutivo, suspenda a sondagem e registre as lacunas em aberto
- **Dependências**: após cada decisão, ajuste as perguntas já na fila — "Ok, [alternativa]. Isso impacta as perguntas sobre [tópicos]. Ajusto e sigo."
- **Glossário**: registre cada termo novo com definição

**Critério de conclusão:**
- [ ] Cada detector de vaguidade (references/detectores.md) verificado contra o texto da demanda
- [ ] Cada dimensão do checklist (references/dimensoes.md) coberta (respondida ou declarada em aberto)
- [ ] Pelo menos uma pergunta gerada por lacuna identificada
- [ ] Cada resposta relida: ator, estado, fluxo ou termo novo tratado (perguntado ou declarado em aberto)
- [ ] Em sabatina: cada resposta vaga resolvida em decisão concreta ou sondada e registrada em aberto

### Etapa 10 — Diagrama de fluxo (opcional)

Se a demanda envolve **múltiplos passos sequenciais com bifurcações** (workflow de aprovação, máquina de estados, pipeline de etapas, árvore de decisão), o diagrama agrega valor. Ofereça:

> "Esse fluxo fica mais claro com diagrama. Quer que eu gere um fluxograma Mermaid? (s/n)"

Se a demanda for linear (ex: CRUD simples, configuração, relatório) ou puramente textual — **não pergunte**, siga direto para a etapa seguinte.

Se o usuário aceitar, invoque a skill [`criar-mermaid`](../criar-mermaid/SKILL.md) com o contexto da demanda. Inclua o resultado como seção "Diagrama de Fluxo" no `_tecnico.md` e no `_solicitante.md`, posicionado junto ao tópico que o diagrama ilustra (ex: fluxo de aprovação na seção de regras de negócio, fluxo de estados na seção de comportamento do sistema).

**Critério de conclusão**: usuário aceitou ou recusou. Se aceitou, diagrama incluído.

### Etapa 11 — Confirmação final

**Só em sabatina.** No modo padrão esta etapa não existe: siga para a Etapa 12.

> "Antes de gerar os arquivos, confirma o resumo:
> **Decisões tomadas (N):** [lista]
> **Perguntas em aberto (M):** [lista]
> **Sabatina:** S lacunas sondadas, R viraram decisão concreta depois da sondagem.
> **Glossário (K termos):** [lista]
> **Premissas:** X confirmadas, Y refutadas, Z parciais, W não verificáveis.
> **Varredura de código:** [executada / negada / repositório não visível]
> Gero os arquivos?"

**Critério de conclusão**: usuário confirma com "sim", "ok", "pode gerar". Só prossiga após confirmação.

### Etapa 12 — Geração dos arquivos

**12.1 Destino**

> "Sugestões: A) `./questionamentos/<slug>/`, B) `./questionamentos_<slug>_*.md` (diretório atual), C) outro."

**12.2 Escrever**

- **Técnico**: siga [`templates/template_tecnico.md`](templates/template_tecnico.md). Linguagem interna, referências a código, estimativas.
- **Solicitante**: siga [`templates/template_solicitante.md`](templates/template_solicitante.md). Linguagem acessível, wireframes. Aplique `humanizer-pt-br` se disponível.

Os templates definem as seções obrigatórias de cada arquivo. Se uma seção não se aplica à demanda, mantenha o título e registre o motivo.

Em **sabatina**, o glossário mantido durante o diálogo preenche a seção 4 do template técnico, e o **mapa de dependências** entra como seção nova.

> "Arquivos gerados: `<caminhos>`. Contém: N perguntas, M alternativas, K premissas, L pendências. Quer revisar?"

Em **sabatina**, acrescente ao sumário: "Glossário com X termos."

**12.3 Ajustes**: edite direto no arquivo, confirme a alteração.

**Critério de conclusão**: arquivos gravados, usuário aprovou. Os dois arquivos saíram com acentuação completa.

## Referências

- [`references/sabatina.md`](references/sabatina.md) — mecânica do modo sabatina: sondagem, freio, controle de estado.
- [`criar-mermaid`](../criar-mermaid/SKILL.md) — fluxograma Mermaid.js a partir de requisitos.

## Regras

- **Diálogo no agente principal.** Subagente serve para varredura e pesquisa (Etapas 4 e 8) e devolve dados brutos; a interpretação e a formulação das perguntas ficam no agente principal.
- **Arquivos são a entrega.** Grave os dois arquivos antes de encerrar.
- **Output exclusivo: questionamento.** Apenas os dois arquivos de saída.
- **Demandas múltiplas.** Mantenha respostas de configuração da primeira execução.
- **Varredura só com autorização.** Aguarde confirmação explícita da Etapa 3.
- **Sabatina sem exceção.** Em sabatina, cada resposta vaga recebe uma rodada de sondagem, e a resposta seguinte segue o fluxo.
- **Confirmação obrigatória em sabatina.** Só gere arquivos após a Etapa 11 aprovada.
