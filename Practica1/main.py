# from GetSNMP import *
from pysnmp.hlapi import *
import rrdtool
import time
import json
import os





# se encarga de crear las bases que necesitamos



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


class Agente:

    def __init__(self,comunidad:str,host:str):
        self.Comunidad=comunidad
        self.Host=host
        self.Nombre_sistema=None
        # Version y logo del sistema operativo (lo ponemos nosotros)
        # Ubicacion geografica 
        self.Num_interfaces=None
        self.Tiempo_Activo=None
        self.Lista_Consultas=[0,0,0,0,0]
        # Creando carpeta para almacenar las bases de datos generadas
        try:
            os.mkdir(self.Host)
        except:
            pass
        self.creaBases()

    def status(self):
        self.Nombre_sistema=self.consultaSNMP("1.3.6.1.2.1.1.1.0")
        # Version y logo del sistema operativo (lo ponemos nosotros)
        # Ubicacion geografica 
        self.Num_interfaces=self.consultaSNMP("1.3.6.1.2.1.2.1.0") 
        self.Tiempo_Activo=self.consultaSNMP("1.3.6.1.2.1.1.3.0")  
        print("|==============================|\nComunidad:",self.Comunidad)
        print("Host:",self.Host)
        print("Nombre del sistema:",self.Nombre_sistema)
        print("Numero de interfaces de red:",self.Num_interfaces)
        print("Tiempo desde el ultimo reinicio:",self.Tiempo_Activo,"")
        print(self.updateListaConsultas())

    def creaBases(self):
        self.nuevaRDD("multicast.rrd")
        self.nuevaRDD("ipv4.rrd")
        self.nuevaRDD("icmp.rrd")
        self.nuevaRDD("octets.rrd")
        self.nuevaRDD("ports.rrd")

    def updateListaConsultas(self)->list:
        #str_mib="1.3.6.1.2.1."
        
        # print("2) Paquetes multicast que ha recibido una interfaz (ifInNUcastPkts) 1.3.6.1.2.1.2.2.1.12.1 counter")
        self.Lista_Consultas[0] = self.consultaSNMP("1.3.6.1.2.1.2.2.1.12.1")
        rrdtool.update(self.Host+'/multicast.rrd', "N:" + self.Lista_Consultas[0])
        rrdtool.dump(self.Host+'/multicast.rrd','multicast.xml')

        # print("2) Paquetes recibidos exitosamente, entregados a protocolos IPv4. (ipInDelivers) 1.3.6.1.2.1.4.9.0 counter")
        self.Lista_Consultas[1] = self.consultaSNMP("1.3.6.1.2.1.4.9.0")
        rrdtool.update(self.Host+'/ipv4.rrd', "N:" + self.Lista_Consultas[1])
        rrdtool.dump(self.Host+'/ipv4.rrd','ipv4.xml')

        # print("2) Mensajes de respuesta ICMP que ha enviado el agente (icmpOutEchoReps) 1.3.6.1.2.1.5.22.0 counter")
        self.Lista_Consultas[2] = self.consultaSNMP("1.3.6.1.2.1.5.22.0")
        rrdtool.update(self.Host+'/icmp.rrd', "N:" + self.Lista_Consultas[2])
        rrdtool.dump(self.Host+'/icmp.rrd','icmp.xml')

        # print("2) Segmentos enviados, incluyendo los de las conexiones actuales, ",
        #     "pero excluyendo los que contienen solamente octetos retransmitidos (ifOutOctets) 1.3.6.1.2.1.2.2.1.16.1 counter")
        self.Lista_Consultas[3] = self.consultaSNMP("1.3.6.1.2.1.2.2.1.16.1")
        rrdtool.update(self.Host+'/octets.rrd', "N:" + self.Lista_Consultas[3])
        rrdtool.dump(self.Host+'/octets.rrd','octets.xml')

        # print("D2) Datagramas recibidos que no pudieron ser entregados por cuestiones ",
        #     "distintas a la falta de aplicación en el puerto destino (udpNoPorts) 1.3.6.1.2.1.7.2.0 counter")
        self.Lista_Consultas[4] = self.consultaSNMP("1.3.6.1.2.1.7.2.0")
        rrdtool.update(self.Host+'/ports.rrd', "N:" + self.Lista_Consultas[4])
        rrdtool.dump(self.Host+'/ports.rrd','ports.xml')

        return self.Lista_Consultas

    def consultaSNMP(self,oid:str):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            # hace la solicitud getsnmp
            getCmd(SnmpEngine(),
                CommunityData(self.Comunidad),
                UdpTransportTarget((self.Host, 161)), # udp
                ContextData(),
                ObjectType(ObjectIdentity(oid)))) 

        # tratamiento de errores
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                varB=(' = '.join([x.prettyPrint() for x in varBind]))
                resultado= varB.split()[2] # se agarra la ultima parte de la consulta
        return resultado

    def nuevaRDD(self,nombreRRD:str):
        # creamos la bae de datos
        ret = rrdtool.create(self.Host+"/"+nombreRRD,
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

    def __eq__(self, agente):
        return self.Host==agente.Host



class Agentes:
    def __init__(self,comunidad:str):
        self.temp_list=[]
        self.agentes=[]
        self.Comunidad=comunidad
        with open("agentes.json",'r') as temp_file:
            self.temp_list=json.load(temp_file)
        print("Agentes actuales",self.temp_list)
        for host in self.temp_list:
            self.agentes.append(Agente(self.Comunidad,host))


    def agregar(self,host:str):
        self.temp_list.append(host)
        self.agentes.append(Agente(self.Comunidad,host))
        self.actualizar()

    def eliminar(self,host:str):
        self.temp_list.remove(host)
        self.agentes.remove(Agente(self.Comunidad,host))
        self.actualizar()

    def actualizar(self):
        with open("agentes.json",'w') as temp_file:
            json.dump(self.temp_list,temp_file)

    def status(self):
        for agente in self.agentes:
            agente.status()

    


if __name__=='__main__':

    comunidad="123"
    agentes=Agentes(comunidad)
    

    opcion=0
    while True:
        agentes.status()
        print("Menu:\n1)Alta.\n2.)Baja.\n3)ver trafico y generar reporte.\n4)Salir\n")
        opcion=int(input("Escriba la opcion: "))
        if opcion==1:
            nuevo_host=input("Escriba un host valido: ")
            # agentes.agregar(nuevo_host)
            print("Agregado")
            sleep(3)
        elif opcion==2:
            fuera_host=input("Escriba el host a eliminar: ")
            # agente.eliminar(fuera_host)
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
    
