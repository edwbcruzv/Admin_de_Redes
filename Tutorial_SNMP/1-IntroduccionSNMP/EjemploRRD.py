
# importacion del modulo
import rrdtool
# al ejecutar el archivo se va a generar:
#   speed.png (grafica)
#   test.rrd
#   test.xml

# se crea una base de datos 
ret = rrdtool.create("test.rrd", # nombre del archivo a generar
                     #step:300
                     "--start",
# contador tipo EPOC, numero de segundos desde el 1 de enero de 1970
                      '920804400', 
# (datasource)DS:es una variable que guarda la informacion:(tipo)Contador:(Numero de segundos entre cada update):Limite inferior:Limite superior
                     "DS:speed:COUNTER:600:U:U", 
# Modo de almacenar la informacio(Circular):AVERAGE(funcion promedio):numero de muestras validas en un intervalo de tiempo:cada cuanto se hace un AVerage:longitud del archivo .rrd
                     "RRA:AVERAGE:0.5:1:24",# (se hace una captura de informacion entre Max y Min, despues se hace un promedio y se almacena)
                     "RRA:AVERAGE:0.5:6:10")# lo mismo de arriba pero cambiando el step y el tamaño del .rrd

# rrdtool.dump('test.rrd','test.xml');# traduccion del .rrd a .xml


# Guardar o actualiza la informacion en la base de datos
# cada 5 min sube el Kilometraje de un carro
upd = rrdtool.update('test.rrd', #Nombre de la base de datos
                     '920804700:12345', # (Tupla) Tiempo:Valor
                     '920805000:12357','920805300:12363',
                     '920805600:12363','920805900:12363',
                     '920806200:12373','920806500:12383',
                     '920806800:12393', '920807100:12399',
                     '920807400:12405', '920807700:12411',
                     '920808000:12415','920808300:12420',
                     '920808600:12422','920808900:12423')

rrdtool.dump('test.rrd','test.xml'); # traduccion del .rrd a .xml

# Genera la grafica de la informacion
gra= rrdtool.graph("speed.png", #nombre del archivo
                   "--start", "920804400",
                   "--end", "920808000",
                   #indica el data-source (esta definida al crear la base de datos)
                   "DEF:myspeed=test.rrd:speed:AVERAGE", 
                   #imprime la linea en la grafica
                   "LINE1:myspeed#FF0000")