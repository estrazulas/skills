---
name: fix-network
description: >
  Diagnoses and fixes VirtualBox VM network after save/restore state. Deploys fix-network script
  to ~/.local/bin/. Use when the user reports "internet stopped working", "network dead after
  restoring VM", "e1000 link down", or "VirtualBox save state broke network". Auto-detects the
  e1000 driver issue and offers to deploy the recovery script.
---

# fix-network — Recuperação de Rede VirtualBox

Ao salvar/restaurar estado de VM no VirtualBox com driver e1000, o NetworkManager falha em renovar DHCP e a rede fica inoperante. Este skill implanta um script de recuperação com 3 níveis progressivos que resolve sem precisar reiniciar a VM.

## Diagnóstico rápido

Antes de implantar o script, verifique se o problema é realmente o e1000 save/restore:

```bash
# 1. O driver é e1000?
ethtool -i enp0s3 | grep ^driver

# 2. Tem evidência do problema nos logs?
journalctl --no-pager -n 100 | grep -E "e1000.*Link is Down|ip-config.*failed.*enp0s3"
dmesg | grep -E "e1000.*Link is Down"
```

Se aparecer `driver: e1000` e `NIC Link is Down` nos logs, o diagnóstico está confirmado.

## Implantação

### Via skill (recomendado)

Peça ao Claude: **"deploy the fix-network script"** ou **"instala o fix-network"** e o skill cuidará do resto.

### Instalação manual

```bash
# Copia o script para o PATH
sudo cp scripts/fix-network /usr/local/bin/fix-network
sudo chmod +x /usr/local/bin/fix-network
```

## Script fix-network

O script tem 3 níveis progressivos de recuperação:

| Nível | Ação | Quando resolve |
|-------|------|---------------|
| **1. Soft** | `nmcli connection down/up` | 80% dos casos |
| **2. Medium** | `ip link down/up` + renovar DHCP | Driver ok, DHCP preso |
| **3. Hard** | `modprobe -r e1000 && modprobe e1000` | Driver em estado interno zoado |

### Uso após instalação

```bash
fix-network              # sempre corrige (padrão)
fix-network --check      # só verifica, não mexe
fix-network --interface enp0s8  # interface específica
fix-network --help       # ajuda completa
```

## Como o script funciona

1. **Pinga o gateway** — se responder, rede está OK (sai, a menos que modo force)
2. **Nível 1**: Desconecta/reconecta a conexão no NetworkManager (`nmcli connection down/up`)
3. **Nível 2**: Derruba/sobe a interface no kernel (`ip link down/up`) + renova DHCP via dhcpcd/dhclient
4. **Nível 3**: Remove e recarrega o módulo e1000 do kernel (`modprobe -r/modprobe`)

O script se auto-eleva com sudo quando necessário. Os gateways e nomes de conexão são auto-detectados.

## Contexto técnico

- **Plataforma**: VirtualBox 7.x com Ubuntu (Netplan + NetworkManager)
- **Driver**: e1000 (Intel 82540EM Gigabit Ethernet)
- **Causa raiz**: Ao restaurar estado, kernel reporta `e1000: enp0s3 NIC Link is Down`, depois `carrier: link connected`, mas o NetworkManager falha na renovação DHCP com `ip-config-unavailable`
- **Sintoma**: `ping 10.0.2.2` falha, `ip addr` mostra interface UP mas sem conectividade
- **Solução permanente**: Usar driver virtio-net em vez de e1000 (requer recriar a VM) ou manter o script instalado
