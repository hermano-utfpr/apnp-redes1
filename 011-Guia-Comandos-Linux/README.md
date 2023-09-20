# Guia de Comandos - Redes Linux - LiveLinux xbnet 2.9

**1) Verificar e endereçar interfaces:**

`linux# ifconfig`

(lista as interfaces ativas)

`linux# ifconfig -a`

(lista todas as interfaces)

`linux# ifconfig eth0 up`

(ativa a interface eth0)

`linux# ifconfig eth0 192.168.0.1 netmask 255.255.255.0`

(atribui um endereço e uma máscara para uma interface)

**2) Alcançabilidade:**

`linux# arp`

(lista a tabela ARP)

`linux# arp -n`

(lista a tabela ARP sem a resolução de nomes)

`linux# tcpdump -ni eth0 arp`

(captura os pacotes arp da interface eth0)

Tecle [CTRL+c] para parar.

`linux# ping 192.168.0.2`

(envia ICMP request para o host 192.168.0.2)

Tecle [CTRL+c] para parar.

`linux# ping -c 1 192.168.0.2`

(envia apenas um ICMP request)

`linux# ping -I eth1 192.168.0.2`

(envia um ICMP request com endereço da interface eth1)

Tecle [CTRL+c] para parar.

`linux# tcpdump -ni eth0 icmp`

(captura os datagramas ICMP da interface eth0)

Tecle [CTRL+c] para parar.

`linux# traceroute -I 192.168.10.2`

(traçar a rota até 192.168.10.2 utilizando ICMP)

Obs: por padrão o traceroute utiliza um protocolo de camada 4, mas colocar o "-I" faz com o que o traceroute utilize ICMP ao invés de UDP.

**3) Roteamento:**

`linux# sysctl -a | egrep ip_forward`

(verifica se o roteamento está ativado)

`linux# sysctl net.ipv4.ip_forward=1`

(ativa o roteamento)

`linux# cat /proc/sys/net/ipv4/ip_forward`

(verifica se o roteamento está ativado)

`linux# echo 1 > /proc/sys/net/ipv4/ip_forward`

(ativa o roteamento)

`linux# route`

(verificar as rotas)

`linux# route -n`

(verificar as rotas sem resolver nomes)

`linux# route add default gw 192.168.0.1`

(adicionar uma rota para a saída padrão)

`linux# route del default`

(remover uma rota para a saída padrão)

`linux# route add -net 192.168.10.0/24 gw 192.168.0.1`

(adiciona uma rota para a rede 192.168.10.0/24 fazendo com que o portão (gateway) seja o endereço 192.168.0.1)

`linux# route del -net 192.168.10.0/24`

(remove a rota para a rede 192.168.10.0/24)

**4) Comunicação NetCat:**

Ferramenta netcat:

`linux# nc -h`

Comunicação TCP:

`server# nc -l -p 3000`

`client# nc 10.0.0.1 3000`

Comunicação UDP:

`server# nc -l -p 3000 -u`

`client# nc 10.0.0.1 3000 -u`

Transferir arquivos (TCP):

`server# nc -l -p 3000 -q 0 < file.txt`

`client# nc 10.0.0.1 3000 > file.txt`

Transferir arquivos (UDP):

`server# nc -u -l -p 4000 > file.txt`

`client# cat file.txt | nc -u 10.0.0.1 4000`

(use ctrl+c para encerrar)

**5) Filtros com TCPdump**

`# tcpdump [-?] [interface] [filtro]`

- (-n) não resolve nomes reversos

- (-A) conteúdo da mensagem em ASCII

- (-i) identificar interface para capturar

- (-e) lista os endereços MACs

- (-X) conteúdo da mensagem em hexadecimal e ASCII

Filtros:

- (src) origem

- (dst) destino

- (host [ip]) um endereço IP

- (net [ip/mask]) um bloco de endereços IPs

Exemplos:

`# tcpdump -nAi eth0`

`# tcpdump -i eth0 arp`

`# tcpdump -nei eth0 host 200.1.0.20`

`# tcpdump -ni eth0 src host 187.0.0.7 and dst net 200.1.0.0/24`

`# tcpdump -ni eth0 tcp port 3000`

**6) Mapeamento com NMAP**

`# nmap [-?] [ip/rede]`

Opções:

-sP - Ping

-sS - TCP Syn

-sU - UDP

-pN - Portas

-n  - Não resolver DNS

Exemplos:

`# nmap -n -sP 200.0.0.0/24`

`# nmap -sS -p80 192.168.10.20`

`# nmap -sU -p53 172.16.1.0/24`

**7) Dica extra:** configurar estação Debian via CLI

`linux# ifconfig eth0 192.168.0.10 netmask 255.255.255.0 up`

(atribuir um endereço e uma máscara para uma interface eth0)

`linux# route add default gw 192.168.0.1`

(adicionar uma rota para a saída padrão)

`linux# echo "nameserver 192.168.1.50" > /etc/resolv.conf`

(modificar o arquivo que armazena o endereço IP do servidor de nomes)

`linux# links www.site.com.br`

(navegar web modo texto, teclar letra q para fechar)

