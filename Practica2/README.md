# Practica 2

[RFC2975:Introducción a la Gestión Contable](https://datatracker.ietf.org/doc/html/rfc2975)
[RFC2924:Atributos contables y formatos de registro](https://www.rfc-editor.org/rfc/rfc2924.html)


![Imagen de la arquitectura](Arquitectura%20Prac2.png)

[Arquitectura de la RFC2924](https://www.rfc-editor.org/rfc/rfc2924.html#section-3)

[Seccion de los parametros que usaremos de la RFC294](https://www.rfc-editor.org/rfc/rfc2924.html#section-4.1)




-- el grupo UDP

          -- La implementación del grupo UDP es obligatoria para todos
          -- sistemas que implementan UDP. 

          udpInDatagrams TIPO DE OBJETO 
              SINTAXIS Contador 
              ACCESO solo lectura 
              ESTADO obligatorio 
              DESCRIPCIÓN 
                      "El número total de datagramas UDP entregados a 
                      usuarios UDP". 
              ::= { udp 1 } 

          udpNoPorts OBJECT-TYPE 
              SYNTAX Counter 
              ACCESS read-only 
              ESTADO obligatorio 
              DESCRIPCIÓN 
                      "El número total de datagramas UDP recibidos para 
                      los que no había ninguna aplicación en el destino
                      port." 
              ::= { udp 2 } 

          udpInErrors OBJECT-TYPE 
              SYNTAX Counter 
              ACCESS read-only 
              ESTADO obligatorio 
              DESCRIPCIÓN 
                      "El número de datagramas UDP recibidos que 
                      no se pudieron entregar por razones distintas a la falta 
                      de una aplicación en el puerto de destino". 
              ::= { udp 3 } Grupo de trabajo SNMP [Página 52]
        
        udpOutDatagrams TIPO DE OBJETO
              SINTAXIS Contador
              ACCESO solo lectura
              ESTADO obligatorio
              DESCRIPCIÓN
                      "El número total de datagramas UDP enviados desde esta
                      entidad". 
              ::= { udp 4 }


          -- la tabla UDP Listener

          -- La tabla UDP listener contiene información sobre
          -- los puntos finales UDP de la entidad en los que una aplicación local
          -- actualmente acepta datagramas. 

          udpTable
              SECUENCIA DE SINTAXIS DE TIPO DE OBJETO DE UdpEntry
              ACCESO no accesible 
              ESTADO obligatorio 
              DESCRIPCIÓN 
                      "Una tabla que contiene información de escucha UDP". 
              ::= { udp 5 } 

          udpEntry TIPO DE OBJETO 
              SINTAXIS UdpEntry 
              ACCESO no accesible 
              ESTADO obligatorio 
              DESCRIPCIÓN "Información sobre un 
                      oyente 
                      UDP actual en particular ". 
              ÍNDICE { udpLocalAddress, udpLocalPort } 
              ::= { udpTable 1 } 
          UdpEntry ::= 
              SEQUENCE { 
                  udpLocalAddress,
                      IpAddress, 
                  udpLocalPort 
                      INTEGER (0..65535) 
              } 

          udpLocalAddress TIPO DE OBJETO 
              SYNTAX IpAddress 
              ACCESO solo lectura 
              ESTADO obligatorio 
              DESCRIPCIÓN 
                      "La dirección IP local para este oyente UDP. En el grupo de trabajo SNMP [Página 53]
                      el caso de un oyente UDP que está dispuesto a
                      aceptar datagramas para cualquier interfaz IP asociada
                      con el nodo, se utiliza el valor 0.0.0.0."
              ::= { udpEntry 1 }

        udpLocalPort OBJECT-TYPE
              SYNTAX INTEGER (0..65535)
              ACCESO de solo lectura
              ESTADO obligatorio
              DESCRIPCIÓN
                      "El número de puerto local para este oyente UDP".
              ::= { udpEntry 2 }

        