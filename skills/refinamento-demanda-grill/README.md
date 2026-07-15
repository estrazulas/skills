# refinamento-demanda-grill

Versao turbinada da `refinamento-demanda` com principios da **grill-me** do Matt Pocock.

## O que resolve

Voce recebe uma demanda vaga de um cliente/chefe. Exemplo classico:

> "Preciso que o sistema permita lancar notas dos alunos."

Isso nao diz: quem lanca? em qual etapa? vale pra todos os cursos? precisa de aprovacao? o que acontece se errar?

A skill atua como um analista de requisitos que:
1. Identifica todas as lacunas (uma por vez)
2. Oferece alternativas com recomendacao
3. Conecta decisoes entre si
4. Sabatina quando voce responde "nao sei" demais
5. Gera dois arquivos prontos pra enviar: um tecnico (pra equipe) e um pro solicitante (linguagem acessivel)

## Diferenca da versao original (refinamento-demanda)

|  | Original | Grill |
|---|---|---|
| Alternativas | A, B, C (neutro) | A, B, C + **uma marcada como (recomendado)** |
| Dependencias | Nao conecta | Apos cada decisao, avisa: "Isso impacta as perguntas X, Y, Z" |
| Codigo | Sempre tenta varrer se tem fonte | So varre com autorizacao explicita do usuario |
| "Nao sei" | Vira pergunta em aberto direto | Aguenta 3, depois entra em **modo sabatina** |
| Glossario | Nao mantem | Acumula durante a sessao, entrega no arquivo tecnico |
| Antes de gerar | Gera direto | **Confirmacao final** com resumo de tudo |
| Subagentes | Proibido totalmente | **Permitido so para varreduras** (codigo, docs, issues); dialogo sempre no agente principal |

## Como usar

```
/refinamento-demanda-grill
```

A skill vai conduzir 8 etapas. Voce so precisa responder — uma pergunta por vez.

## Exemplo completo de sessao

### Entrada (o que voce cola na Etapa 4)

> "O sistema precisa ter uma tela de renovacao de matricula. O aluno entra, confirma os dados e finaliza. Similar ao que ja tem no SIGAA."

### Como a skill conduz

**Etapa 1 — Fontes:**
> "Existe alguma fonte que eu possa consultar pra validar as suposicoes da demanda?"

Usuario: `Nao, so o texto.`

**Etapa 1.5 — Varredura de codigo:**
> (Pulada — sem fontes)

**Etapa 2 — Issues existentes:**
> "Existe alguma base de issues, tickets ou historias ja criadas?"

Usuario: `Nao.`

**Etapa 3 — Formato de saida:**
> "Ao final vou gerar dois arquivos: um tecnico e um pro solicitante. Alguma observacao?"

Usuario: `Nao, segue.`

**Etapa 5 — Espelho de entendimento:**
> "Entendi que voce quer uma tela onde o aluno visualiza seus dados cadastrais, confirma que estao corretos e finaliza a renovacao de matricula para o proximo periodo. A referencia ao SIGAA sugere um fluxo similar ao de sistemas academicos convencionais. Esta fiel?"

Usuario: `Sim.`

**Etapa 7 — Perguntas de refinamento (uma por vez, com recomendacao):**

> "Sobre o perfil que acessa a renovacao:
> A) Apenas alunos com matricula ativa no periodo anterior **(recomendado)**
> B) Alunos ativos + alunos com matricula trancada que desejam reabrir
> C) Qualquer pessoa com vinculo (inclui ex-alunos)
>
> Qual se aproxima mais?"

Usuario: `A.`

> "Ok, A: apenas alunos ativos. Isso impacta a pergunta sobre prazos — se e so pra ativos, o periodo de renovacao provavelmente e uma janela fixa, nao aberto o ano todo. Ajusto e sigo."

> "Sobre prazos:
> A) Janela fixa de 30 dias antes do inicio do periodo **(recomendado)**
> B) Aberto o ano todo, sem prazo
> C) Duas janelas: uma prioritária (15 dias) e uma de ajuste (mais 15 dias)
>
> Qual?"

Usuario: `A.`

> "Ok, janela fixa de 30 dias. Isso implica que a pergunta sobre notificacao precisa incluir aviso de abertura e lembrete de fechamento. Mantenho."

> "Sobre aprovacao/homologacao da renovacao:
> A) Automatica apos confirmacao do aluno **(recomendado)**
> B) Passa por aprovacao da coordenacao de curso
> C) Passa por aprovacao da secretaria academica
>
> Qual?"

