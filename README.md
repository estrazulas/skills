# Skills

Skills pessoais para agentes de IA. Cada skill é uma pasta com `SKILL.md` dentro de `skills/`.

## Instalação

Copie a pasta da skill desejada para o diretório de skills do seu agente:

```bash
# Exemplo para Claude Code
cp -r skills/<nome-da-skill> ~/.claude/skills/

# Exemplo para outros agentes
cp -r skills/<nome-da-skill> <diretorio-de-skills-do-agente>/
```

Cada agente tem seu próprio mecanismo de descoberta de skills. Consulte a documentação do agente que você está usando.

## Skills

### Texto
- **casual-chat** — reescreve ou traduz texto para inglês informal de grupo dev (Discord/Telegram), removendo padrões de IA
- **humanizer-pt-br** — remove traços de escrita gerada por IA de textos em português brasileiro, tornando-os mais naturais

### Dev
- **caveman-commit** — gera mensagens de commit ultra-compactas no formato Conventional Commits
- **developer** — agente de desenvolvimento Node.js/TypeScript com TDD, SOLID e dependency injection
- **security-review** — revisão de segurança de código para vulnerabilidades (OWASP, XSS, injection, auth, etc.)

### Mídia
- **estudos** — processa vídeos do YouTube e gera mapas mentais em markdown + Mermaid
- **ffmpeg** — processamento de vídeo/áudio: conversão, compressão, resize, extração de áudio
- **md-to-pdf** — converte markdown para PDF preservando hyperlinks (usa Chrome headless)

### Headroom
- **headroom-auth** — gerencia o sistema de auth do HeadroomGate: times, usuários, chaves API, roles
- **headroom-clean-e2e** — limpa usuários, chaves e times criados pelos testes e2e/admin do HeadroomGate
- **headroom-doctor** — diagnostica problemas no proxy Headroom: containers, portas, logs, endpoints

### Produtividade
- **resumo-tarefas** — gera resumo diário das tarefas criadas ou modificadas nos últimos 2 dias
- **tarefa** — salva e arquiva tarefas como `.md` numa pasta configurável

### Util
- **deepseek-saldo** — consulta o saldo disponível na conta DeepSeek via API
- **discord_reader** — lê as últimas mensagens de um canal do Discord e opcionalmente gera resumo com IA
- **find-skills** — busca e instala skills do ecossistema skills.sh
- **fix-network** — diagnostica e corrige rede de VM VirtualBox após save/restore

### Requisitos (requisitos/)
- **criar-mermaid** — gera fluxograma Mermaid.js a partir de especificação de requisitos
- **criar-prd** — gera PRD + user stories a partir de entrevista estruturada
- **refinamento-demanda** — refina demandas mal especificadas em questionários estruturados
- **refinamento-demanda-grill** — refinamento intensivo com questionamento profundo (modo sabatina)

### Coleção Externa
- **mattpocock** — coleção de 30 skills de Matt Pocock (code review, TDD, domain modeling, etc.)

### IFSC (ifsc_util/)

Sub-skills utilitárias para o contexto institucional IFSC:

- **compilar-relatorio** — compila relatório final combinando plano de trabalho (issues GitLab) e descrição de chamados
- **descrever-chamados** — formata chamados atendidos no período, classificando por tipo e sistema
- **plano-trabalho** — cria resumo de plano de trabalho a partir de issues do GitLab usando template padronizado
- **spec-para-issues** — converte specs do Kiro (requirements/design/tasks) em issues no padrão do projeto de requisitos
