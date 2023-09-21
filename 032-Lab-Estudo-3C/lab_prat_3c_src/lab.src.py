####################################################################
# Autor Hermano Pereira
# Versao 29/06/2019
####################################################################

import os
import re
import random
import sys
import datetime
import subprocess
import tkinter as tk
from PIL import Image, ImageTk

####################################################################

version = '2.9'
admin = ''

# Verificar versao
lversion = os.popen('cat /etc/xbnet_version.txt').read().rstrip()
if (lversion != version):
   print ('Script deve ser executado em xbnet '+version+'! (local: xbnet '+lversion+')')
   sys.exit()

# Testar Root
if os.getuid() != 0:
   print('Script deve ser executado como root!')
   print('Tente: sudo py lab.py')
   sys.exit()

# Espaço em /cow
cowmem = 800000
cow = os.popen('df -a | egrep cow | tr -s " " | cut -d " " -f 4').read()
if (int(cow) <= cowmem):
   print ('Espaço em memória insuficiente para executar este laboratório!')
   print ('Mínimo requerido (/cow): '+str(cowmem)+' bytes.')
   sys.exit()

# Expirou?
hoje = datetime.date.today()
#nao_antes = datetime.date(2022,10,23)
#nao_depois = datetime.date(2022,11,8)
#if (hoje < nao_antes):
#   print ('Laboratório ainda não está ativo!')
#   sys.exit()
#elif (hoje > nao_depois):
#   print ('Laboratório expirou!')
#   sys.exit()


# Nome do Admin
try:
  admin = sys.argv[1]
  admin_ok = False
  if (len(admin) >= 3 and len(admin) <= 20):
     if re.match(r"^[A-Za-z]+$",admin):
        admin_ok = True
  if not (admin_ok):
     print ('Para o nome do Admin utilize:')
     print ('Mínimo de 3 e máximo de 20 caracteres')
     print ('Caracteres de "a" a "z"')
     sys.exit()
  #admin = admin.capitalize()
except Exception as e:
  print ('Faltou preencher o nome do Admin!')
  print ('Tente: py lab.py Fulano')
  sys.exit()

# Registro Academico
try:
  racad = sys.argv[2]
  racad_ok = False
  if (len(racad) >= 6 and len(racad) <= 10):
     if re.match(r"^[0-9]+$",racad):
        racad_ok = True
  if not (racad_ok):
     print ('Preencha o número do seu Registro Acadêmico (RA):')
     print ('Mínimo de 6 e máximo de 10 caracteres')
     sys.exit()
except Exception as e:
  print ('Faltou preencher o número do seu Registro Acadêmico (RA):')
  print ('Tente, exemplo: py lab.py Fulano 123456')
  sys.exit()


### Criptografia

idlab = '3C1'
chave = '394545868'

hoje = datetime.date.today() 
comp_texto = idlab+" "+admin+" "+racad+" "+str(hoje)
comprovante = os.popen('echo \"'+comp_texto+'\" | openssl enc -aes-256-cbc -a -nosalt -K '+chave+' -iv 0').read()
comprovante = re.escape(comprovante)

os.system('openssl enc -d -aes-256-cbc -a -nosalt -K '+chave+' -iv 0 -in lab.tar.gz.crypt -out lab.tar.gz > /dev/null')
os.system('tar -xvzf lab.tar.gz > /dev/null')
os.system('rm -f lab.tar.gz > /dev/null') 

# Preparar enderecos

b1 = str(random.randint(193,223))
b2 = str(random.randint(100,254))
b3 = str(random.randint(100,254))

net = b1+'.'+b2+'.'+b3+'.'

prefs = [24,25,26,27,28,29,30]
masks = ['255.255.255.0','255.255.255.128','255.255.255.192','255.255.255.224','255.255.255.240','255.255.255.248','255.255.255.252']
m = random.randint(0,len(prefs)-3)

prefix = prefs[m]
mask   = masks[m]

nh = 2 ** (32-prefix)
nn = 256 / nh
n = random.randint(0,nn-1)
n_id = n * nh
n_ini = n_id 
n_fin = n_id + nh - 1 

n1_id = int(n_id)
n2_id = int(n_id + (nh/2))

r1_e0 = net+str(n1_id + 1)
r1_e1 = net+str(n2_id + 1)
h1_e0 = net+str(n1_id + 2)
h2_e0 = net+str(n2_id + 2)

