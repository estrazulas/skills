# Criar Mermaid — Fluxograma de Requisitos

Skill que traduz especificações de requisitos de software em fluxogramas Mermaid.js com cobertura completa de caminhos felizes e infelizes.

## Uso rápido

```
/criar-mermaid <especificação do fluxo>
```

Exemplo mínimo:

```
/criar-mermaid Usuário faz login. Sistema valida credenciais. Se ok, vai pro dashboard. Se não, mostra erro e link de recuperação.
```

A skill gera o código Mermaid. Cole em qualquer renderizador Mermaid (GitHub, GitLab, Notion, Mermaid Live Editor, Obsidian).

## O que a skill garante

- **Contraste legível** — todo `classDef` declara `fill` + `color` + `stroke`. O diagrama funciona em tema claro e escuro.
- **Cobertura exaustiva** — cada risco vira um nó de erro. Cada decisão tem os dois ramos rotulados.
- **Estados de UI** — loading, empty state e error feedback aparecem como nós com classe própria.
- **Sintaxe semântica** — retângulos para ações, losangos para decisões, cantos arredondados para início/fim.

## Cenários de uso

### 1. Ideia bruta (sem análise de riscos)

Você tem uma descrição informal. A skill infere os pontos de falha.

```
/criar-mermaid O cliente escolhe um produto, informa o CEP, sistema calcula frete via API dos Correios,
exibe prazo e valor. Cliente confirma e vai pro pagamento.
```

Saída: fluxograma com nós de erro para API offline, CEP inválido, produto indisponível na região.

```mermaid
%%{init: {'theme': 'base'}}%%
graph TD
    A[Cliente escolhe produto] --> B[Informa CEP]
    B --> C[Consulta API de frete]
    C --> D{API respondeu?}
    D -->|Sim| E[Exibe prazo e valor]
    D -->|Não| F[Erro: API indisponível]
    F --> G[Tentar novamente?]
    G -->|Sim| C
    G -->|Não| H[Escolher outro produto]
    E --> I{CEP válido?}
    I -->|Sim| J{Produto disponível?}
    I -->|Não| K[Erro: CEP inválido]
    K --> B
    J -->|Sim| L[Cliente confirma]
    J -->|Não| M[Erro: Indisponível na região]
    M --> H
    L --> N[Ir para pagamento]

classDef error fill:#fee,color:#900,stroke:#c00
classDef success fill:#efe,color:#060,stroke:#393
classDef decision fill:#fff3cd,color:#630,stroke:#c90
classDef action fill:#e8e8e8,color:#222,stroke:#666
classDef startend fill:#d4edda,color:#155724,stroke:#28a745

class F,K,M error
class N success
class D,I,J decision
class A,B,C,E,G,H,L action
```

### 2. Com análise de riscos pronta

Você já tem riscos mapeados. A skill é exaustiva — cada risco declarado aparece no diagrama.

```
/criar-mermaid Fluxo: agendamento de consulta.
Riscos:
- API de disponibilidade retorna 500
- Horário escolhido é ocupado durante o submit (concorrência)
- Paciente sem cadastro ativo no convênio
- Timeout no gateway de pagamento (15s)
- Envio de email de confirmação falha
Caminho feliz: paciente escolhe data → sistema consulta vagas → paciente confirma →
sistema reserva → envia confirmação por email.
```

```mermaid
%%{init: {'theme': 'base'}}%%
graph TD
    A[Paciente escolhe data] --> B[Sistema consulta vagas]
    B --> C{API de disponibilidade respondeu?}
    C -->|Sim| D{Há vagas na data?}
    C -->|Não| E[Erro: API indisponível]
    E --> F[Tentar novamente mais tarde]
    D -->|Sim| G[Exibe horários disponíveis]
    D -->|Não| H[Empty: Sem vagas nesta data]
    H --> A
    G --> I[Paciente confirma horário]
    I --> J{Convênio do paciente ativo?}
    J -->|Sim| K[Reserva temporária]
    J -->|Não| L[Erro: Convênio inativo]
    L --> M[Encaminhar para central]
    K --> N[Gateway de pagamento]
    N --> O{Pagamento aprovado em 15s?}
    O -->|Sim| P[Sistema reserva horário]
    O -->|Não| Q[Erro: Timeout no pagamento]
    Q --> R[Reserva temporária expira]
    R --> A
    P --> S[Envia email de confirmação]
    S --> T{Email enviado?}
    T -->|Sim| U[Consulta agendada]
    T -->|Não| V[Erro: Email não enviado]
    V --> U

classDef error fill:#fee,color:#900,stroke:#c00
classDef success fill:#efe,color:#060,stroke:#393
classDef decision fill:#fff3cd,color:#630,stroke:#c90
classDef action fill:#e8e8e8,color:#222,stroke:#666
classDef empty fill:#f3e8ff,color:#5a0,stroke:#a3c
classDef startend fill:#d4edda,color:#155724,stroke:#28a745

class E,L,Q,V error
class U success
class C,D,J,O,T decision
class A,B,F,G,I,K,M,N,P,R,S action
class H empty
```

### 3. Fluxo com estados de tela (UX)

Quando o foco é a experiência do usuário entre telas.

```
/criar-mermaid App de pedidos: usuário acessa "Meus Pedidos".
Estados possíveis: carregando lista, lista vazia (primeiro acesso), erro de rede,
lista com pedidos, pedido sem status de entrega.
```

