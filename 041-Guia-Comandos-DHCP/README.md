# Guia de Comandos - DHCP Server - LiveLinux xbnet 2.9

**Servidor DHCP:**

Arquivo de configuração:

`# nano /etc/dhcp/dhcpd.conf`

Configuração básica:

1) Remover o comentário para DHCP autoritativo:

`authoritative`

2) Adicionar uma sub-rede:

```
subnet 10.0.0.0 netmask 255.255.255.0 {
   range 10.0.0.2 10.255.255.254;
   option routers 10.0.0.1;
}
```

Reiniciar serviço DHCP:

`# /etc/init.d/isc-dhcp-server restart`

Verificar registros (logs):

`# egrep dhcp /var/log/syslog`

Verificar leases (concessões de IPs)

`# cat /var/lib/dhcp/dhcpd.leases`

**Cliente DHCP:**

`# dhclient eth0`

-> executa DHCP na interface eth0.
