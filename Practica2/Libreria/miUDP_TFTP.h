#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netinet/ip.h> /* superset of previous */
#include <arpa/inet.h>

//Estructura que se mandara al los hilos, ya que solo aceptan un parametro
typedef struct datos_dir{
        int udp_socket; //socket asociado a la direccion
        struct sockaddr_in *dir; //direccion, esta sera dinamica
    }*Direccion;

typedef struct tftp_strct{
    unsigned char* peticion;
    int longitud;
    }*TFTP_Struct;
    
//recibe solo el arreglo y el tamaño del arreglo y esta funcion hace todo el proceso dinamico de lo recibido
TFTP_Struct NuevoStructTFTP(unsigned char* paq,int lon){

    TFTP_Struct temp=(TFTP_Struct)malloc(sizeof(struct tftp_strct));
    temp->peticion=(unsigned char*)malloc(sizeof(unsigned char)*lon);
    memcpy(temp->peticion,paq,lon);
    temp->longitud=lon;
    return temp;
}

// imprime los datos del paquete que se recibe como parametro
int MostrarTFTP_Struct(TFTP_Struct paq){
    for (int i = 0; i < paq->longitud; i++)
    {
        fprintf(stdout,"\n[%d]=%c,%d,%x",i,paq->peticion[i],paq->peticion[i],paq->peticion[i]);
    }
    //printf("fin");
}
//**************************INICIO DE LAS ESTRUCTURAS **************************//


//Esctructura de Solicitud de lectura
//     2 bytes     string    1 byte     string   1 byte
//     ------------------------------------------------
//    | Opcode |  Filename  |   0  |    Mode    |   0  |
//     ------------------------------------------------

TFTP_Struct Struct_RRQ(unsigned char *name_file){
    unsigned char paq[516];

    unsigned char code[]={0x00,0x01};
    unsigned char cero[]={0x00};
    unsigned char mode[]="octet";

    int ptr=0;
    memcpy(paq+ptr,code,2);
    ptr=ptr+2;

    memcpy(paq+ptr,name_file,strlen(name_file));
    ptr=ptr+strlen(name_file);

    memcpy(paq+ptr,cero,1);
    ptr=ptr+1;

    memcpy(paq+ptr,mode,strlen(mode));
    ptr=ptr+strlen(mode);

    memcpy(paq+ptr,cero,1);
    ptr=ptr+1;


    return NuevoStructTFTP(paq,ptr);
}

//Estrcutura de Solicitud de escritura
//     2 bytes     string    1 byte     string   1 byte
//     ------------------------------------------------
//    | Opcode |  Filename  |   0  |    Mode    |   0  |
//     ------------------------------------------------
TFTP_Struct Struct_WRQ(unsigned char *name_file){
    unsigned char paq[516];
    
    unsigned char code[]={0x00,0x02};
    unsigned char mode[]="octet";
    unsigned char cero[]={0x00};

    int ptr=0; 
    memcpy(paq+ptr,code,2);
    ptr=ptr+2;
    
    memcpy(paq+ptr,name_file,strlen(name_file));
    ptr=ptr+strlen(name_file);
     
    memcpy(paq+ptr,cero,1);
    ptr=ptr+1;

    memcpy(paq+ptr,mode,strlen(mode));
    ptr=ptr+strlen(mode);

    memcpy(paq+ptr,cero,1);
    ptr=ptr+1;

    return NuevoStructTFTP(paq,ptr);
}
//Esctructura de Paquete de datos
//    2 bytes     2 bytes      n bytes
//    ----------------------------------
//   | Opcode |   Block #  |   Data     |
//    ----------------------------------
TFTP_Struct Struct_DATA(unsigned char * num_block,unsigned char *data,int tam_data){
    unsigned char paq[516];
    
    unsigned char code[2]={0x00,0x03};
    int ptr=0;
    memcpy(paq+ptr,code,2);
    ptr=ptr+2;
    memcpy(paq+ptr,num_block,2);
    ptr=ptr+2;
    memcpy(paq+ptr,data,tam_data);
    ptr=ptr+tam_data;
    
    return NuevoStructTFTP(paq,ptr);
}
//Estructura de Paquete de confirmacion o Reconocimiento
//   2 bytes     2 bytes
//   ---------------------
//  | Opcode |   Block #  |
//   ---------------------
TFTP_Struct Struct_ACK(unsigned char *num_block){
    unsigned char paq[516];

    unsigned char code[2]={0x00,0x04};
    int ptr=0;
    memcpy(paq+ptr,code,2);
    ptr=ptr+2;
    memcpy(paq+ptr,num_block,2);
    ptr=ptr+2;

    return NuevoStructTFTP(paq,ptr);
}
//Estructura de Paquete de error
//    2 bytes     2 bytes      string    1 byte
//    -----------------------------------------
//   | Opcode |  ErrorCode |   ErrMsg   |   0  |
//    -----------------------------------------
TFTP_Struct Struct_ERROR(unsigned char *code_error,unsigned char *msj_error){
    unsigned char paq[516];

    unsigned char code[2]={0x00,0x05};
    unsigned char cero[]={0x00};

    int ptr=0;
    memcpy(paq+ptr,code,2);
    ptr=ptr+2;
    memcpy(paq+ptr,code_error,2);
    ptr=ptr+2;
    memcpy(paq+ptr,msj_error,strlen(msj_error));
    ptr=ptr+strlen(msj_error);
    memcpy(paq+ptr,cero,1);
    ptr=ptr+1;
    return NuevoStructTFTP(paq,ptr);
}
//**************************FIN DE LAS ESTRUCTURAS **************************//


