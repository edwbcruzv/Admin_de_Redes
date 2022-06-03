# Enviar correo al buzón especificado
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
import fileinput
aux=fileinput.input()
print(aux)
 
user_mail = 'dummycuenta3@gmail.com'
contrasena = 'Secreto123#'
send_mail = 'dummycuenta3@gmail.com'
smtp_server = 'snmtp.gmail.com:587'



# Complete el cuerpo del correo electrónico, la información del remitente, la información del destinatario, el asunto
msg = MIMEMultipart()	
msg['Subject'] = "Alerta del tio cruz"
msg['From'] = user_mail
msg['To'] = send_mail

server = smtplib.SMTP("smtp.gmail.com:587") #Ejecute el puerto 25 del servidor de la oficina postal
server.starttls()		#	
server.login(user_mail, contrasena) #Iniciar sesión en el servidor
server.sendmail(user_mail,send_mail, msg.as_string ()) # Enviar correo a la dirección especificada
server.quit() # Servicio final
print("alerta enviada a correo")