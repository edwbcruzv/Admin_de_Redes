from ftplib import FTP

ftp=FTP(host="192.168.1.2",user="rcp",passwd="rcp")

print(ftp.getwelcome())
print(ftp.dir())


# enviar archivos al servidor
# filename = "some_file.txt"
# with open(filename, "rb") as file:
#     # use FTP's STOR command to upload the file
#     ftp.storbinary(f"STOR {filename}", file)


# descargar archivos del servidor
filename = "startup-config"
with open(filename, "wb") as file:
#     # use FTP's RETR command to download the file
    ftp.retrbinary(f"RETR {filename}", file.write)

print(ftp.quit())