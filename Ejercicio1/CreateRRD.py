import rrdtool

# solo se va acrear la base de datos

# creamos la bae de datos
ret = rrdtool.create("traficoRED.rrd",
                     "--start", # momento que se empieza a almacenar los datos
                     'N',# now (empieza al momento de ejecutar el script) (tambien un numero)
                     "--step", # un step
                     '60',      # cada minuto
#DS: Octetos de entrada : Tipo contador : cada dos minutos : sin limites minumos : sin limites maximos
                     "DS:segmentosEntrada:COUNTER:120:U:U",# captura los datos de entrada
#DS: Octetos de salida : Tipo contador : cada dos minutos : sin limites minumos : sin limites maximos
                     "DS:segmentosSalida:COUNTER:120:U:U",# captura los datos de salida
#RRA: Cada 60 segs se hace un AVERAGE : la mitad de muestras se validan: cada 6 step : numero de filas en la base de datos
                     "RRA:AVERAGE:0.5:6:5",
#RRA: Cada 60 segs de hace un AVERAGE: la mitad de muestras se validan: cada 1 step : numero de filas en la base de datos
                     "RRA:AVERAGE:0.5:1:20")


#en caso de haber un error lo sabremos
if ret:
    print (rrdtool.error())