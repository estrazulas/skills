# MarkText no Ubuntu — visualizador de `.md` com Mermaid

Abre `.md` com duplo clique, renderiza **Mermaid**, imagens, tabelas, KaTeX. Open source, leve, sem ser IDE ou terminal.

## Instalação

```bash
# 1. Instalar Flatpak
sudo apt update && sudo apt install -y flatpak gnome-software-plugin-flatpak

# 2. Instalar MarkText (adiciona Flathub se não existir)
flatpak install flathub com.github.marktext.marktext
```

## Associar `.md` ao duplo clique

O `xdg-mime` não basta — Ubuntu/GNOME usa GIO, e o GIO não enxerga o desktop file do Flatpak em `/var/lib/flatpak/exports/…`.

```bash
# 1. Link simbólico pro GIO encontrar o desktop file
ln -sf /var/lib/flatpak/exports/share/applications/com.github.marktext.marktext.desktop \
       ~/.local/share/applications/com.github.marktext.marktext.desktop

# 2. Associar via GIO (não xdg-mime)
gio mime text/markdown com.github.marktext.marktext.desktop

# 3. Reiniciar Nautilus
nautilus -q

# 4. (Opcional) Forçar reload da shell GNOME
# Alt+F2 → r → Enter
```

## Verificar

```bash
gio mime text/markdown
# Deve mostrar:
#   Default application for "text/markdown": com.github.marktext.marktext.desktop
```

Depois disso, duplo clique no `.md` → abre no MarkText.
