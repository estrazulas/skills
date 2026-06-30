---
name: spec-para-issues
description: 'Converter specs geradas pelo Kiro (requirements.md, design.md, tasks.md) em issues no padrão do projeto de requisitos, com rastreabilidade completa entre requisitos, issues e tasks. Use ao transformar uma spec técnica em issues objetivas para desenvolvedores que podem ou não implementar com IA. Não use para criar uma issue avulsa sem spec de origem — nesse caso use a skill issue-format.'
argument-hint: 'Caminho da spec (.kiro/specs/<nome>) ou branch onde está a spec'
user-invocable: true
inclusion: manual
---

# Skill: Spec para Issues

Transforma specs técnicas geradas pelo Kiro em **issues no padrão do projeto de requisitos**, mantendo rastreabilidade entre os requisitos da spec, as issues criadas e as tasks de implementação.

## Filosofia

- A **spec do Kiro** (requirements/design/tasks) é técnica e detalhada, voltada para implementação assistida por IA.
- As **issues** geradas dão o **contexto geral e objetivo** ao desenvolvedor, que pode implementá-las manualmente caso não queira ou não possa usar IA (ex.: sem créditos no Kiro disponíveis).
- As issues continuam **referenciando a spec** no link do repositório, para quem quiser implementar com as tasks.
- Toda issue gerada segue o padrão da skill **issue-format** do projeto de requisitos.

## Quando usar
- Existe uma spec gerada pelo Kiro em `.kiro/specs/<nome>` e o usuário quer issues para os desenvolvedores.
- O usuário quer mapear cobertura entre requisitos e issues.
- O usuário quer atualizar a spec para manter rastreabilidade após identificar lacunas.

## Pré-requisitos
- A skill **issue-format** define o formato das issues (história de usuário, critérios de aceitação, sugestões de notificação, casos de teste CT01/CT02). Siga-a ao redigir cada issue.
- As issues são salvas em `data/alteracoes_DDMMYYYY` do projeto de requisitos, conforme regras do harness.

## Fluxo de Execução

### 1. Localizar e ler a spec
1. Identificar a branch atual do repositório de código (`git branch --show-current`) caso o usuário não informe o caminho.
2. Localizar a spec em `.kiro/specs/<nome>/` (arquivos `requirements.md`, `design.md`, `tasks.md`).
3. Ler `requirements.md` integralmente — é a fonte de verdade dos requisitos.
4. Ler `design.md` e `tasks.md` para entender estrutura técnica, nomes de colunas/campos, e o que já está planejado.

### 2. Propor a organização das issues (SEMPRE antes de escrever)
1. Analisar os requisitos e agrupar logicamente por **perfil afetado** e **camada/fluxo** (ex.: interface do candidato, CRUD admin, exportação, auditoria).
2. Apresentar uma **lista numerada** das issues propostas (número, título, perfil) e **aguardar confirmação** do usuário.
3. Não escrever nenhuma issue antes do usuário confirmar a organização.
4. Evitar granularidade excessiva: requisitos puramente técnicos (migrations, validações, persistência) normalmente entram como critérios de uma issue funcional, não como issue separada. Confirmar o nível de granularidade com o usuário.

### 3. Entrevistar o usuário — UMA pergunta por vez
Antes de redigir cada issue (ou bloco de issues), levantar o que a spec não deixa claro do ponto de vista funcional, **uma pergunta por vez**, aguardando resposta:
- Perfis de acesso (consultar `perfis.md` do projeto de requisitos como base).
- Onde a funcionalidade fica na interface (tela, aba, menu).
- Filtros opcionais ou obrigatórios.
- Informação adicional de apoio ao desenvolvedor.
- Nunca assumir o que não foi fornecido — perguntar.

### 4. Redigir as issues
1. Seguir o template e as regras da skill **issue-format**.
2. Salvar em `data/alteracoes_DDMMYYYY` (data atual) do projeto de requisitos.
3. Na seção **"Informações adicionais para o desenvolvedor"**, incluir **apenas o link da spec no repositório** (branch + caminho `.kiro/specs/<nome>`). Não copiar detalhes técnicos da spec (migrations, models, services) — o dev acessa a spec se quiser.
4. Manter exemplos de formato esperado quando fizer sentido (ex.: exemplo de CSV, exemplo de JSON), pois ajudam o dev.
5. Escrever em pt-BR fluido. Nomes de colunas, propriedades e código permanecem em inglês conforme o padrão do projeto de código.
6. Adicionar referências de dependência entre issues quando houver (ex.: "Esta issue depende da issue X.Y (#?)").

