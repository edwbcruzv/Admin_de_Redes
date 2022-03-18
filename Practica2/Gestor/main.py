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
        self.Lista_Consultas=[0,0,0,0,0,0,0]
        # Creando carpeta para almacenar las bases de datos generadas

        try:
            os.mkdir(self.Host)
        except:
            pass

    def status(self)->bool:
        try:
            self.Nombre_sistema=self.consultaSNMP("1.3.6.1.2.1.1.1.0")
            # Version y logo del sistema operativo (lo ponemos nosotros)
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
        

    def reporte(self):
        print(self.updateListaConsultas())
        
            

    def updateListaConsultas(self)->list:
        #str_mib="1.3.6.1.2.1."
       
        self.Lista_Consultas[0] = self.consultaSNMP("1.3.6.1.2.1.2.2.1.12.1.0")
        # udpInDatagrams: 1.3.6.1.2.1.7.1
        self.Lista_Consultas[1] = self.consultaSNMP("1.3.6.1.2.1.7.1.0")
        # udpNoPorts: 1.3.6.1.2.1.7.2
        self.Lista_Consultas[2] = self.consultaSNMP("1.3.6.1.2.1.7.2.0")
        # updInErrors: 1.3.6.1.2.1.7.3
        self.Lista_Consultas[3] = self.consultaSNMP("1.3.6.1.2.1.7.3.0")
        # udpOutDatagrams: 1.3.6.1.2.1.7.4
        self.Lista_Consultas[4] = self.consultaSNMP("1.3.6.1.2.1.7.4.0")
        # udpLocalAddress: 1.3.6.1.2.1.7.5.1.1
        self.Lista_Consultas[5] = self.consultaSNMP("1.3.6.1.2.1.7.5.1.1.1")
        # udpLocalPort: 1.3.6.1.2.1.7.5.1.2
        self.Lista_Consultas[6] = self.consultaSNMP("1.3.6.1.2.1.7.5.1.2.1")

    
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

    

    def __eq__(self, agente):
        return self.Host==agente.Host

    def reporte(self):
        c=canvas.Canvas(self.Host+"/"+self.Host+"_report.pdf")
        
        c.drawString(170, 780, "Reporte de trafico hecho por Cruz villalba Edwin Benrardo")

        datos_principales= ("Comunidad:"+self.Comunidad+"\n",
                "Host:"+self.Host+"\n",
                "Nombre del sistema:"+self.Nombre_sistema+"\n",
                "Numero de interfaces:"+self.Num_interfaces+"\n",
                "Tiempo activo:"+self.Tiempo_Activo)
        texto=c.beginText(70,760)
        texto.textLines(datos_principales)
        c.drawImage(self.Host+"/ports.png", 150,350, width=250, height=100)
        c.drawText(texto)
        c.save()


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
        pass
        list_hilos=[]
        for index,agente in zip(range(0,len(self.agentes)),self.agentes):
        #for agente in self.agentes:
            list_hilos.append(threading.Thread(target=agente.analisis))
            list_hilos[index].start()

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
        os.system("clear")
        print(agentes.temp_list)
        agentes.status()
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
            print("Espere 16 min para que se llene la base de datos...")
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
    
