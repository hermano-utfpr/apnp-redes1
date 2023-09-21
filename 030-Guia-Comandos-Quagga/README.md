# Guia de Comandos Roteadores Quagga - LiveLinux xbnet 2.9

**Configuração Básica**

Use o comando show:

`zebra# show ?`

Verificar interfaces:

`zebra# show interface`

Verificar tabela de roteamento:

`zebra# show ip route`

Acessar modo de configuração:

`zebra# configure terminal`

`zebra(config)#`

Configurar uma interface:

`zebra(config)# interface eth0`

`zebra(config-if)# ip address 192.168.0.10/24`

`zebra(config-if)# no shutdown`

`zebra(config-if)# exit`

Modificar a variável de largura de banda de uma interface:

`zebra(config)# interface eth0`

`zebra(config-if)# bandwidth 10000`

`zebra(config-if)# exit`

(largura de banda em kbits/s, neste exemplo 10Mbps)

Configurar uma rota estática:

`zebra(config)# ip route 192.168.10.0/24 192.168.0.1`

Sair:

`zebra(config)# end`

`zebra# exit`

`Configuração do protocolo RIP`

Use o comando show:

`ripd# show ?`

Verificar rotas aprendidas com o RIP:

`ripd# show ip rip`

Verificar configuração e status do RIP:

`ripd# show ip rip status`

Acessar modo de configuração:

`ripd# configure terminal`

`ripd(config)#`

Divulgar uma rede:

`ripd(config)# router rip`

`ripd(config-router)# network 10.0.0.0/8`

`ripd(config-if)# exit`

Sair:

`ripd(config)# end`

`ripd# exit`

**Configuração do protocolo OSPF**

Use o comando show:

`ospfd# show ?`

Verificar rotas aprendidas com o OSPF:

`ospfd# show ip ospf route`

Verificar configuração e status do OSPF:

`ospfd# show ip ospf ?`

-> opções (interface|neighbor|database)

Acessar modo de configuração:

`ospfd# configure terminal`

`ospfd(config)#`

Divulgar uma rede:

`ospfd(config)# router ospf`

`ospfd(config-router)# network 10.0.0.0/8 area 0`

`ospfd(config-if)# exit`

Verificar e modificar os custos das interfaces:

`ospfd# show ip ospf interface eth0`

`ospfd# configure terminal`

`ospfd(config)# interface eth0`

`ospfd(config-if)# ospf cost 30`

`ospfd(config-if)# end`

Sair:

`ospfd(config)# end`

`ospfd# exit`

