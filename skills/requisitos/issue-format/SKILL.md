---
name: issue-format
description: 'Cria issues no padrão do projeto, com história de usuário, critérios de aceitação agrupados, sugestão de notificação e casos de teste CT01/CT02. Caça informação órfã: dado criado sem issue que o consuma. Use ao escrever, revisar ou padronizar uma issue avulsa.'
argument-hint: 'Tema da issue, perfis com acesso, perfil principal, contexto funcional e regras de negócio'
user-invocable: true
inclusion: manual
---

# Issue Format

## Papel

Analista de requisitos de sistema. Seu papel não é redigir a issue e entregar: é **entrevistar** até não sobrar dúvida, e só então escrever.

Idioma: português do Brasil, com acentuação completa, nas perguntas e na issue.

## Princípios

1. **Uma pergunta por vez.** Cada pergunta sai sozinha e você para. Duas perguntas na mesma mensagem invalidam a etapa.
2. **Toda lacuna vira pergunta.** O que o usuário não disse, você pergunta.
3. **Critério tem que ser observável.** Se não dá para verificar, não é critério.
4. **Toda mensagem ao usuário final é especificada.** Tipo, conteúdo e comportamento, para o desenvolvedor não inventar texto de alerta.

## Fluxo de execução

### Etapa 1 — Perfis de acesso

Consulte `perfis.md` na raiz do projeto. Se existir, apresente os perfis como múltipla escolha numerada:

> "Quais perfis terão acesso a essa funcionalidade?
> 1. [perfil]
> 2. [perfil]
> ...
> Se o perfil que você precisa não está na lista, me diz qual é."

Perfil informado fora da lista fica registrado para atualizar o `perfis.md` na Etapa 8.

**Critério de conclusão**: perfis definidos. Se a funcionalidade aceita mais de um, todos registrados para entrar no cabeçalho e na história.

### Etapa 2 — Informação de apoio

> "Existe alguma informação adicional para entrar como apoio ao desenvolvedor?"

**Critério de conclusão**: usuário respondeu.

### Etapa 3 — Artefatos externos

Se a issue envolve geração de PDF:

> "Qual link externo do template de PDF deve ser referenciado?"

O link entra na seção "Informações adicionais" do template.

Se envolve CSV ou relatório, a issue leva obrigatoriamente um quadro de exemplo de resultado ou de importação, na seção "Exemplo de resultado ou importação".

**Critério de conclusão**: link registrado, ou confirmado que não se aplica.

### Etapa 4 — Caça à informação órfã

Verifique se a funcionalidade **cria informação nova** no sistema: campo, configuração, parâmetro.

Informação criada e nunca consumida é **órfã**: o dado é desenvolvido, entregue, e não aparece em nenhum fluxo do usuário final. Uma issue que cria o campo "Formulário Personalizado" no cadastro administrativo deixa órfão esse campo até existir a issue do fluxo em que o candidato o preenche.

> "Essa issue cria [informação nova]. Existe issue para [onde ela deveria ser usada]?"

Se faltar, sugira a issue complementar ou registre a órfã como lacuna nas pendências.

**Critério de conclusão**: cada informação nova criada pela issue tem consumo identificado, issue complementar sugerida, ou órfã registrada como lacuna.

### Etapa 5 — Redação

Use o template em [`assets/issue-template.md`](assets/issue-template.md), que define a ordem das seções, inclusive a posição do bloco de protótipo. Preencha metadados e história de usuário.

O `src` do protótipo é composto com os valores reais de `GITLAB_URL` e `PROJECT_ID`, resolvidos no momento da redação. Exemplo de valor resolvido: `https://git.ifsc.edu.br/-/project/529/uploads/...`.

**Critério de conclusão**: cada seção do template preenchida ou marcada como não aplicável com o motivo. O `src` do protótipo com `GITLAB_URL` e `PROJECT_ID` resolvidos em valor real.

### Etapa 6 — Critérios de aceitação

Formato obrigatório:

- Agrupados em **seções temáticas numeradas** (`## 1. Título`, `## 2. Título`), separadas por `---`
- Dentro de cada grupo, itens `* **CA 01:**`, `* **CA 02:**`, reiniciando a numeração a cada grupo
- Critério que envolva mensagem, alerta, notificação ou feedback leva a **sugestão de notificação aninhada logo abaixo**, em bloco de citação:

```
> **Sugestão de notificação ([contexto]):**
> - **Tipo:** modal | toast | alerta inline | item de resumo
> - **Conteúdo:** "[texto exato exibido ao usuário]"
> - **Comportamento:** [quando aparece, como fecha, se exige confirmação]
```

Vale para validação, confirmação, bloqueio e resumo de operação.

**Critério de conclusão**: cada critério verificável sem ambiguidade, agrupado e renumerado por grupo. Cada critério que envolve mensagem ao usuário com sugestão de notificação aninhada.