r1_e0_mask = masks[m+1]
r1_e1_mask = masks[m+1]
h1_e0_mask = masks[m+1]
h2_e0_mask = masks[m+1]

# Preparar MACs

ouis = ('3COM',
        'CISCO',
        'INTEL',
        'HUAWEI',
        'NETGEAR',
        'APPLE',
        'ASUSTEK',
        'JUNIPER',
        'SAMSUNG',
        'DELL',
        'EXTREME',
        'CISCO',
        'INTEL',
        'HUAWEI',
        'NETGEAR',
        'APPLE',
        'ASUSTEK',
        'JUNIPER',
        'SAMSUNG',
        'DELL',
        'EXTREME',
        '3COM')
macs = ('20:fd:f1',
        '6c:5e:3b',
        'dc:71:96',
        'ec:56:23',
        '10:0c:6b',
        'dc:56:e7',
        '60:45:cb',
        '00:24:dc',
        '00:09:18',
        'a8:99:69',
        'b8:50:01',
        '6c:dd:30',
        '24:41:8c',
        '04:8c:9a',
        '3c:37:86',
        '64:5a:ed',
        '10:7b:44',
        '40:b4:f0',
        'e4:7d:bd',
        '18:66:da', 
	'5c:0e:8b',
        '40:01:c6')

rnd = random.randint(0,len(ouis)-1)
oui1 = ouis[rnd]
mac1 = macs[rnd]
rnd = random.randint(0,len(ouis)-1)
oui2 = ouis[rnd]
mac2 = macs[rnd]
rnd = random.randint(0,len(ouis)-1)
oui3 = ouis[rnd]
mac3 = macs[rnd]

fullmacs = []
i = 0;
while (i < 4):
   mw1 = str(random.randint(0,9))
   mw2 = str(random.randint(0,9))
   mw3 = str(random.randint(0,9))
   mw4 = str(random.randint(0,9))
   mw5 = str(random.randint(0,9))
   mw6 = str(random.randint(0,9))
   if (i <= 1):
      fullmacs.append(mac1+':'+mw1+mw2+':'+mw3+mw4+':'+mw5+mw6)
   elif (i == 2):
      fullmacs.append(mac2+':'+mw2+mw3+':'+mw4+mw5+':'+mw6+mw1)
   else:
      fullmacs.append(mac3+':'+mw6+mw1+':'+mw2+mw3+':'+mw4+mw5)
   i = i + 1

### Descarte

ms_drop  = ['0.05','0.10','0.15']
ms_flush = ['0.15','0.10','0.05']
ms_perc  = ['30','50','70']
ms = random.randint(0,len(ms_drop)-1)

mtu_size = ['1500','1000','500']
mtu_segs = ['1000','1700','3400']
mtu = random.randint(0,len(mtu_size)-1)

####################################################################

switch_name = []
switch_prep = []
switch_load = []
switch_rect_x = []
switch_rect_y = []
switch_taps = []

uml_name = []
uml_prep = []
uml_load = []
uml_block = []
uml_inst = []
uml_runrc = []
uml_rect_x = []
uml_rect_y = []
uml_kernel = []
uml_fs = []
uml_mem = []
uml_pkgs = []
uml_eths = []
uml_taps = []
uml_macs = []
uml_ips = []
uml_masks = []
uml_gw = []
uml_domain = []
uml_dns = []
uml_route = []
uml_cmds = []

vbox_name = []
vbox_appl = []
vbox_prep = []
vbox_load = []
vbox_rect_x = []
vbox_rect_y = []
vbox_tap = []
vbox_mac = []
vbox_rdp = []

wshark_name = []
wshark_iface = []
wshark_prep = []
wshark_load = []
wshark_rect_x = []
wshark_rect_y = []

rect_c_switch = []
rect_e_switch = []
rect_c_uml = []
rect_e_uml = []
rect_c_vbox = []
rect_e_vbox = []
rect_c_wshark = []
rect_e_wshark = []

####################################################################

# Switch LNK ########################
switch_name.append('switch-link1')
switch_prep.append(True)
switch_load.append(False)
switch_rect_x.append(700)
switch_rect_y.append(700)
swnic_tap = []
swnic_tap.append('tap0')
swnic_tap.append('tap1')
switch_taps.append(swnic_tap)

