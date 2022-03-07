# Practica 1: Adquisicion de informacion usando SNMP

### Objetivos

- Implementar la arquitectura basica del protocolo SNMP.
- Implementar la comunicacion (instercambiar mensajes) entre agentes y gestor usando SNMP.
- Implementar la persistencia de una manera eficiente.
- Generar reportes  para controlar y vigilar los agentes.
- Implementar un modelo de red.



### Agregar Dispositivo
### Eliminar dispositivo
### Reposte de informacion de dispositivo


#### Asignacion de bloque

El scrip que calcula los dias vividos  hasta el 23 de febrero de 2022
Mi fecha de nacimiento: 23 de enero de 1998 

Dias transcurridos 8797

Bloque que debo de realizar: 2

# Ejercicios

Mib-2: 1.3.6.1.2.1.[^2].


- 1.Paquetes unicast que ha recibido una interfaz (ifInUcastPkts) 1.3.6.1.2.1.2.2.1.11.1 counter.
- 2.Paquetes multicast que ha recibido una interfaz (ifInNUcastPkts) 1.3.6.1.2.1.2.2.1.12.1 counter.
- 3.Paquetes multicast que ha enviado una interfaz (ifOutNUcastPkts) 1.3.6.1.2.1.2.2.1.18.1 counter[^2].

- 1.Paquetes recibidos a protocolos IPv4, incluyendo los que tienen errores. (ipInReceives) 1.3.6.1.2.1.4.3.0 counter.
- 2.Paquetes recibidos exitosamente, entregados a protocolos IPv4. (ipInDelivers) 1.3.6.1.2.1.4.9.0 counter.
- 3.Paquetes Ipv4 que los protocolos locales de usuarios de IPv4 suministraron a IPv4 en las solicitudes de transmisión. (ipOutRequests)        1.3.6.1.2.1.4.10.0 counter[^2].
    

- 1.Mensajes ICMP echo que ha enviado el agente (icmpOutEchos) 1.3.6.1.2.1.5.21.0 counter.
- 2.Mensajes de respuesta ICMP que ha enviado el agente (icmpOutEchoReps) 1.3.6.1.2.1.5.22.0 counter.
- 3.Mensajes ICMP que ha recibido el agente. (icmpInEchos) 1.3.6.1.2.1.5.8.0 counter[^2].

- 1.Segmentos recibidos, incluyendo los que se han recibido con errores. (ifInOctets) 1.3.6.1.2.1.2.2.1.10.1 counter.
- 2.Segmentos enviados, incluyendo los de las conexiones actuales, pero excluyendo los que contienen solamente octetos retransmitidos            (ifOutOctets) 1.3.6.1.2.1.2.2.1.16.1 counter.
- 3.Segmentos retransmitidos; es decir, el número de segmentos TCP transmitidos que contienen uno o más octetos transmitidos  previamente[^2].
    


- 1.Datagramas entregados a usuarios UDP (udpInDatagrams) 1.3.6.1.2.1.7.1.0 counter.
- 2.Datagramas recibidos que no pudieron ser entregados por cuestiones distintas a la falta de aplicación en el puerto destino (udpNoPorts) 1.3.6.1.2.1.7.2.0 counter.
- 3.Datagramas enviados por el dispositivo. (udpOutDatagrams) 1.3.6.1.2.1.7.4.0 counter[^2].





## Se debera de crear un documento PDF mostrando las 5 graficas y mostrar la sig informacion

- Nombre del sistema 1.3.6.1.2.1.1.1.0
- Version y logo del sistema operativo (lo ponemos nosotros)
- Ubicacion geografica 
- Numero de interfaces de red 1.3.6.1.2.1.2.1.0
- Tiempo de actividad desde el ultimo reinicio 1.3.6.1.2.1.1.3.0
- comunidad 
- IP