# [número.versão] [perfil] [título da issue]

**Estado:** opened
**Autor:** [nome do autor]

---

Como um **[perfil]**, eu quero que **[funcionalidade]** para que **[benefício]**.

## Objetivo do usuário final

[descrever o ganho direto para o usuário]

## Objetivo final de negócio

[descrever impacto no processo ou na organização]

## Critérios de aceitação

Organize os critérios em **seções temáticas numeradas** (`## 1. Título do grupo`, `## 2. ...`), separadas por `---`. Dentro de cada grupo, liste os critérios como itens `* **CA 01:**`, `* **CA 02:**` ... reiniciando a numeração a cada grupo. Quando um critério envolver mensagem, alerta ou feedback ao usuário, aninhe a sugestão de notificação logo abaixo dele, em bloco `>` com Tipo, Conteúdo e Comportamento.

## 1. [Título do primeiro grupo de critérios]
* **CA 01:** [regra verificável]
* **CA 02:** [regra verificável]
    > **Sugestão de notificação ([contexto]):**
    > - **Tipo:** [modal | toast | alerta inline | item de resumo]
    > - **Conteúdo:** "[texto exato exibido ao usuário]"
    > - **Comportamento:** [quando aparece, como fecha, se exige confirmação]

---

## 2. [Título do segundo grupo de critérios]
* **CA 01:** [regra verificável]
* **CA 02:** [regra verificável]

<div align="center">

  <img src="[GITLAB_URL]-/project/[PROJECT_ID]/uploads/..." alt="Protótipo sugestivo" style="display: block; margin: 0 auto;">
  <br>
  <p align="center">
    <b>Figura 1:</b> Protótipo (SUGESTIVO) da funcionalidade.
  </p>
</div>

## Informações adicionais

[informações de apoio ao desenvolvedor, quando existirem]

## Exemplo de resultado ou importação (quando o requisito exigir)

| Campo | Exemplo |
| --- | --- |
| [registro 1] | [valor esperado] |
| [registro 2] | [valor esperado] |

ou

```csv
campo,exemplo
registro1,"valor texto exemplo1"
registro2,"valor, com vírgula exemplo2"
```

## Casos de teste

### CT01: [nome do cenário principal]
* **Perfil/Usuário:** [perfil] / Login: `[login]` Senha: `[senha]`
* **Pré-condições:**
    1. [pré-condição 1]
    2. [pré-condição 2]

* **Passos:**
    1. [passo 1]
    2. [passo 2]
    3. [passo 3]

* **Resultado esperado:**
   * [resultado 1]
   * [resultado 2]

### CT02: [nome do cenário alternativo]
* **Perfil/Usuário:** [perfil] / Login: `[login]` Senha: `[senha]`
* **Pré-condições:**
    1. [pré-condição 1]

* **Passos:**
    1. [passo 1]
    2. [passo 2]

* **Resultado esperado:**
   * [resultado 1]
