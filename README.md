# Skills

Skills pessoais para Claude Code e Hermes. Cada skill é uma pasta com `SKILL.md` dentro de `skills/`.

## Skills

- **casual-chat** — reescreve ou traduz texto para inglês informal de grupo dev (Discord/Telegram), removendo padrões de IA
- **caveman-commit** — gera mensagens de commit ultra-compactas no formato Conventional Commits
- **deepseek-saldo** — consulta o saldo disponível na conta DeepSeek via API
- **developer** — agente de desenvolvimento Node.js/TypeScript com TDD, SOLID e dependency injection
- **discord_reader** — lê as últimas mensagens de um canal do Discord e opcionalmente gera resumo com IA
- **estudos** — processa vídeos do YouTube e gera mapas mentais em markdown + Mermaid
- **ffmpeg** — processamento de vídeo/áudio: conversão, compressão, resize, extração de áudio
- **find-skills** — busca e instala skills do ecossistema skills.sh
- **fix-network** — diagnostica e corrige rede de VM VirtualBox após save/restore
- **headroom-auth** — gerencia o sistema de auth do HeadroomGate: times, usuários, chaves API, roles
- **headroom-clean-e2e** — limpa usuários, chaves e times criados pelos testes e2e/admin do HeadroomGate
- **headroom-doctor** — diagnostica problemas no proxy Headroom: containers, portas, logs, endpoints
- **humanizer-pt-br** — remove traços de escrita gerada por IA de textos em português brasileiro, tornando-os mais naturais
- **md-to-pdf** — converte markdown para PDF preservando hyperlinks (usa Chrome headless)
- **mem** — lista e busca nas memórias persistentes do projeto
- **refinamento-demanda** — analista de requisitos que refina demandas mal especificadas antes de virarem issue/spec
- **resumo-tarefas** — gera resumo diário das tarefas criadas ou modificadas nos últimos 2 dias
- **supabase** — guia de desenvolvimento Supabase: changelog, verificação, API, error recovery
- **supabase-postgres-best-practices** — otimização de queries Postgres: índices, pooling, RLS, schema design
- **tarefa** — salva e arquiva tarefas como `.md` numa pasta configurável

## Skills IFSC (ifsc_util/)

Sub-skills utilitárias para o contexto institucional IFSC:

- **compilar-relatorio** — compila relatório final combinando plano de trabalho (issues GitLab) e descrição de chamados
- **descrever-chamados** — formata chamados atendidos no período, classificando por tipo e sistema
- **plano-trabalho** — cria resumo de plano de trabalho a partir de issues do GitLab usando template padronizado
- **spec-para-issues** — converte specs do Kiro (requirements/design/tasks) em issues no padrão do projeto de requisitos