# Switch1 ########################
switch_name.append('switch-link2')
switch_prep.append(True)
switch_load.append(False)
switch_rect_x.append(700)
switch_rect_y.append(700)
swnic_tap = []
swnic_tap.append('tap10')
swnic_tap.append('tap11')
switch_taps.append(swnic_tap)

# Router ###########################
uml_name.append('router')
uml_prep.append(True)
uml_load.append(True)
uml_block.append(True)
uml_inst.append(True)
uml_runrc.append(True)
uml_rect_x.append(384)
uml_rect_y.append(220)
uml_kernel.append('linux_v4_nf')
uml_fs.append('jessie_fs') 
uml_mem.append('64')
host_pkgs = []
host_pkgs.append('python3')
uml_pkgs.append(host_pkgs)
host_eths = []
host_taps = []
host_macs = []
host_ips = []
host_masks = []
host_eths.append('eth0') #### eth0
host_taps.append('tap0')
host_macs.append(fullmacs[0])
host_ips.append(r1_e0)
host_masks.append(r1_e0_mask)
host_eths.append('eth1') #### eth1
host_taps.append('tap10')
host_macs.append(fullmacs[1])
host_ips.append(r1_e1)
host_masks.append(r1_e1_mask)
uml_eths.append(host_eths)
uml_taps.append(host_taps)
uml_macs.append(host_macs)
uml_ips.append(host_ips)
uml_masks.append(host_masks)
uml_gw.append('') #### route/dns
uml_domain.append('')
uml_dns.append('')
uml_route.append(True)
host_cmds = []
host_cmds.append('sed -i \'s/_NOMEADMIN_/'+admin+'/\' en/dn/router/bash_fin.pl')
host_cmds.append('sed -i \'s/_MSDROP_/'+ms_drop[ms]+'/\' en/dn/router/bash_fin.pl')
host_cmds.append('sed -i \'s/_MSFLUSH_/'+ms_flush[ms]+'/\' en/dn/router/bash_fin.pl')
host_cmds.append('sed -i \'s/_MSPERC_/'+ms_perc[ms]+'/\' en/dn/router/bash_fin.pl')
host_cmds.append('sed -i \'s/_MTUSIZE_/'+mtu_size[mtu]+'/\' en/dn/router/bash_fin.pl')
host_cmds.append('sed -i \'s/_MTUSEGS_/'+mtu_segs[mtu]+'/\' en/dn/router/bash_fin.pl')
host_cmds.append('sed -i \'s/_LOSS_/'+str(ms+1)+'/\' en/dn/router/bash_fin.pl')
host_cmds.append('sed -i \'s/_SEGS_/'+str(mtu+1)+'/\' en/dn/router/bash_fin.pl')
host_cmds.append('sed -i \'s/_COMPROVANTE_/'+comprovante+'/\' en/dn/router/bash_fin.pl')
uml_cmds.append(host_cmds)

# host1 ###########################
uml_name.append('host1')
uml_prep.append(True)
uml_load.append(True)
uml_block.append(False)
uml_inst.append(True)
uml_runrc.append(True)
uml_rect_x.append(125)
uml_rect_y.append(220)
uml_kernel.append('linux_v4')
uml_fs.append('jessie_fs') 
uml_mem.append('64')
host_pkgs = []
host_pkgs.append('tcpdump')
host_pkgs.append('netcat')
uml_pkgs.append(host_pkgs)
host_eths = []
host_taps = []
host_macs = []
host_ips = []
host_masks = []
host_eths.append('eth0') #### eth0
host_taps.append('tap1')
host_macs.append(fullmacs[2])
host_ips.append(h1_e0)
host_masks.append(h1_e0_mask)
uml_eths.append(host_eths)
uml_taps.append(host_taps)
uml_macs.append(host_macs)
uml_ips.append(host_ips)
uml_masks.append(host_masks)
uml_gw.append(r1_e0) #### route/dns
uml_domain.append('')
uml_dns.append('')
uml_route.append(False)
host_cmds = []
host_cmds.append('sed -i \'s/_MTU_/'+mtu_size[mtu]+'/\' en/dn/host1/bash_fin.pl')
uml_cmds.append(host_cmds)

