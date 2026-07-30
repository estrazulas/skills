---
name: navigation-paths
description: 'Identifica caminho de navegação no sistema, perfil recomendado e login sugerido a partir do caminhos.md do projeto. Use quando pedirem o caminho para chegar numa funcionalidade, qual perfil acessa uma tela, ou roteiro de navegação para teste.'
argument-hint: 'Objetivo funcional, perfil desejado (opcional) e contexto da tela'
user-invocable: true
inclusion: manual
---

# Navigation Paths

Idioma: português do Brasil, com acentuação completa.

## Quando usar

Alguém pede o caminho para chegar numa funcionalidade, qual perfil deve acessar uma tela, ou um roteiro de navegação para teste e validação.

## Fonte de verdade

O arquivo **`caminhos.md` na raiz do projeto** onde a navegação está sendo mapeada — não na pasta desta skill. Leia antes de responder.

Se o projeto não tem `caminhos.md`, diga isso na resposta e pergunte o caminho ao usuário, em vez de inferir menu que talvez não exista.

## Normalização do caminho

Formato: `Entrar -> Menu -> Submenu -> Ação`.

Use os nomes de menu como aparecem no projeto, sem traduzir nem abreviar. Valor variável entra como marcador em colchetes: `[parâmetro]`, `[identificador]`, `[registro]`.

## Seleção de perfil

O `caminhos.md` mapeia perfil por funcionalidade. Se o mapeamento não estiver lá, pergunte qual perfil deve ser usado.

## Informação faltante

Declare a lacuna em vez de preencher com suposição:

| Situação | O que escrever |
|---|---|
| login ou senha não definidos | `não informado` |
| perfil não mapeado no `caminhos.md` | `perfil a confirmar`, e pergunte |
| parâmetro não definido | marcador variável entre colchetes |
| caminho incompleto no dataset | `caminho parcial`, explicitamente |

## Formato de saída

Use o template em [`assets/path-response-template.md`](assets/path-response-template.md): três blocos, nesta ordem — perfil recomendado com login e senha, caminho de navegação, observações com variáveis e dependências.

**Critério de conclusão**: os três blocos preenchidos, cada passo do caminho vindo do `caminhos.md` ou perguntado ao usuário, e cada informação ausente declarada com o marcador da tabela acima. Nenhum passo, perfil ou credencial inferido em silêncio.

## Referências

- [`issue-format`](../issue-format/SKILL.md) — consome o caminho de navegação nos casos de teste CT01/CT02.