```mermaid
%%{init: {'theme': 'base'}}%%
graph TD
    A[Usuário acessa Meus Pedidos] --> B[Carregando lista de pedidos]
    B --> C{API de pedidos respondeu?}
    C -->|Sim| D{Há pedidos no histórico?}
    C -->|Não| E[Erro: Falha de rede]
    E --> F[Tentar novamente]
    F --> B
    D -->|Sim| G[Lista de pedidos carregada]
    D -->|Não| H[Empty: Nenhum pedido encontrado]
    H --> I[Que tal fazer seu primeiro pedido?]
    G --> J{Pedido tem status de entrega?}
    J -->|Sim| K[Exibe pedido com status de entrega]
    J -->|Não| L[Exibe pedido sem status — Aguardando transportadora]

classDef error fill:#fee,color:#900,stroke:#c00
classDef success fill:#efe,color:#060,stroke:#393
classDef decision fill:#fff3cd,color:#630,stroke:#c90
classDef action fill:#e8e8e8,color:#222,stroke:#666
classDef loading fill:#eef,color:#036,stroke:#69c
classDef empty fill:#f3e8ff,color:#5a0,stroke:#a3c

class E error
class B loading
class H empty
class C,D,J decision
class A,F,G,I,K,L action
```

### 4. Pós-PRD (validação visual)

Com user stories e edge cases já documentados.

```
/criar-mermaid PRD: Carrinho de compras.
US-03: Finalizar compra.
Edge cases:
- Item fica fora de estoque entre adicionar e finalizar
- Cupom de desconto expira durante o checkout
- Sessão do usuário expira após 30 min de inatividade
- Bandeira do cartão não aceita pela adquirente
```

```mermaid
%%{init: {'theme': 'base'}}%%
graph TD
    A[Carrinho com itens] --> B[Usuário clica em Finalizar compra]
    B --> C{Sessão ainda ativa?}
    C -->|Sim| D[Valida itens do carrinho]
    C -->|Não| E[Erro: Sessão expirada]
    E --> F[Redireciona para login]
    D --> G{Itens em estoque?}
    G -->|Sim| H[Usuário informa cupom]
    G -->|Não| I[Erro: Item fora de estoque]
    I --> J[Remove item e recalcula]
    J --> D
    H --> K{Cupom ainda válido?}
    K -->|Sim| L[Aplica desconto]
    K -->|Não| M[Erro: Cupom expirado]
    M --> N[Remove cupom, segue sem desconto]
    N --> L
    L --> O[Usuário informa cartão]
    O --> P{Bandeira aceita?}
    P -->|Sim| Q[Envia para adquirente]
    P -->|Não| R[Erro: Bandeira não aceita]
    R --> S[Sugere outra forma de pagamento]
    S --> O
    Q --> T{Pagamento aprovado?}
    T -->|Sim| U[Pedido confirmado]
    T -->|Não| V[Erro: Pagamento recusado]
    V --> S

classDef error fill:#fee,color:#900,stroke:#c00
classDef success fill:#efe,color:#060,stroke:#393
classDef decision fill:#fff3cd,color:#630,stroke:#c90
classDef action fill:#e8e8e8,color:#222,stroke:#666
classDef startend fill:#d4edda,color:#155724,stroke:#28a745

class E,I,M,R,V error
class U success
class C,G,K,P,T decision
class A,B,D,F,H,J,L,N,O,Q,S action
```

### 5. Composição com outras skills

O fluxograma como etapa de validação visual entre refino e PRD:

```
1. /refinamento-demanda   → refina a demanda, identifica riscos
2. /criar-mermaid          → fluxograma com os riscos mapeados (validação visual)
3. /criar-prd              → PRD com o fluxograma como referência
```

## Paleta de cores

| Nó | Classe | Aparência |
|---|---|---|
| Erro / falha | `error` | Fundo rosa claro, texto vermelho escuro |
| Sucesso / conclusão | `success` | Fundo verde claro, texto verde escuro |
| Decisão (losango) | `decision` | Fundo amarelo claro, texto marrom |
| Ação / processo | `action` | Fundo cinza claro, texto quase preto |
| Loading / espera | `loading` | Fundo azul claro, texto azul escuro |
| Empty state / vazio | `empty` | Fundo lilás claro, texto verde oliva |
| Início / fim | `startend` | Fundo verde suave, texto verde escuro |

## Como renderizar o diagrama

O output da skill é código Mermaid puro. Você pode colar em:

- **GitHub/GitLab** — blocos de código com ` ```mermaid `
- **Mermaid Live Editor** — https://mermaid.live
- **Obsidian** — suporte nativo a blocos mermaid
- **Notion** — via integração Mermaid
- **VS Code** — extensão "Markdown Preview Mermaid Support"
- **Qualquer arquivo `.md`** — renderizadores de markdown com suporte a Mermaid

## Por que o contraste funciona

O problema comum é declarar `classDef error fill:#f96` sem `color`. O Mermaid delega a cor do texto ao tema do renderizador. Se o tema for escuro (`neutral`, `dark`), o texto padrão é cinza claro (`#ccc`) sobre um preenchimento médio — ilegível.

Esta skill resolve com duas regras fixas:

1. **`%%{init: {'theme': 'base'}}%%`** força o tema neutro, que respeita cores explícitas
2. **`fill` + `color` + `stroke` sempre juntos** — fundo claro + texto escuro = contraste garantido em qualquer plataforma
