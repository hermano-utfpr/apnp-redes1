# Guia de Comandos - IPTables NAT

Verificar regras:

`# iptables -t nat -L -n -v`
-t tabela NAT
-L listar
-n não resolver DNS
-v verbose, detalhado (bytes e pacotes)

Exemplos de regras utilizadas nas aulas:

Regra utilizada para redes privadas utilizarem apenas um endereço IP:

`# iptables -t nat -I POSTROUTING -s [REDE_PRIVADA] -o [IFACE] -j MASQUERADE`
-> -I Initial, início da lista (pós roteamento)
-> -s IP, Rede de origem
-> -o Output, interface de saída
-> -j Ação (masquerade, mascarar IP de origem)

Regra utilizada para permitir à rede externa acessar um serviço na rede privada:

`# iptables -t nat -I PREROUTING -p [PROTO] --dport [PORT] -i [IFACE] -j DNAT --to-destination [IP:PORT]`
-> -I Initial, início da lista (pré roteamento)
-> -p Protocolo (ip, icmp, tcp ou udp)
-> --dport Porta destino (no caso de tcp ou udp)
-> -i Input, interface de entrada
-> -j Ação, NAT destino, traduzido para o destino IP:PORT

Remover todas as regras:

`# iptables -t nat -F`