# host2 ###########################
uml_name.append('host2')
uml_prep.append(True)
uml_load.append(True)
uml_block.append(False)
uml_inst.append(True)
uml_runrc.append(True)
uml_rect_x.append(642)
uml_rect_y.append(220)
uml_kernel.append('linux_v4')
uml_fs.append('jessie_fs') 
uml_mem.append('64')
host_pkgs = []
host_pkgs.append('tcpdump')
host_pkgs.append('netcat')
uml_pkgs.append(host_pkgs)
host_eths = []
host_taps = []
host_macs = []
host_ips = []
host_masks = []
host_eths.append('eth0') #### eth0
host_taps.append('tap11')
host_macs.append(fullmacs[3])
host_ips.append(h2_e0)
host_masks.append(h2_e0_mask)
uml_eths.append(host_eths)
uml_taps.append(host_taps)
uml_macs.append(host_macs)
uml_ips.append(host_ips)
uml_masks.append(host_masks)
uml_gw.append(r1_e1) #### route/dns
uml_domain.append('')
uml_dns.append('')
uml_route.append(False)
host_cmds = []
host_cmds.append('sed -i \'s/_MTU_/'+mtu_size[mtu]+'/\' en/dn/host2/bash_fin.pl')
uml_cmds.append(host_cmds)

#host_cmds.append('sed -i \'s/_NOMEADMIN_/'+admin+'/\' en/dn/estacao/bash_fin.pl')
#host_cmds.append('sed -i \'s/_MACEST_/'+fullmacs[5]+'/\' en/dn/estacao/bash_fin.pl')
#host_cmds.append('sed -i \'s/_IPBD_/'+bd_e0+'/\' en/dn/estacao/bash_fin.pl')
#host_cmds.append('sed -i \'s/_NET_/'+net+'/\' en/dn/estacao/bash_fin.pl')

# WireShark1   ##################
wshark_name.append('wireshark1')
wshark_iface.append('tap1')
wshark_prep.append(True)
wshark_load.append(False)
wshark_rect_x.append(268)
wshark_rect_y.append(190)

# WireShark2   ##################
wshark_name.append('wireshark2')
wshark_iface.append('tap11')
wshark_prep.append(True)
wshark_load.append(False)
wshark_rect_x.append(503)
wshark_rect_y.append(190)



####################################################################

win_title = 'Laboratório - Prática '+idlab

win_wid   = 700
win_hei   = 500
win_bg    = 'white'
win_img   = 'dt/lab.png'
win_rsz   = 12
win_rcd   = 'gray'
win_rce   = 'blue'
win_red   = 'red'
win_ree   = 'green'
win_blk   = 'black'

win = tk.Tk()
win.title(win_title)
win_cnv = tk.Canvas(win, width=win_wid, height=win_hei, bg=win_bg)
win_cnv.pack()

im = Image.open(win_img)
im_tk = ImageTk.PhotoImage(im)

win_cnv.create_image(win_wid/2,win_hei/2,image=im_tk)
win_cnv.create_text(5,15,anchor=tk.W,font=('Helvetica',10),text='Admin: '+admin+' ('+racad+')')

#img = ImageTk.PhotoImage(file='av/webserver/var/www/html/'+provedor+'.png')
#win_cnv.create_image(410,343, anchor=tk.NW, image=img)

## Personalizado para este lab
win_cnv.create_text(310,325,anchor=tk.W,font=('Helvetica',10),text='Olá '+admin+',')
win_cnv.create_text(310,340,anchor=tk.W,font=('Helvetica',10),text='O roteador acima está congestionado e ')
win_cnv.create_text(310,355,anchor=tk.W,font=('Helvetica',10),text='está descartando muitos pacotes.')
win_cnv.create_text(310,370,anchor=tk.W,font=('Helvetica',10),text='Favor realizar uma análise detalhada.')
win_cnv.create_text(310,385,anchor=tk.W,font=('Helvetica',10),text='Bom trabalho! Frank.')


#win_cnv.create_text(325,80,anchor=tk.W,font=('Helvetica',10),text=net+str(n3_id)+'/30')
#win_cnv.create_text(98,232,anchor=tk.W,font=('Helvetica',10),text=net+str(n1_id)+'/'+str(prefs[m+1]))
#win_cnv.create_text(560,232,anchor=tk.W,font=('Helvetica',10),text=net+str(n2_id)+'/'+str(prefs[m+2]))

#############################

####################################################################

