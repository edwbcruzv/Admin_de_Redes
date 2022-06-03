

### Traps

- alertas que envia el agente y el gestor las recibe

el archivo `/usr/share/snmp/mibs/TRAP-TEST-MIB.txt`

```txt
TRAP-TEST-MIB DEFINITIONS ::= BEGIN
        IMPORTS ucdExperimental FROM UCD-SNMP-MIB;

demotraps OBJECT IDENTIFIER ::= {ucdExperimental 990}

demotrap TRAP-TYPE
        ENTERPRISE demotraps
        VARIABLES {sysLocation}
        DESCRIPTION "an example of an smiv1 trap"
        ::= 17

END

```

>sudo apt-get install snmp snmpd

>sudo apt-get install snmp-mibs-downloader

>sudo apt-get update

>sudo apt-get install snmptrapd


configurar archivo y agregar la comunidad:123
>sudo nano /etc/snmp/snmptrapd.conf


para ejecutar el demonio
>sudo snmptrapd -f -Lo -c '/etc/snmp/snmptrapd.conf'



### Generar alertas 
sintaxis de snmp version 1
>snmptrap -v [version] -c [comunidad] [target host] [enterpriseOID] [agent-addr] [generic-trap] [specific-trap] [timestamp] [list-var-binds]



>snmptrap -v 1 -c 123 localhost '1.2.3.4.5' "" 1 0 "" 1.3.6.1.2.1.1.1.0 s "testing"



>snmptrap -v 1 -c 123 localhost TRAP-TEST-MIB::demotraps "" 2 0 "" IF-MIB::ifIndex i 1



### Configuracion de un handler

agregarle nuevas instrucciones a '/etc/snmp/snmptrapd.conf'

```
authCommunity log,execute,net 123
traphandle .1.3.6.1.6.3.1.1.5.3 python3 /usr/bin/notificacion.py
traphandle .1.3.6.1.6.3.1.1.5.4 python3 /usr/bin/notificacion2.py
#traphandle .1.3.6.1.6.3.1.1.5.2 /home/cruz/echotrap.sh
#traphandle .1.3.6.1.6.3.1.1.5.3 /home/cruz/echotrap.sh
#traphandle TRAP-TEST-MIB::demotrap /home/cruz/echotrap.sh

```


instalar
>sudo apt-get install libnet-ssleay-perl libio-socket-ssl-perl libcrypt-ssleay-perl


probamos
>snmptrap -v 1 -c 123 localhost TRAP-TEST-MIB::demotraps "" 2 0 "" IF-MIB::ifIndex i 1


### Configuracion del enrutador

una vez asignada la ip...

ver documentacion
>snpm-server community {comunidad} ro

>snmp enable traps

>snmp-server host {ip del gestor} traps version 2c {comunidad}

para mostrar la configuracion
>show running-config


### configuracion para tap0

sudo route add -net {la mascara de subred} netmask 255.255.255.0 gw {ip destino} dev tap0