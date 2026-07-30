# Sabatina — mecânica

Acionada quando o usuário escolhe **sabatina** na Etapa 1. No modo padrão nada aqui se aplica.

## Princípios adicionais

Valem junto aos 5 princípios da skill.

6. **Sabatina.** Toda resposta vaga, genérica ou "não sei" é sondada na hora, antes da próxima pergunta. Uma rodada por pergunta — se o usuário sustentar, registre como aberto e siga.
7. **Conecte decisões.** Após cada resposta, sinalize impactos nas perguntas futuras.

## Controle de estado interno

Mantenha silenciosamente durante todo o diálogo:

- **Contador de "não sei"**: incrementa a cada resposta vaga consecutiva. Reseta com decisão concreta. Não é gatilho da sabatina (ela já está ativa desde a primeira pergunta) — é o **freio**: ao atingir 3, pare de sondar, registre as lacunas em aberto em bloco e avise o usuário. Evita transformar o refinamento em interrogatório quando o solicitante realmente não tem a informação.
- **Lacunas sondadas**: quantas perguntas passaram por sondagem e quantas viraram decisão concreta depois dela. Usado no resumo da Etapa 11.
- **Glossário de domínio**: cada termo novo registrado com definição no momento em que aparece. Preenche a seção 4 do `template_tecnico.md`.
- **Mapa de dependências**: cada decisão tomada registra quais perguntas futuras foram impactadas. Entra como seção nova no arquivo técnico.

## Sondagem — toda resposta vaga

Toda resposta vaga, genérica ou "não sei" recebe **uma** rodada de sondagem antes da próxima pergunta:

> "Antes de seguir: você consegue descobrir isso? Quem saberia? Se não houver como resolver agora, registro como pergunta em aberto."

Uma rodada por pergunta, sem insistir. Se o usuário sustentar o "não sei", registre como aberto e avance — a decisão de não decidir é do usuário.

Contam como resposta vaga: "não sei", "tanto faz", "como for melhor", "do jeito que já é", "depois a gente vê", e escolhas que não resolvem a lacuna perguntada.

## Freio — 3 "não sei" consecutivos

Quando o contador atinge 3, a sondagem para de valer a pena. Suspenda a sondagem e alinhe o rumo:

> "Percebi que várias perguntas ficaram sem resposta. Prefere que eu registre todas as lacunas restantes como perguntas em aberto e siga direto para os arquivos, ou vale envolver quem tem esse contexto antes de continuar?"

Registre as lacunas pendentes em aberto, resete o contador e siga conforme a escolha.
