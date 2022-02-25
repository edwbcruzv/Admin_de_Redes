import time
import rrdtool
from GetSNMP import consultaSNMP
total_input_traffic = 0
total_output_traffic = 0


while 1:
    total_input_traffic = int(
        consultaSNMP('123','localhost', #se hace el getsnmp
                     '1.3.6.1.2.1.6.10.0')) # octetos de entrada TCP
    total_output_traffic = int(
        consultaSNMP('123','localhost',
                     '1.3.6.1.2.1.2.2.1.16.2')) # octetos de salida

    # se arma el valor de la hora de lectura para despues almacenarlo
    valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
    print (valor)

    # se guarda o actualiza la base de datos
    rrdtool.update('traficoRED.rrd', valor)

    #
    rrdtool.dump('traficoRED.rrd','traficoRED.xml')
    time.sleep(1)

if ret:
    print (rrdtool.error())
    time.sleep(300)