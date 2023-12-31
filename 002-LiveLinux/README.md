# 002 - LiveLinux - xbnet 2.9

Xubuntu Network LiveLinux (xbnet) é uma distribuição Linux preparada para as aulas de Redes de Computadores do curso de Tecnologia em Sistemas para Internet (TSI) da UTFPR Câmpus Guarapuava. Trata-se de uma modificação do Xubuntu 16.04. 

É possível executar essa distribuição a partir de DVD ou Pendrive e trabalhar com diversos laboratórios de Redes através da virtualização de estações, servidores, switches e roteadores. 

Hardware recomendado: mínimo de 2 núcleos e 4GB de memória RAM. 

**Download da Imagem:**

a) Link 1 [xbnet-2.9](https://nuvem.utfpr.edu.br/index.php/s/Up1aZm0RFPpmKWr); 

b) Link 2 [xbnet-2.9](https://drive.google.com/file/d/1V4tdBn8-RQPDYvhrDSvxvGHQ6tXQ7irw/view?usp=sharing).

**Utilizar o LiveLinux como Máquina Virtual:**

Tanto VirtualBox como VMWare são boas opções para criar uma máquina virtual para rodar o LiveLinux:

Sugestão:
- Máquina Linux (Ubuntu) 64 bits
- Mínimo de 4GB de vRAM
- Mínimo de 2 vCPUs
- Não precisa de vHD
- Colocar o arquivo ISO como Boot em Drive Óptico
Faça diversos testes, procure otimizar o melhor possível de acordo com o seu hardware. 

*No Ubuntu, uma boa opção é o Virt-Manager: `sudo apt-get install virt-manager`.
Carregar Virt-Manager -> File -> New Virtual Machine -> Local install media -> (Forward) -> Choose ISO: procurar arquivo extensão .iso -> Browse Local -> Selecionar -> Choose the Operating System: Generic or Unknown OS -> Forward -> Preencher CPU e RAM -> Forward -> Não habilitar Storage -> Forward -> Nomear VM -> Finish.*

**Gerar um Pendrive/DVD com LiveLinux:**

Utilize as ferramentas para gerar um novo LiveDVD ou novo LivePendrive:

Sugestão: utilize dd, ou [Rufus](https://rufus.ie/pt_BR/). 

[Ventoy](https://www.ventoy.net/en/index.html) também é uma opção interessante, permite várias ISOs no mesmo pendrive.

*Cuidado!*
Exemplo, gerar um Pendrive via Linux:
`:~$ dd if=xbnet2.9.iso of=/dev/sdX`
-> Importante: certifique-se de que "/dev/sdX" é o dispositivo pendrive para não perder dados em seu computador (use o comando `fdisk -l`).
*Cuidado!* 

Reinicie o seu computador e selecione a opção de Boot Primário para inicializar o sistema operacional a partir do seu DVD ou Pendrive (USB). 

**Execute um laboratório de exemplo no LiveLinux:**

`estudante@estudante$ cd lab_tutorial`

`estudante@estudante/lab_tutorial$ sudo py lab.py SeuNome`

Nesse laboratório serão necessários 2GB de RAM para carregar os dispositivos "router" e "server". Para carregar também os "desktops" é necessário que o seu computador tenha 4GB de RAM. 

**Iniciar o LiveLinux com o melhor desempenho possível:**

Recomendado para >= 6GB de RAM.

Pressione a tecla TAB no momento de carregamento do GRUB.

Adicione o comando "toram" conforme abaixo:

`> /casper/vmlinuz file=/cdrom/preseed/custom.seed boot=casper initrd=/casper/initrd.gz quiet splash toram --`

Este comando irá copiar todo o LiveLinux para a memória RAM. 

