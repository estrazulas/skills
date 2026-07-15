# Ordem de Prioridade das Perguntas

1. **Contexto** — em qual sistema/produto esta feature se insere, qual a stack, o que ja existe hoje. Essas informacoes tornam o PRD autocontido — sem elas, nao ha contexto suficiente para implementar.
2. **Problema** — qual dor esta feature resolve, quem e afetado, qual o impacto de nao resolver
3. **Solucao** — visao geral do que sera construido
4. **Funcionalidades** — quais sao as funcionalidades principais? Para cada uma, identificar:
   - User Story (quem, o que, por que)
   - Rules (regras de negocio, limites, restricoes, comportamentos esperados)
   - Edge cases (situacoes de erro, concorrencia, limites, inputs inesperados)
5. **Decisoes-chave** — escolhas de arquitetura ou produto ja definidas
6. **Escopo negativo** — o que explicitamente fica de fora
7. **Criterios de aceite** — se usuario optou por metricas na Etapa 3, perguntar baselines e metas. Senao, apenas criterios tecnicos.
8. **Milestones** — fases de entrega com valor incremental, referenciando as US
9. **Riscos e dependencias** — o que pode dar errado, o que bloqueia
10. **Referencias** — existem documentos, issues, PRDs relacionados, APIs ou recursos externos relevantes para esta feature?

Para cada funcionalidade identificada, faca perguntas direcionadas de edge cases:
- "O que acontece se [recurso/servico] nao estiver disponivel?"
- "E se dois usuarios fizerem isso ao mesmo tempo?"
- "Qual o comportamento quando o input esta no limite ou e invalido?"
- "O que acontece em caso de falha parcial?"
