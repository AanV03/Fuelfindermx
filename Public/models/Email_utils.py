from flask import Flask
from flask_mail import Mail, Message

# Configuración del correo
app = Flask(__name__)
app.secret_key = 'hello'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '_@gmail.com'  # Cambia por tu correo
app.config['MAIL_PASSWORD'] = 'FuelFindermx'  # Cambia por tu contraseña

mail = Mail(app)

def enviar_correo(destinatario):
    """
    Envía un correo electrónico al destinatario con un enlace de restablecimiento.
    """
    mensaje = Message(
        subject="Recuperación de contraseña",
        recipients=[destinatario]
    )
    mensaje.body = f"""
    Hola,

    Hemos recibido tu solicitud para restablecer la contraseña.
    Haz clic en el siguiente enlace para continuar:
    http://tu_dominio.com/restablecer_contrasena

    Si no solicitaste este cambio, ignora este mensaje.
    """
    try:
        with app.app_context():  # Contexto de la aplicación
            mail.send(mensaje)
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False