### 5. Verificar cobertura requisitos → issues
1. Montar uma tabela mapeando **cada requisito da spec** para a(s) issue(s) que o cobrem.
2. **Decisão sobre subagentes (ver seção "Uso de subagentes")**: se a spec for grande (muitos requisitos/critérios) ou houver muitas issues, sugerir ao usuário disparar subagentes em paralelo — um por requisito ou por issue — para verificar a cobertura. Para specs pequenas, fazer a verificação diretamente.
3. Classificar cada requisito como Coberto / Parcial / Não coberto e apresentar o relatório.

### 6. Corrigir lacunas
1. Para lacunas identificadas, **adicionar critérios de aceitação extras** nas issues — em linguagem funcional/de situação, sem entrar em detalhe técnico de implementação de código.
   - Exemplo: em vez de descrever a query SQL, escrever "o sistema deve validar no servidor que o tipo informado é um dos valores permitidos".
2. Discutir as correções com o usuário **uma por uma**, explicando o contexto de cada uma em linguagem leiga quando o usuário pedir, e exemplificando sempre quais campos/itens estão envolvidos.
3. Aplicar apenas as correções que o usuário aprovar.

### 7. Revisar clareza e português
1. **Decisão sobre subagentes**: se forem muitas issues ou issues longas, sugerir disparar um subagente por issue para revisar clareza para o dev, linguagem (pt-BR), consistência entre critérios e casos de teste, e pontos ambíguos. Para poucas issues curtas, revisar diretamente.
2. Consolidar o relatório com marcação [OK] / [ATENÇÃO] / [ERRO].
3. Discutir os ajustes com o usuário **um por um** antes de aplicar.

### 8. Garantir rastreabilidade na spec (atualizar de volta)
Quando a verificação revelar que a spec original **não cobre** algo definido nas issues (ex.: uma issue nova de auditoria, ou um requisito de tabela auxiliar):
1. Atualizar `requirements.md` da spec adicionando os novos requisitos no mesmo formato (SHALL / WHEN / IF-THEN).
2. Atualizar `tasks.md` adicionando as tasks correspondentes, com referência `_Requirements: X.Y_` e atualizando o grafo de dependências (waves) se existir.
3. Atualizar a seção de notas da spec indicando dependências entre as novas issues.
4. Isso mantém a rastreabilidade bidirecional: spec → issues e issues → spec.

## Uso de subagentes

Avalie o **tamanho do pedido** antes de decidir:
- **Sugerir subagentes** quando: a spec tem muitos requisitos (ex.: 8+), há muitas issues a verificar/revisar, ou os arquivos são grandes. Nesses casos, propor ao usuário disparar subagentes em paralelo (um por requisito ou por issue) — é mais rápido e preserva o contexto principal.
- **Fazer diretamente** quando: a spec é pequena, poucas issues, arquivos curtos. Não há ganho em paralelizar.
- Sempre **sugerir** ao usuário e deixá-lo decidir, em vez de disparar subagentes automaticamente sem avisar.

## Regras importantes
- Seguir sempre a skill **issue-format** para o formato das issues.
- Propor a organização das issues em lista e aguardar confirmação antes de escrever.
- Entrevistar uma pergunta por vez; nunca assumir o que não foi informado.
- Issues em pt-BR fluido; nomes técnicos (colunas, propriedades) em inglês.
- Seção "Informações adicionais para o desenvolvedor" deve conter apenas o link da spec.
- Critérios extras de correção em linguagem funcional, não em detalhe de código.
- Discutir correções e ajustes um a um com o usuário.
- Ao final, garantir rastreabilidade atualizando a spec (requirements + tasks) quando necessário.

## Saída esperada
- Conjunto de issues em Markdown no padrão do projeto, salvas em `data/alteracoes_DDMMYYYY`.
- Relatório de cobertura requisitos → issues.
- Spec atualizada (requirements.md + tasks.md) quando houver lacunas de rastreabilidade.
