@ -1,22 +0,0 @@
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Cambia esto por tu servidor SMTP
app.config['MAIL_PORT'] = 587  # O el puerto que uses
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tu_email@example.com'  # Tu correo
app.config['MAIL_PASSWORD'] = 'tu_contraseña'  # Tu contraseña
app.config['MAIL_DEFAULT_SENDER'] = 'tu_email@example.com'  # Remitente por defecto

mail = Mail(app)

def enviar_correo(destinatario, token):
    mensaje = Message("Actualización de Contraseña",
                      recipients=[destinatario])
    mensaje.body = f"Para actualizar tu contraseña, haz clic en el siguiente enlace: http://tu_dominio.com/actualizar_contrasena?token={token}"
    
    with app.app_context():
        mail.send(mensaje)