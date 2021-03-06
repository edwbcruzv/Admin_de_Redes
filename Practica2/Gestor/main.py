# from GetSNMP import *
from pysnmp.hlapi import *
import rrdtool
from time import *
import json
import os
import threading
from reportlab.pdfgen import canvas


class Agente:

    def __init__(self,comunidad:str,host:str):
        self.Comunidad=comunidad
        self.Host=host
        self.Nombre_sistema=None
        # Version y logo del sistema operativo (lo ponemos nosotros)
        # Ubicacion geografica 
        self.Num_interfaces=None
        self.Tiempo_Activo=None
        self.Lista_Consultas=[0,0,0,0]
        # Creando carpeta para almacenar las bases de datos generadas

        try:
            os.mkdir(self.Host)
        except:
            pass

    def status(self)->bool:
        try:
            self.Nombre_sistema=self.consultaSNMP("1.3.6.1.2.1.1.1.0")
            # Ubicacion geografica 
            self.Num_interfaces=self.consultaSNMP("1.3.6.1.2.1.2.1.0") 
            self.Tiempo_Activo=self.consultaSNMP("1.3.6.1.2.1.1.3.0")  
            print("|==============================|\nComunidad:",self.Comunidad)
            print("Host:",self.Host)
            print("Nombre del sistema:",self.Nombre_sistema)
            print("Numero de interfaces de red:",self.Num_interfaces)
            print("Tiempo desde el ultimo reinicio:",self.Tiempo_Activo,"Segs")
            return True
        except :
            print("Error en status")
            return False
        

    def registrar(self):
        self.nuevaRDD("miUDP.rrd") # creando base de datos para 10 min
        # dejando 10 min corriendo el while para llenar la base de datos
        inicio=time()
        fin= inicio + 600# 10 minutos
        while True:
            print(self.updateListaConsultas())
            inicio=time()
            if not inicio < fin:
                break
        print(rrdtool.lastupdate(self.Host+"/"+"miUDP.rrd"))
        pass

    def reporte(self):
        ultima_lectura=int(rrdtool.last(self.Host+"/"+"miUDP.rrd"))
        print(ultima_lectura)
        tiempo_final=ultima_lectura
        tiempo_inicial=tiempo_final-600
        
        dicc=rrdtool.fetch(self.Host+'/miUDP.rrd',"-s,"+str(tiempo_inicial),"LAST")
        Filas=60
        datos=dicc[2][Filas-1]
        print(dicc)

        print("|=============Servicio UDP TFTP=================|")
        print("Comunidad:",self.Comunidad)
        print("Host:",self.Host)
        print("Nombre del sistema:",self.Nombre_sistema)
        print("Numero de interfaces de red:",self.Num_interfaces)
        print("Tiempo desde el ultimo reinicio:",self.Tiempo_Activo,"Segs")
        
        # print("#udpInDatagrams:",datos[0])
        # print("#udpNoPorts:",datos[1])
        # print("#updInErrors:",datos[2])
        # print("#udpOutDatagrams:",datos[3])
            

    def updateListaConsultas(self)->list:
        #str_mib="1.3.6.1.2.1."
        # 18 reply mesage
        # 47 acct-input-packets
        # 48 acct-output-packets

        # udpInDatagrams: 1.3.6.1.2.1.7.1
        self.Lista_Consultas[0] = self.consultaSNMP("1.3.6.1.2.1.7.1.0") 
        # udpNoPorts: 1.3.6.1.2.1.7.2
        self.Lista_Consultas[1] = self.consultaSNMP("1.3.6.1.2.1.7.2.0")
        # updInErrors: 1.3.6.1.2.1.7.3
        self.Lista_Consultas[2] = self.consultaSNMP("1.3.6.1.2.1.7.3.0")
        # udpOutDatagrams: 1.3.6.1.2.1.7.4
        self.Lista_Consultas[3] = self.consultaSNMP("1.3.6.1.2.1.7.4.0") 
        # # udpLocalAddress: 1.3.6.1.2.1.7.5.1.1
        # self.Lista_Consultas[5] = self.consultaSNMP("1.3.6.1.2.1.7.5.1.1")
        # # udpLocalPort: 1.3.6.1.2.1.7.5.1.2
        # self.Lista_Consultas[6] = self.consultaSNMP("1.3.6.1.2.1.7.5.1.2")

        rrdtool.update(self.Host+'/miUDP.rrd', "N:" + self.Lista_Consultas[0] + ":"
            + self.Lista_Consultas[1] + ":" + self.Lista_Consultas[2] + ":" + self.Lista_Consultas[3])
        rrdtool.dump(self.Host+'/miUDP.rrd',self.Host+'/miUDP.xml')
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
                # print(varB)
                resultado= varB.split()[2] # se agarra la ultima parte de la consulta
        return resultado

    def nuevaRDD(self,nombreRRD:str):
        # creamos la bae de datos
        ret = rrdtool.create(self.Host+"/"+nombreRRD,
                            "--start", # momento que se empieza a almacenar los datos
                            'N',# now (empieza al momento de ejecutar el script) (tambien un numero)
                            "--step", # un step
                            '10',      # cada minuto
        #DS: Octetos de entrada : Tipo contador : cada dos minutos : sin limites minumos : sin limites maximos
                            "DS:con1:COUNTER:60:U:U",
                            "DS:con2:COUNTER:60:U:U",
                            "DS:con3:COUNTER:60:U:U",
                            "DS:con4:COUNTER:60:U:U",
        #RRA: Cada 60 segs de hace un : la mitad de muestras se validan: cada 1 step : numero de filas en la base de datos
                            "RRA:AVERAGE:0:1:60") #60 filas, 10segs cada uno

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
        nuevo=Agente(self.Comunidad,host)
        if nuevo.status():
            self.temp_list.append(host)
            self.agentes.append(nuevo)
            self.actualizar()
            return True
        else:
            del nuevo
            return False

    def eliminar(self,host:str):
        nuevo=Agente(self.Comunidad,host)
        if nuevo.status():
            self.temp_list.remove(host)
            self.agentes.remove(nuevo)
            self.actualizar()
            return True
        else:
            return False

    def actualizar(self):
        with open("agentes.json",'w') as temp_file:
            json.dump(self.temp_list,temp_file)
        
    def trafico(self):
        list_hilos=[]
        for index,agente in zip(range(0,len(self.agentes)),self.agentes):
        #for agente in self.agentes:
            list_hilos.append(threading.Thread(target=agente.registrar))
            list_hilos[index].start()
        pass

    def reportes(self):
        for agente in self.agentes:
            agente.reporte()
        
        
    def status(self):
        for agente in self.agentes:
            agente.status()


if __name__=='__main__':

    comunidad="123"
    agentes=Agentes(comunidad)
    
    opcion=0
    while True:
        # os.system("clear")
        # print(agentes.temp_list)
        # agentes.status()
        print("|==============================|")
        print("Menu:\n1)Alta.\n2)Baja.\n3)Trafico.\n4)Generar reporte\n5)Salir\n")
        opcion=int(input("Escriba la opcion: "))
        if opcion==1:
            nuevo_host=input("Escriba un host valido: ")
            if agentes.agregar(nuevo_host):
                print("Agregado.")
            else:
                print("No se encontro el agente.")
            sleep(3)
        elif opcion==2:
            fuera_host=input("Escriba el host a eliminar: ")
            if agentes.eliminar(fuera_host):
                print("Eliminado")
            else:
                print("No se encontro el agente a eliminar.") 
            sleep(3)
        elif opcion==3:
            print("Espere 10 min para que se llene la base de datos...")
            agentes.trafico()
            sleep(2)
        elif opcion==4:
            print("Generando reportes... Espere")
            agentes.reportes()
            sleep(2)
        elif opcion==5:
            break
        else:
            continue
    