Usuario: `Nao sei.`

> "Registrado. (contador nao sei: 1)"

> "Sobre o que acontece se o aluno nao renovar no prazo:
> A) Matricula e automaticamente cancelada **(recomendado)**
> B) Matricula fica como 'pendente' e o aluno pode regularizar com justificativa
> C) Nada acontece, o sistema so nao gera a matricula do proximo periodo
>
> Qual?"

Usuario: `Nao sei.`

> "Registrado. (contador nao sei: 2)"

> "Sobre o comprovante de renovacao:
> A) Gera PDF automatico apos confirmacao **(recomendado)**
> B) So mostra mensagem de sucesso na tela, sem comprovante
> C) Envia comprovante por email
>
> Qual?"

Usuario: `Nao sei, pergunta pra ele.`

> **(Modo sabatina — 3 "nao sei" consecutivos)**
> "Percebi que 3 perguntas seguidas ficaram sem resposta. Voce consegue descobrir essas informacoes? Quem no time ou na instituicao saberia responder? Se preferir, posso registrar todas como pergunta em aberto, mas quero ter certeza de que nao ha como resolver nenhuma delas aqui antes de seguir."

Usuario: `Realmente nao sei — a coordenacao que decide isso. Deixa em aberto.`

> "Certo. Registrando as 3 como perguntas em aberto. (contador resetado)"

... (continua ate esgotar as 15 dimensoes do checklist)

### Etapa 7.5 — Confirmacao final

> "Antes de gerar os arquivos, confirma o resumo:
>
> **Decisoes tomadas (3):**
> - Perfil de acesso: apenas alunos ativos
> - Prazo: janela fixa de 30 dias antes do periodo
> - Comprovante: aguardando (em aberto)
>
> **Perguntas em aberto (3):**
> - Quem homologa a renovacao?
> - O que acontece se nao renovar no prazo?
> - Formato do comprovante?
>
> **Termos do glossario (2):**
> - Renovacao de matricula: processo em que o aluno confirma continuidade para o proximo periodo
> - Janela de renovacao: periodo fixo em que o sistema aceita confirmacoes
>
> **Premissas verificadas:** 0 confirmadas, 0 refutadas, 0 parciais, 5 nao verificaveis (sem fontes).
>
> Esta tudo certo? Gero os arquivos?"

Usuario: `Sim.`

### Etapa 8 — Arquivos gerados

Dois arquivos sao criados:
- `questionamentos/renovacao-matricula_tecnico.md` — com linguagem interna, glossario, mapa de dependencias
- `questionamentos/renovacao-matricula_solicitante.md` — com linguagem acessivel, wireframes, sem jargao

## Fluxo recomendado de uso

```
Email vago do cliente ("Preciso de uma tela de matricula")
        |
        v
refinamento-demanda-grill  ← "O que preciso perguntar pra ele?"
        |                     (identifica lacunas, gera questionarios)
        v
   [cliente responde]
        |
        v
criar-prd                  ← "Agora que tenho respostas, como escrevo
        |                     a spec pro dev implementar?"
        |                     (gera PRD com user stories, edge cases,
        |                      milestones, criterios de aceite)
        v
   implementacao (dev ou IA)
```

**Regra de ouro**: `refinamento-demanda-grill` = fase de perguntas. `criar-prd` = fase de spec. Nao misturar — cada uma tem saida diferente.

## Quando usar cada versao

| Cenario | Use |
|---|---|
| Demanda simples, voce ja conhece o dominio, so quer organizar | `refinamento-demanda` |
| Demanda complexa, muitas incertezas, voce nao sabe todas as respostas | `refinamento-demanda-grill` |
| O solicitante e tecnico e voce so precisa de um checklist | `refinamento-demanda` |
| O solicitante e leigo, voce precisa de um documento amigavel pra enviar | `refinamento-demanda-grill` |
| Quer recomendacoes do agente pra cada decisao | `refinamento-demanda-grill` |
| Prefere neutralidade total, sem opiniao do agente | `refinamento-demanda` |

## Instalacao

A skill ja esta no Hermes (`~/.hermes/skills/refinamento-demanda-grill/`) e no repo de skills (`~/git/skills/skills/refinamento-demanda-grill/`).

Para usar no Claude Code, crie um symlink:

```bash
ln -s ~/git/skills/skills/refinamento-demanda-grill ~/.claude/skills/refinamento-demanda-grill
```