def create_tap(ntap):
   os.system('tunctl -t '+ntap+' -u nobody > /dev/null 2> /dev/null')
   os.system('ifconfig '+ntap+' up')

def initial_pkgs_uml(fs):
   tmp_pkgs = []
   os.system('rm -Rf mn/*')
   os.system('mount -o loop fs/'+fs+' mn/')
   os.system('mkdir -p mn/opt/dpkg/')
   i = 0
   while (i < len(uml_pkgs)):
      if (uml_fs[i] == fs):
         j = 0
         host_pkgs = uml_pkgs[i] 
         while (j < len(host_pkgs)):
            k = 0
            fnd = False
            while (k < len(tmp_pkgs)):
               if (host_pkgs[j] == tmp_pkgs[k]):
                  fnd = True
               k = k + 1
            if (not fnd):
               os.system('cp -r /opt/dpkg/'+host_pkgs[j]+' mn/opt/dpkg/')
               os.system('cp en/bashrc mn/root/.bashrc')
               os.system('cp en/rc.local mn/etc/rc.local')
               os.system('cp en/rc.conf.pl mn/opt/')
               os.system('cp en/bash.conf.pl mn/opt/') 
               os.system('cp -r en/dn/* mn/opt/ 2> /dev/null')
               tmp_pkgs.append(host_pkgs[j])
            j = j + 1
      i = i + 1
   os.system('umount mn/')
   os.system('rm -Rf mn/*')
   os.system('rm -Rf en/*')

def initial_uml():
   exit_uml()
   tmp_fs = []
   os.system('rm -Rf en/* 2> /dev/null')
   os.system('mkdir en/dn')
   os.system('cp cf/bashrc en/')
   os.system('cp cf/rc.local en/')
   os.system('cp cf/rc.conf.pl en/')
   os.system('cp cf/bash.conf.pl en/')
   rcconf = open('en/rc.conf.pl','a')
   bashconf = open('en/bash.conf.pl','a')
   i = 0
   while (i < len(uml_name)):
      # ---  por fazer
      os.system('cp -r av/'+uml_name[i]+' en/dn/ 2> /dev/null');
      # ---   / por fazer
      host_eths = uml_eths[i]
      host_macs = uml_macs[i]
      host_ips = uml_ips[i]
      host_masks = uml_masks[i]
      host_pkgs = uml_pkgs[i]
      rcconf.write('### Configuracao do '+uml_name[i]+':\n')
      bashconf.write('### Configuracao do '+uml_name[i]+':\n')
      rcconf.write('my $mac = &catch_mac("eth0");\n')
      bashconf.write('my $hostname = &catch_hostname();\n')
      rcconf.write('if ($mac eq "'+host_macs[0]+'") {\n')
      bashconf.write('if ($hostname eq "'+uml_name[i]+'") {\n')
      if(uml_runrc[i]):
         rcconf.write('   system("/usr/bin/perl /opt/'+uml_name[i]+'/rc_ini.pl 2> /dev/null");\n')
         rcconf.write('   &change_hostname("'+uml_name[i]+'");\n')
         j = 0
         while (j < len(host_ips)):
            rcconf.write('   &network_conf("'+host_eths[j]+'","'+host_ips[j]+'","'+host_masks[j]+'");\n')
            j = j + 1 
         rcconf.write('   &gateway_conf("'+uml_gw[i]+'");\n') 
         rcconf.write('   &nameserver_conf("'+uml_dns[i]+'","'+uml_domain[i]+'");\n') 
         if (uml_route[i]):
            rcconf.write('   &route_enable;\n')
         rcconf.write('   system("/usr/bin/perl /opt/'+uml_name[i]+'/rc_fin.pl 2> /dev/null");\n')
      bashconf.write('   system("/usr/bin/perl /opt/'+uml_name[i]+'/bash_ini.pl 2> /dev/null");\n')
      if (uml_inst[i]):
         j = 0
         while (j < len(host_pkgs)):
            bashconf.write('   &install_pkg("'+host_pkgs[j]+'");\n') 
            j = j + 1 
      bashconf.write('   system("/usr/bin/perl /opt/'+uml_name[i]+'/bash_fin.pl 2> /dev/null");\n')
      rcconf.write('}\n')
      bashconf.write('}\n')
      rcconf.write('#-x-x-x-x-x\n\n')
      bashconf.write('#-x-x-x-x-x\n\n')
      # Comandos (NEW) #########
      host_cmds = uml_cmds[i]
      j = 0
      while (j < len(host_cmds)):
         os.system(host_cmds[j])
         j = j + 1
      ########################## 
      i = i + 1
   rcconf.close() 
   bashconf.close() 
   i = 0
   while (i < len(uml_fs)):
      j = 0
      fnd = False
      while (j < len(tmp_fs) and not fnd):
         if (uml_fs[i] == tmp_fs[j]):
            fnd = True
         j = j + 1
      if (not fnd):
         os.system('cp /opt/filesystem/'+uml_fs[i]+' fs/')
         tmp_fs.append(uml_fs[i])
         initial_pkgs_uml(uml_fs[i])
      i = i + 1

