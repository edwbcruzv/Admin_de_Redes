from Libreria.GetSNMP import *
from Libreria.CreateRRD import *


def mostrarConsulta(comunidad:str,host:str,str_mib:str)->None:
    traffic=""
    traffic=consultaSNMP('123','localhost','1.3.6.1.2.1.2.2.1.10.2')
    print (traffic)

def nuevaRDD():
    pass



def listaConsultas():
    comunidad="123"
    host="localhost"
    str_mib="1.3.6.1.2.1."
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
    # 1) Paquetes unicast que ha recibido una interfaz (ifInUcastPkts) 1.3.6.1.2.1.2.2.1.11 counter
    print("Paquetes unicast que ha recibido una interfaz (")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.2.2.1.11")
    # 2) Paquetes multicast que ha recibido una interfaz (ifInNUcastPkts) 1.3.6.1.2.1.2.2.1.12 counter
    print("Paquetes multicast que ha recibido una interfaz")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.2.2.1.12")
    # 3) Paquetes multicast que ha enviado una interfaz (ifOutNUcastPkts) 1.3.6.1.2.1.2.2.1.18 counter
    print("Paquetes multicast que ha enviado una interfaz")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.2.2.1.18")

    # 1) Paquetes recibidos a protocolos IPv4, incluyendo los que tienen errores. (ipInReceives) 1.3.6.1.2.1.4.3.0 counter
    print("Paquetes recibidos a protocolos IPv4, incluyendo los que tienen errores")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.4.3.0")
    # 2) Paquetes recibidos exitosamente, entregados a protocolos IPv4. (ipInDelivers) 1.3.6.1.2.1.4.9.0 counter
    print("Paquetes recibidos exitosamente, entregados a protocolos IPv4")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.4.9.0")
    # 3) Paquetes Ipv4 que los protocolos locales de usuarios de IPv4 suministraron a IPv4 en las solicitudes de transmisión. (ipOutRequests) 1.3.6.1.2.1.4.10.0 counter
    print("Paquetes Ipv4 que los protocolos locales de usuarios de IPv4 suministraron a IPv4 en las solicitudes de transmisión.")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.4.10.0")

    # 1) Mensajes ICMP echo que ha enviado el agente (icmpOutEchos) 1.3.6.1.2.1.5.21.0 counter
    print("Mensajes ICMP echo que ha enviado el agente ")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.5.21.0")
    # 2) Mensajes de respuesta ICMP que ha enviado el agente (icmpOutEchoReps) 1.3.6.1.2.1.5.22.0 counter
    print("Mensajes de respuesta ICMP que ha enviado el agente")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.5.22.0")
    # 3) Mensajes ICMP que ha recibido el agente. (icmpInEchos) 1.3.6.1.2.1.5.8.0 counter
    print("Mensajes ICMP que ha recibido el agente")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.5.8.0")

    # 1) Segmentos recibidos, incluyendo los que se han recibido con errores. (ifInOctets) 1.3.6.1.2.1.2.2.1.10 counter
    print("Segmentos recibidos, incluyendo los que se han recibido con errores")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.2.2.1.10")
    # 2) Segmentos enviados, incluyendo los de las conexiones actuales, pero excluyendo los que contienen solamente octetos retransmitidos (ifOutOctets) 1.3.6.1.2.1.2.2.1.16 counter
    print("Segmentos enviados, incluyendo los de las conexiones actuales, pero excluyendo los que contienen solamente octetos retransmitidos")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.2.2.1.16")
    # 3) Segmentos retransmitidos; es decir, el número de segmentos TCP transmitidos que contienen uno o más octetos transmitidos previamente 
    print("Segmentos retransmitidos; es decir, el número de segmentos TCP transmitidos que contienen uno o más octetos transmitidos previamente")
    #mostrarConsulta(comunidad, host, str_mib)

    # 1) Datagramas entregados a usuarios UDP (udpInDatagrams) 1.3.6.1.2.1.7.1.0 counter
    print("Datagramas entregados a usuarios UDP")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.7.1.0")
    # 2) Datagramas recibidos que no pudieron ser entregados por cuestiones distintas a la falta de aplicación en el puerto destino (udpNoPorts) 1.3.6.1.2.1.7.2.0 counter
    print("Datagramas recibidos que no pudieron ser entregados por cuestiones distintas a la falta de aplicación en el puerto destino")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.7.2.0")
    # 3) Datagramas enviados por el dispositivo. (udpOutDatagrams) 1.3.6.1.2.1.7.4.0 counter
    print("Datagramas enviados por el dispositivo")
    mostrarConsulta(comunidad, host, "1.3.6.1.2.1.7.4.0")
 
while True:
    listaConsultas()