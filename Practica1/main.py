from GetSNMP import *
import rrdtool
import time
import json

# se encarga de hacer el get y regresar lo que queremos 
def mostrarConsulta(comunidad:str,host:str,str_mib:str)->str:
    traffic=""
    traffic=consultaSNMP(comunidad,host,str_mib)
    print (traffic)
    return traffic

# Crea una base de datos en base al nombre y para un solo dato
def nuevaRDD(nombreRRD:str):
    # creamos la bae de datos
    ret = rrdtool.create(nombreRRD,
                        "--start", # momento que se empieza a almacenar los datos
                        'N',# now (empieza al momento de ejecutar el script) (tambien un numero)
                        "--step", # un step
                        '30',      # cada minuto
    #DS: Octetos de entrada : Tipo contador : cada dos minutos : sin limites minumos : sin limites maximos
                        "DS:octets:COUNTER:30:U:U",
    #RRA: Cada 60 segs de hace un AVERAGE: la mitad de muestras se validan: cada 1 step : numero de filas en la base de datos
                        "RRA:AVERAGE:0.5:1:32") #32 filas,cada uno de 30 segs

    #en caso de haber un error lo sabremos
    if ret:
        print (rrdtool.error())


# se encarga de crear las bases que necesitamos
def creaBases():
    nuevaRDD("multicast.rrd")
    nuevaRDD("ipv4.rrd")
    nuevaRDD("icmp.rrd")
    nuevaRDD("octets.rrd")
    nuevaRDD("ports.rrd")

# realiza las consultas que necesitamos
def listaConsultas(comunidad:str,host:str):
    
    str_mib="1.3.6.1.2.1."
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")

    # print("2) Paquetes multicast que ha recibido una interfaz (ifInNUcastPkts) 1.3.6.1.2.1.2.2.1.12.1 counter")
    valor = "N:" + mostrarConsulta(comunidad, host, "1.3.6.1.2.1.2.2.1.12.1")
    rrdtool.update('multicast.rrd', valor)
    rrdtool.dump('multicast.rrd','multicast.xml')
    # print("2) Paquetes recibidos exitosamente, entregados a protocolos IPv4. (ipInDelivers) 1.3.6.1.2.1.4.9.0 counter")
    valor = "N:" + mostrarConsulta(comunidad, host, "1.3.6.1.2.1.4.9.0")
    rrdtool.update('ipv4.rrd', valor)
    rrdtool.dump('ipv4.rrd','ipv4.xml')
    # print("2) Mensajes de respuesta ICMP que ha enviado el agente (icmpOutEchoReps) 1.3.6.1.2.1.5.22.0 counter")
    valor = "N:" + mostrarConsulta(comunidad, host, "1.3.6.1.2.1.5.22.0")
    rrdtool.update('icmp.rrd', valor)
    rrdtool.dump('icmp.rrd','icmp.xml')
    # print("2) Segmentos enviados, incluyendo los de las conexiones actuales, ",
    #     "pero excluyendo los que contienen solamente octetos retransmitidos (ifOutOctets) 1.3.6.1.2.1.2.2.1.16.1 counter")
    valor = "N:" + mostrarConsulta(comunidad, host, "1.3.6.1.2.1.2.2.1.16.1")
    rrdtool.update('octets.rrd', valor)
    rrdtool.dump('octets.rrd','octets.xml')
    # print("D2) Datagramas recibidos que no pudieron ser entregados por cuestiones ",
    #     "distintas a la falta de aplicación en el puerto destino (udpNoPorts) 1.3.6.1.2.1.7.2.0 counter")
    valor = "N:" + mostrarConsulta(comunidad, host, "1.3.6.1.2.1.7.2.0")
    rrdtool.update('ports.rrd', valor)
    rrdtool.dump('ports.rrd','ports.xml')


def nuevaGrafica(nombre_grafica:str,base_RRD:str):
    # tiempo actual
    tiempo_actual = int(time.time())
    #Grafica desde el tiempo actual menos diez minutos
    tiempo_inicial = tiempo_actual - 690 #16 minutos lo que dura el analisis
    # solo se generara una grafica en base al tradico de red
    ret = rrdtool.graph( nombre_grafica,
                        "--start",str(tiempo_inicial),
                        "--end","N",
                        "--vertical-label=Bytes/s", # maquillaje para la grafica
                        "--title=Tráfico de Red de un agente \n Usando SNMP y RRDtools", # maquillaje para la grafica
                        # se consulta la informacion para graficarlo
                        "DEF:traficoEntrada="+base_RRD+":octets:AVERAGE",
                        # recorre toda la coleccion para convertir los octetos a bites
                        "CDEF:escalaIn=traficoEntrada,8,*",
                        # Para imprimir los datos
                        "LINE3:escalaIn#00FF00:Trafico de entrada")

def creaGraficas():
    nuevaGrafica("multicast.png",'multicast.rrd')
    nuevaGrafica("ipv4.png",'ipv4.rrd')
    nuevaGrafica("icmp.png",'icmp.rrd')
    nuevaGrafica("octets.png",'octets.rrd')
    nuevaGrafica("ports.png",'ports.rrd')


def trafico(comunidad:str, host:str):
    listaConsultas(comunidad, host)
    creaBases()
    inicio=time.time()
    fin= inicio + 960# 16 minutos
    while True:
        listaConsultas()
        inicio=time.time()
        if not inicio < fin:
            break
    creaGraficas()

class Agentes:
    

    def __init__(self):
        self.temp_list=[]
        with open("agentes.json",'r') as temp_file:
            self.temp_list=json.load(temp_file)
        print("Agentes actuales",self.temp_list)

    def agregar(self,host:str):
        self.temp_list.append(host)

    def eliminar(self,host:str):
        pass

    def actualizar(self):
        with open("agentes.json",'w') as temp_file:
            json.dump(self.temp_list,temp_file)
            

if __name__=='__main__':

    comunidad="123"
    agentes=Agentes()
    

    opcion=0

    while True:
        print("Menu:\n1)Alta.\n2.)Baja.\n3)ver trafico y generar reporte.\n4)Salir\n")
        opcion=int(input("Escriba la opcion: "))
        if opcion==1:
            nuevo_host=input("Escriba un host valido: ")
            # agentes.agregar("192.168.1.66")
            agentes.actualizar()
            print("Agregado")
            sleep(3)
        elif opcion==2:
            fuera_host=input("Escriba el host a eliminar: ")
            # agente.eliminar()
            agentes.actualizar()
            print("Eliminado")
            sleep(3)
        elif opcion==3:
            reporte_host=input("escriba el host a examinar: ")
            print("Espere 16 min en lo que se genera el reporte... en un momento comienza..")
            sleep(5)
        elif opcion==4:
            break
        else:
            continue
    

    