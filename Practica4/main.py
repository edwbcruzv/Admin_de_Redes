from ftplib import FTP
import getpass
from traceback import print_tb
# import telnetlib
# from telnetlib import Telnet


# def conexionTELNET():
#     # HOST = "http://192.168.1.2:23/"
#     # HOST = "192.168.1.2"
#     user = input("Enter your remote account: ")
#     password = getpass.getpass()

#     # tn = telnetlib.Telnet(HOST)
#     with Telnet('192.168.1.2', 23) as tn:
#         # tn.interact()

#         tn.read_until(b"login: ")
#         tn.write(user.encode('ascii') + b"\n")
#         if password:
#             tn.read_until(b"Password: ")
#             tn.write(password.encode('ascii') + b"\n")

#     # tn.write(b"ls\n")
#     # tn.write(b"exit\n")

#     # print(tn.read_all().decode('ascii'))


class conexionFTP:

    def __init__(self,ip:str,usuario:str,pw:str) -> None:
        self.ftp=FTP(host=ip,user=usuario,passwd=pw)
        print(self.ftp.getwelcome())
        # print(self.ftp.dir())


    # enviar archivos al servidor
    def enviarArchivo(self,filename:str,newname:str):
        with open(filename, "rb") as file:
            # use FTP's STOR command to upload the file
            self.ftp.storbinary(f"STOR {newname}", file)
        
        # print(self.ftp.sendcmd("enable"))
        # print(self.ftp.sendcmd("configure"))
        # print(self.ftp.sendcmd("copy running-config startup-config"))


    # descargar archivos del servidor
    def descargarArchivo(self,filename:str,newname:str):
        with open(newname, "wb") as file:
        #     # use FTP's RETR command to download the file
            self.ftp.retrbinary(f"RETR {filename}", file.write)
        print(self.ftp.quit())
    
    def __del__(self):
        self.ftp.close()
        print("Se cerro conexion ftp")

class Menu:

    def __init__(self) -> None:
        # Nos conectamos a R1
        opcion=1
        while opcion:
            opcion=0
            try:
                opcion=int(input("Escoje 1 para configurar o 2 para backup: "))
            except:
                opcion=1
                print("Escoje de nuevo una opcion")

            if opcion==1:
                self.confRouter()
            elif opcion==2:
                self.backupRouters()
    def confRouter(self):
        try:
            R1=conexionFTP("192.168.201.15","rcp","rcp")
            R1.enviarArchivo("R1.txt","startup-config")
            del R1
            print("Exito al configurar R1")
        except:
            print("Error al configurar R1")

        try:
            R2=conexionFTP("192.168.232.2","rcp","rcp")
            R2.enviarArchivo("R2.txt","startup-config")

            del R2
            print("Exito al configurar R2")
        except:
            print("Error al configurar R2")

        # try:
        #     R3=conexionFTP("192.168.232.5","rcp","rcp")
        #     R3.enviarArchivo("R3.txt","startup-config")

        #     del R3
        #     print("Exito al configurar R3")
        # except:
        #     print("Error al configurar R3")

    def backupRouters(self):

        try:
            R1=conexionFTP("192.168.201.15","rcp","rcp")
            R1.descargarArchivo("startup-config","R1.txt")
            del R1
            print("Exito en backup de R1")
        except:
            print("Error en backup de R1")

        try:
            R2=conexionFTP("192.168.232.2","rcp","rcp")
            R2.enviarArchivo("startup-config","R2.txt")

            del R2
            print("Exito en backup de R2")
        except:
            print("Error en backup de R2")

        try:
            R3=conexionFTP("192.168.232.5","rcp","rcp")
            R3.enviarArchivo("startup-config","R3.txt")

            del R3
            print("Exito en backup de R3")
        except:
            print("Error en backup de R3")


x=Menu()