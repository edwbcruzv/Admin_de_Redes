import sys
import rrdtool
import time

while True:
    time.sleep(0.5)
    # tiempo actual
    tiempo_actual = int(time.time())
    #Grafica desde el tiempo actual menos diez minutos
    tiempo_inicial = tiempo_actual - 300 #5 minutos

    # solo se generara una grafica en base al tradico de red


    ret = rrdtool.graph( "traficoRED.png",
                        "--start",str(tiempo_inicial),
                        "--end","N",
                        "--vertical-label=Bytes/s", # maquillaje para la grafica
                        "--title=Tráfico de Red de un agente \n Usando SNMP y RRDtools", # maquillaje para la grafica
                        # se consulta la informacion para graficarlo
                        "DEF:traficoEntrada=traficoRED.rrd:inoctets:AVERAGE",
                        # se consulta la informacion para graficarla
                        "DEF:traficoSalida=traficoRED.rrd:outoctets:AVERAGE",
                        # recorre toda la coleccion para convertir los octetos a bites
                        "CDEF:escalaIn=traficoEntrada,8,*",
                        # recorre toda la coleccion para convertir los octetos a bites
                        "CDEF:escalaOut=traficoSalida,8,*",
                        # Para imprimir los datos
                        "LINE3:escalaIn#FF0000:Trafico de entrada",
                        "LINE3:escalaOut#0000FF:Tráfico de salida")


