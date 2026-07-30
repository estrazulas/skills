# Detectores de Vaguidade

Ative alerta automático quando o texto contiver:

- **Comparação sem definição**: "similar a X", "análogo a", "mesma funcionalidade de Y", "no mesmo padrão de", "como já funciona em"
- **Modais fracos**: "quando for o caso", "se necessário", "eventualmente", "poderá", "deverá considerar"
- **Sujeito omitido**: "sistema deve permitir" (a quem?), "poderá ser feito" (por quem?)
- **Verbos de fluxo sem estados**: "convocar", "encaminhar", "aprovar", "homologar" — sem dizer o antes, o durante e o depois
- **Substantivos de domínio sem definição**: qualquer termo específico que aparece pela primeira vez e não tem definição no texto (nomes de perfis, etapas, artefatos)
- **Referências a "existente" não verificáveis**: "como já tem no sistema", "reaproveitar a tela X" — validar contra fontes ou marcar ❓
- **Números sem unidade ou fórmula**: "pontuação", "peso", "nota" — sem dizer intervalo, arredondamento, ponderação