def kill_switch(i):
   os.system('kill $(ps aux | grep \'fdb.show '+switch_name[i]+'\' | awk \'{print $2}\')')
   
def delete_switch(i):
   # nao deletar taps
   os.system('ovs-vsctl del-br '+switch_name[i]+' 2> /dev/null ')

def kill_uml(i):
   os.system('kill $(ps aux | grep \'ubd0=fs/'+uml_name[i]+',fs/'+uml_fs[i]+' \' | awk \'{print $2}\')')
  
def kill_vbox(i):
   os.system('vboxmanage controlvm '+vbox_name[i]+' poweroff 2> /dev/null')

def delete_vbox(i):
   os.system('vboxmanage unregistervm '+vbox_name[i]+' --delete 2> /dev/null')

def kill_wshark(i):
   os.system('kill $(ps aux | grep \'.o wsharkname:'+wshark_name[i]+'\' | awk \'{print $2}\')')

def exit_switch():
   i = 0
   while (i < len(switch_name)):
      kill_switch(i)
      delete_switch(i)
      i = i + 1 

def exit_uml():
   os.system('killall linux_v4 2> /dev/null')
   os.system('killall linux_v4_nf 2> /dev/null')
   os.system('killall linux_v6 2> /dev/null')
   os.system('killall linux_v6_nf 2> /dev/null')
   os.system('rm -Rf fs/*')
   os.system('rm -Rf en/*')

def exit_vbox():
   i = 0
   while (i < len(vbox_name)):
      kill_vbox(i)
      delete_vbox(i)
      i = i + 1 

def exit_wshark():
   i = 0
   while (i < len(wshark_name)):
      kill_wshark(i)
      i = i + 1 

def prep_switch(i):
   win_cnv.itemconfig(rect_c_switch[i],fill=win_rcd)
   win_cnv.itemconfig(rect_e_switch[i],fill=win_red)
   win_cnv.update_idletasks()
   kill_switch(i)
   delete_switch(i)
   os.system('ovs-vsctl add-br '+switch_name[i]+' ')
   swnic_tap = switch_taps[i]
   j = 0
   while (j < len(swnic_tap)):
      create_tap(swnic_tap[j])
      os.system('ovs-vsctl add-port '+switch_name[i]+' '+swnic_tap[j]+' ')
      j = j + 1
   os.system('sleep 1')
   win_cnv.itemconfig(rect_c_switch[i],fill=win_rce)
   win_cnv.itemconfig(rect_e_switch[i],fill=win_ree)

def prep_uml(i):
   win_cnv.itemconfig(rect_c_uml[i],fill=win_rcd)
   win_cnv.itemconfig(rect_e_uml[i],fill=win_red)
   win_cnv.update_idletasks()
   kill_uml(i)
   os.system('rm fs/'+uml_name[i]+' 2> /dev/null')
   os.system('sleep 1')
   win_cnv.itemconfig(rect_c_uml[i],fill=win_rce)
   win_cnv.itemconfig(rect_e_uml[i],fill=win_ree)
   if (uml_block[i]):
      win_cnv.itemconfig(rect_c_uml[i],fill=win_blk)


def prep_vbox(i):
   win_cnv.itemconfig(rect_c_vbox[i],fill=win_rcd)
   win_cnv.itemconfig(rect_e_vbox[i],fill=win_red)
   win_cnv.update_idletasks()
   kill_vbox(i)
   delete_vbox(i)
   os.system('vboxmanage import /opt/vbox/'+vbox_appl[i]+'.ova > /dev/null 2> /dev/null')
   os.system('vboxmanage modifyvm '+vbox_appl[i]+' --name '+vbox_name[i]+' 2> /dev/null')
   win_cnv.itemconfig(rect_c_vbox[i],fill=win_rce)
   win_cnv.itemconfig(rect_e_vbox[i],fill=win_ree)

