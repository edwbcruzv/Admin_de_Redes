

### Creacion de una interfaz de red (tap0)

```
// creacion de una interfaz
sudo tunctl -u cruz
// necesitamos asignarle una ip y habilitarla
sudo ifconfig tap0 {ip} up
// verificamos si sesta habilitada
ifconfig

```


### Modificar el gateway de una interfaz

Por defecto todo el trafico de la computadora se va por la interfaz inalambrica que es el que esta por defecto


```
// mostrar la tabla de roteo
sudo route -v
// para deviar el trafico a la interfaz tap0
sudo route add -net {mask origen} netmask 255.255.255.0 gw {ip destino} dev tap0
// verificamos que se haya modificado la tabla de enrutamiento
sudo route -v
// ahora el trafico que vaya del 192.168.201.0 ira al tap0
```

### Conectarnos mediante FTP a un routerador y mandar archivos
anters de conectarnos al routeador, primero necesitamos estar en la carpeta donde se encuentrar los archivos que queremos mandar al router, ya estando ahi pasamos a las intrucciones
```

// primero verificamos conectividad con ping
// ya comprobando que que recibamos respuestas mutuamente pasamos a conectarnos
ftp {ip del router}
// ingresamos las credenciales del routeador

// cone  comando put mandamos los archivos
put {archivo} {nombre con el que llegara al routeador el archivo}

// ya que mandamos el o los archivos pasamos a reiniciar el routeador, pero antes
// debe de estar configurado la persistencia en el routeador, si ya esta se procede a // reiniciar
reboot

```