///////////////////////////////////////////UDP/////////////////////////////////////////////////
//Regresa un descriptor de socket al mandar a llamar a la funcion
int crearSocket(){
    int udp_socket = socket(AF_INET, SOCK_DGRAM, 0);

    if (udp_socket==-1){
        perror("Error al abrir el socket, buscar el error en el manual (man socket)\n");
        exit(0);
    }
    else{
        perror("Exito al abrir el socket.");
    }

    return udp_socket;
}
//Esta funcion es usada por EL CLIENTE y SERVIDOR para definir sus propias direcciones locales
//Recibe un numero entero que indicara el puerto 
struct sockaddr_in *crearLocal(int puerto){
    struct sockaddr_in *servidor=(struct sockaddr_in*)malloc(sizeof(struct sockaddr_in));
    servidor->sin_family=AF_INET; /* address family: AF_INET */
    servidor->sin_port=htons(puerto);   /* port in network byte order*/
    servidor->sin_addr.s_addr=INADDR_ANY;   /* internet address */
    return servidor;
}
//Esta funcion es usada por EL CLIENTE
//Recibe el puerto y la direccion ip el formato de cadena
struct sockaddr_in *crearRemota(int puerto,char ips_serv[]){
    struct sockaddr_in *remota=(struct sockaddr_in*)malloc(sizeof(struct sockaddr_in));
    remota->sin_family=AF_INET; /* address family: AF_INET */
    remota->sin_port=htons(puerto);  /* es el puerto por defecto por donde se manda mensaje*/
    remota->sin_addr.s_addr=inet_addr(ips_serv);  /*ip del servidor*/
    return remota;
}
//Esta funcion es usada por EL SERVIDOR
//regresa una estructura vacia la cual sera llenado por una funcion al momento de recibir un paquete
struct sockaddr_in *crearCliente(){
    struct sockaddr_in *cliente=(struct sockaddr_in*)malloc(sizeof(struct sockaddr_in));
    // cliente.sin_family=AF_INET; /* address family: AF_INET */
    // cliente.sin_port=htons(53);  /* es el puerto por defecto por donde se manda mensaje*/
    // cliente.sin_addr.s_addr=inet_addr("8.8.8.8");  /*ip del servidor*/
    return cliente; //no se llena, solo se declara la estructura
}

//asocia el socket enviado y la estructura de la direccion local
int crearBind(int socket,struct sockaddr_in *dir){

    int lbind=bind(socket,(struct sockaddr*)dir,sizeof(*dir)); //se necesita el tamanio donde apunto
    if(lbind==-1){
        perror("Error en bind.");
        exit(0);
    }
    else{
        perror("Exito en bind.");
    }
    return lbind;
}
// Esta funcion se dedica a recibir paquetes
// Esta asociado a la Direccion que contiene:
// el socked y la direccion ip del origen, 
// regresa el paquete recibido
// si hay un error regresa -1 en unsigned
TFTP_Struct recibir(Direccion direc){
    unsigned char paq_recv[516];  //512 por defecto
    struct sockaddr_in dir_temp=*(direc->dir);
    int socket=direc->udp_socket;
    int len_dir=sizeof(dir_temp);
    //MSG_DONTWAIT
    int lrecv=recvfrom(socket,paq_recv, 516,0,(struct sockaddr *)&dir_temp,&len_dir);
    if(lrecv==-1){
        perror("\nError al recibir.\n");
        return NULL;
    }
    else{
        // esto es necesario para el servidor, debe de obtener los tatos del remitente
        *(direc->dir)=dir_temp; 

        //Almacenamiento del mensaje para regreasarlo 
        return NuevoStructTFTP(paq_recv,lrecv);
    }
    
}

// Esta funcion se dedicara a enviar paquetes 
// asociando a la Direccion que contiene:
// socket, el mensaje y la direccion ip a la que se envia
// regresa 0 si tuvo exito
// si hay un error regresa -1
int enviar(Direccion direc,TFTP_Struct paq){

    struct sockaddr_in dir_temp=*(direc->dir);
    int socket=direc->udp_socket;
    //MSG_DONTWAIT
    int tam=sendto(socket,paq->peticion,paq->longitud,0,(struct sockaddr *)&dir_temp,sizeof(dir_temp));
    
    if(tam==-1){
        //perror("\nError en enviar.\n");
        return -1;
    }
    else{
        //perror("Exito en enviar.");
        return 0;
    }
}
////////////////////////////////////////FIN UDP//////////////////////////////////////////////