def prep_wshark(i):
   win_cnv.itemconfig(rect_c_wshark[i],fill=win_rcd)
   win_cnv.itemconfig(rect_e_wshark[i],fill=win_red)
   win_cnv.update_idletasks()
   kill_wshark(i)
   os.system('sleep 1')
   win_cnv.itemconfig(rect_c_wshark[i],fill=win_rce)
   win_cnv.itemconfig(rect_e_wshark[i],fill=win_ree)

def run_switch(i):
   if (win_cnv.itemcget(rect_e_switch[i],'fill') == win_ree):
      kill_switch(i)
      exec_switch = 'ovs-appctl fdb/show '+switch_name[i]+' '
      os.system('xfce4-terminal --disable-server -T '+switch_name[i]+' -x watch -n 1 "'+exec_switch+'" 2> /dev/null &')

def run_uml(i):
   if (win_cnv.itemcget(rect_e_uml[i],'fill') == win_ree):
      kill_uml(i)
      exec_uml = '/opt/kernel/'+uml_kernel[i]+' ubd0=fs/'+uml_name[i]+',fs/'+uml_fs[i]+' mem='+uml_mem[i]+'M '
      host_eths = uml_eths[i]
      host_taps = uml_taps[i]
      host_macs = uml_macs[i]
      j = 0
      exec_iface = ''
      while (j < len(host_eths)):
         # create_tap(host_taps[j]) # analisar
         exec_iface = host_eths[j]+'=tuntap,'+host_taps[j]+','+host_macs[j]+', '
         exec_uml = exec_uml + exec_iface
         j = j + 1
      os.system('xfce4-terminal --disable-server -T '+uml_name[i]+' -x '+exec_uml+' 2> /dev/null &')
      if (uml_block[i]): 
         win_cnv.itemconfig(rect_e_uml[i],fill=win_blk)


def run_vbox(i):
   if (win_cnv.itemcget(rect_e_vbox[i],'fill') == win_ree):
      kill_vbox(i)
      os.system('vboxmanage modifyvm '+vbox_name[i]+' --vrdeaddress 127.0.0.1 --vrde on --vrdeport '+vbox_rdp[i]+' 2> /dev/null')
      # create_tap(vbox_tap[i]) # analisar
      os.system('vboxmanage modifyvm '+vbox_name[i]+' --bridgeadapter1 '+vbox_tap[i]+' 2> /dev/null')
      macaddress = vbox_mac[i].replace(':','')
      os.system('vboxmanage modifyvm '+vbox_name[i]+' --macaddress1 "'+macaddress+'" 2> /dev/null')
      os.system('vboxmanage startvm '+vbox_name[i]+' --type headless > /dev/null 2> /dev/null')
      os.system('rdesktop -T '+vbox_name[i]+' 127.0.0.1:'+vbox_rdp[i]+' 2> /dev/null &')

def run_wshark(i):
   if (win_cnv.itemcget(rect_e_wshark[i],'fill') == win_ree):
      kill_wshark(i)
      os.system('wireshark -i '+wshark_iface[i]+' -n -k -o wsharkname:'+wshark_name[i]+' &')

def draw_rect (rect_c,rect_e,x,y):
   wd = 2
   y2 = y + win_rsz + wd * 2
   rect_c.append(win_cnv.create_rectangle(x,y,x+win_rsz,y+win_rsz,fill=win_rcd,width=wd))
   rect_e.append(win_cnv.create_rectangle(x,y2,x+win_rsz,y2+win_rsz,fill=win_red,width=wd))

def draw_rect_all():
   i = 0
   while (i < len(switch_rect_x)):
      draw_rect(rect_c_switch,rect_e_switch,switch_rect_x[i],switch_rect_y[i])
      i = i + 1
   i = 0
   while (i < len(uml_rect_x)):
      draw_rect(rect_c_uml,rect_e_uml,uml_rect_x[i],uml_rect_y[i])
      i = i + 1
   i = 0
   while (i < len(vbox_rect_x)):
      draw_rect(rect_c_vbox,rect_e_vbox,vbox_rect_x[i],vbox_rect_y[i])
      i = i + 1
   i = 0
   while (i < len(wshark_rect_x)):
      draw_rect(rect_c_wshark,rect_e_wshark,wshark_rect_x[i],wshark_rect_y[i])
      i = i + 1

