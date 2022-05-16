




### al iniciar


al inicir en RCP, usuario y contraseña: RCP

```
rcp
rcp
// si damos ? aparece

enable          modo administrador
exit            salimos del modo actual
logout          salimos de la sesion
no              comando negativo
ping            mandar un mensaje a un nodo
show            mostrar alguna informacion
telnet-client   abrir una sesion telnet
traceroute      trazar una ruta de un nodo


```

### asignacion o cambio de ip a una interfaz de red

```
//mostrar interfaces
show interface
enable
configure
interface ethernet {interfaz que queremos manipular}
interface ethernet eth1
// entramos a la configuracion dela interfaz, procedemos a cambiar la ip
ip address 192.168.1.1/24
// ya esta asignada la ip, ahora necesitamos habilitarlo
no shutdown
exit
// ahora volvemos a mostrar las interfaces y debemos de evr la interfaz que modificamos con su ip respectiva y que este habilitada
show interface


```


### Configuracion de la persistencia


//accedemos con la credenciales por defecto y presionames f5
```
// nos vamos a la carpeta raiz
 cd ..

// vemos las aprticiones del disco
fdisk -l

// creamos la particion (tiene que coincidir el nombre de las unidades, por eso el comando anterior, en este caso seria)
fdisk /dev/sda
// presionamos 'm' para ver las opciones de las aprticiones
m
// como queremos crear una particion entonces presionamos 'n'
n
// elejimos la particion tipo primary 'p'
p
// numero de particion a manipular, como es una unica particion (por defecto 1), solo damos enter
(enter)
// toma elejir el primer sector y el ultimo (que vienen marcados por defecto)
(enter)
// elejimos el ultimo sector
(enter)
// quedo creada la particion y queda escribir la particion en el disco
// presionamos 'w' para escribir sobre el disco
w
// ya quedo creado, para comprobar ingresmos
fdisk -l
// debe de salir la particion que conicidan los los sectores por defecto,
// ya quedo creado la particion



```


### Creacion de un sistema de archivos en la nueva particion

```
// creamos el sistema de archivos y elejimos la particion del disco
mkfs.ext2 /dev/sda1
// despues reiniciamos la maquina con 
reboot

// ya una vez reiniciada la maquina entramos a la consola de debian con f5
// buscamos el archivo persist.sh
persist.sh
//si nos sale un menu con la particion que creamos hace rato, entonces ya esta creada la persistencia, queda seleccionar la particion con '1'
1
// volvemos a reiniciar para que se guarden los cambios


```

### comprobar que la persistencia este funcionando

```
// cambiamos el nombre de la maquina rcp
//ingresamos credenciales
enable
configure
hostname {Nombre que queremos}
// al dar enter se cambia el nombre en la entradda de comandos
// ahora guardamos todos los comandos que hemos ingresado en un archivo startup-config
copy running-config startup-config
// comprobamos que exista el archivo
dir

// nos movemos a la consala con f5
// nos movemso a la carpeta raiz y vamos al sig dicectorio
cd home/rcp
// debe de estar la carpeta startup-config
// pasamos a reiniciar la maquina y debe de conservar el nombre que le pusimos al principio
// ingresamos las credenciales y verificamos el nombre


```

### Configuracion del FTP (activarlo)


```
configure
service ftp


```

### MAndar archivos de un routeador a otro

ver la documentacion del comando copy
o ejecutar copy ? y poner atencion en como enviar por ftp
```


```