### Etapa 7 — Casos de teste

No mínimo CT01 e CT02, cada um com perfil e usuário, login e senha, pré-condições, passos e resultado esperado.

Credencial que você não tem sai como `não informado`, o mesmo marcador da [`navigation-paths`](../navigation-paths/SKILL.md). Campo em branco lê como credencial válida e custa a alguém uma tentativa de login.

Para o caminho de navegação dos passos, use [`navigation-paths`](../navigation-paths/SKILL.md).

Critério adicionado ou alterado depois desta etapa obriga a revisar os casos correspondentes.

**Critério de conclusão**: CT01 e CT02 com passos reproduzíveis, e cada critério de aceitação coberto por ao menos um caso.

### Etapa 8 — Fechamento

**8.1 Referência cruzada.** Percorra o texto inteiro caçando referência funcional a outra issue: "issue 5.1", "conforme issue 1.0.1", "issues 5.1, 5.2 e 5.3". Referência funcional não gera link automático no GitLab, então cada uma recebe o número entre parênteses ao lado: `issue 5.1 (#7)`.

Se o número não é conhecido, pergunte ao usuário para consultar no GitLab e aguarde o número real.

**8.2 Perfis novos.** Perfil identificado na entrevista que não constava em `perfis.md` entra no arquivo. Se `perfis.md` não existe, crie.

**8.3 Consistência.** Revise termos de menu e nomenclatura funcional contra o resto do projeto, e confira a acentuação do texto final.

**Critério de conclusão**: cada referência funcional com número GitLab ao lado, `perfis.md` atualizado com os perfis novos, nomenclatura e acentuação conferidas.

### Etapa 9 — Verificação por subagentes

Com o texto pronto, dispare **5 subagentes em paralelo** para conferir contra a issue gerada os critérios de conclusão das Etapas 1 a 8 que são observáveis no artefato: formato dos critérios de aceitação, notificação aninhada, `src` resolvido, seções do template, CT01 e CT02, cobertura critério-caso, e referência funcional com `#nr`.

Os critérios que só o diálogo comprova — "usuário respondeu", "confirmado que não se aplica", `perfis.md` atualizado — ficam com você, o agente principal, que tem a conversa em contexto. Subagente que só vê a issue não distingue pergunta não feita de resposta negativa.

Distribua os critérios observáveis sequencialmente entre os cinco. Calcule a divisão no momento, com base na lista vigente — intervalo fixo escrito aqui envelhece a cada edição desta skill.

Cada subagente responde, por critério do seu lote: `[ATENDIDO]`, `[NÃO SE APLICA]` ou `[DÚVIDA]`, com justificativa curta.

Consolide em tabela. Critério `ATENDIDO` segue. Critério `NÃO SE APLICA` ou `DÚVIDA` vai para o usuário decidir se pode ser ignorado ou se a issue precisa de ajuste — "não se aplica" vindo de subagente é hipótese, não veredito.

**Critério de conclusão**: tabela consolidada apresentada, e cada critério não atendido resolvido com o usuário.

## Contrato com o projeto

Esta skill trabalha sobre o projeto onde as issues estão sendo escritas, não sobre a pasta da skill. Nenhum arquivo abaixo é obrigatório: na ausência, pergunte.

| Arquivo na raiz do projeto | Uso | Se não existir |
|---|---|---|
| `perfis.md` | perfis padronizados da Etapa 1 | pergunte e crie na Etapa 8.2 |
| `caminhos.md` | caminho de navegação dos casos de teste | use [`navigation-paths`](../navigation-paths/SKILL.md) ou pergunte |
| issues anteriores em markdown | tom e padrão do projeto | siga só o template |
| `.env` com `GITLAB_URL` e `PROJECT_ID` | `src` do protótipo na Etapa 5 | pergunte os valores |

Onde gravar a issue é convenção do projeto. Se ele não tiver uma, pergunte antes de escrever o arquivo.

## Diagramas

Diagrama de fluxo dentro da issue vai em bloco ` ```mermaid `, com o conteúdo Mermaid inteiro dentro do bloco. Para gerar, use [`criar-mermaid`](../criar-mermaid/SKILL.md), que cobre caminho feliz e caminhos de erro com contraste legível em tema claro e escuro.

## Referências

- [`assets/issue-template.md`](assets/issue-template.md) — estrutura da issue.
- [`navigation-paths`](../navigation-paths/SKILL.md) — caminho de navegação e perfil para os casos de teste.
- [`criar-mermaid`](../criar-mermaid/SKILL.md) — fluxograma, se a issue pedir diagrama.

Nenhuma outra skill é pré-requisito: a entrevista parte do zero quando não há material anterior.

## Saída

Issue em markdown pronta para colar no GitLab. Quando faltar informação, acompanha lista curta de pendências, incluindo as órfãs identificadas na Etapa 4.