def usr_clic(event):
   x = event.x
   y = event.y
   i = 0
   fnd = False
   while (i < len(switch_name) and not fnd):
      [xmin,ymin,xmax,ymax] = win_cnv.coords(rect_c_switch[i])
      if (xmin <= x <= xmax and ymin <= y <= ymax):
         prep_switch(i)
         fnd = True
      [xmin,ymin,xmax,ymax] = win_cnv.coords(rect_e_switch[i])
      if (xmin <= x <= xmax and ymin <= y <= ymax):
         run_switch(i)
         fnd = True
      i = i + 1
   i = 0
   fnd = False
   while (i < len(uml_name) and not fnd):
      [xmin,ymin,xmax,ymax] = win_cnv.coords(rect_c_uml[i])
      if (xmin <= x <= xmax and ymin <= y <= ymax):
         if not (uml_block[i]):
            prep_uml(i)
         fnd = True
      [xmin,ymin,xmax,ymax] = win_cnv.coords(rect_e_uml[i])
      if (xmin <= x <= xmax and ymin <= y <= ymax):
         if not (uml_block[i]):
            run_uml(i)
         fnd = True
      i = i + 1
   i = 0
   while (i < len(vbox_name) and not fnd):
      [xmin,ymin,xmax,ymax] = win_cnv.coords(rect_c_vbox[i])
      if (xmin <= x <= xmax and ymin <= y <= ymax):
         prep_vbox(i)
         fnd = True
      [xmin,ymin,xmax,ymax] = win_cnv.coords(rect_e_vbox[i])
      if (xmin <= x <= xmax and ymin <= y <= ymax):
         run_vbox(i)
         fnd = True
      i = i + 1
   i = 0
   while (i < len(wshark_name) and not fnd):
      [xmin,ymin,xmax,ymax] = win_cnv.coords(rect_c_wshark[i])
      if (xmin <= x <= xmax and ymin <= y <= ymax):
         prep_wshark(i)
         fnd = True
      [xmin,ymin,xmax,ymax] = win_cnv.coords(rect_e_wshark[i])
      if (xmin <= x <= xmax and ymin <= y <= ymax):
         run_wshark(i)
         fnd = True
      i = i + 1

def usr_clic_xy(event):
   x = event.x
   y = event.y
   print('x '+str(x)+' y '+str(y))

def init_preps():
   i = 0 
   while (i < len(switch_name)):
      if (switch_prep[i]):
         prep_switch(i)      
      i = i + 1
   i = 0 
   while (i < len(uml_name)):
      if (uml_prep[i]):
         prep_uml(i)      
      i = i + 1
   i = 0 
   while (i < len(vbox_name)):
      if (vbox_prep[i]):
         prep_vbox(i)      
      i = i + 1
   i = 0 
   while (i < len(wshark_name)):
      if (wshark_prep[i]):
         prep_wshark(i)      
      i = i + 1

def init_loads():
   i = 0 
   while (i < len(switch_name)):
      if (switch_load[i]):
         run_switch(i)      
      i = i + 1
   i = 0 
   while (i < len(uml_name)):
      if (uml_load[i]):
         run_uml(i)      
      i = i + 1
   i = 0 
   while (i < len(vbox_name)):
      if (vbox_load[i]):
         run_vbox(i)      
      i = i + 1
   i = 0 
   while (i < len(wshark_name)):
      if (wshark_load[i]):
         run_wshark(i)      
      i = i + 1

####################################################################

initial_uml()
draw_rect_all()
init_preps()
init_loads()

os.system('rm -Rf av/ > /dev/null')
os.system('rm -Rf dt/ > /dev/null')
os.system('rm -Rf cf/ > /dev/null') 

win_cnv.bind('<Double-1>',usr_clic)
win_cnv.bind('<Double-3>',usr_clic_xy)
win.mainloop()

exit_wshark()
exit_uml()
exit_vbox()
exit_switch()

os.system('rm -Rf en/ > /dev/null')
os.system('rm -Rf fs/ > /dev/null')
os.system('rm -Rf mn/ > /dev/null') 

####################################################################


