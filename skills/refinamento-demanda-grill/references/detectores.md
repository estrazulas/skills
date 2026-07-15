# Detectores de Vaguidade

Ative alerta automatico quando o texto contiver:

- **Comparacao sem definicao**: "similar a X", "analogo a", "mesma funcionalidade de Y", "no mesmo padrao de", "como ja funciona em"
- **Modais fracos**: "quando for o caso", "se necessario", "eventualmente", "podera", "devera considerar"
- **Sujeito omitido**: "sistema deve permitir" (a quem?), "podera ser feito" (por quem?)
- **Verbos de fluxo sem estados**: "convocar", "encaminhar", "aprovar", "homologar" — sem dizer o antes, o durante e o depois
- **Substantivos de dominio sem definicao**: qualquer termo especifico que aparece pela primeira vez e nao tem definicao no texto (nomes de perfis, etapas, artefatos)
- **Referencias a "existente" nao verificaveis**: "como ja tem no sistema", "reaproveitar a tela X" — validar contra fontes ou marcar ❓
- **Numeros sem unidade ou formula**: "pontuacao", "peso", "nota" — sem dizer intervalo, arredondamento, ponderacao
