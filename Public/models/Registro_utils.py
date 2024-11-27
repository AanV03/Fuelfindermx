from conexion import obtener_conexion
from werkzeug.security import generate_password_hash
import re

def registrar_usuario(nombre, apellido, email, contraseña, confirmar_contraseña, security_question_id, security_answer):
    "Función para registrar un nuevo usuario en la base de datos."
    
    # Validar contraseñas
    if contraseña != confirmar_contraseña:
        return "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.", 400

    # Cifrar la contraseña
    contraseña_cifrada = generate_password_hash(str(contraseña))
    
    # Validar que la respuesta de seguridad no esté vacía
    if not security_answer:
        return "La respuesta de seguridad no puede estar vacía.", 400

    # Conectar a la base de datos y guardar los datos
    conexion = None
    try:
        conexion = obtener_conexion()  # Usar la función de conexión de conexion.py
        if conexion is None:
            return "No se pudo establecer conexión con la base de datos.", 500
            
        with conexion.cursor() as cursor:
            # Insertar el usuario junto con la pregunta de seguridad y la respuesta
            query = """
            INSERT INTO dbo.Usuarios (Nombre, Apellido, Email, Contraseña, security_question_id, security_answer)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (nombre, apellido, email, contraseña_cifrada, security_question_id, security_answer))
            conexion.commit()

        return "Cuenta creada exitosamente.", 200
    except Exception as e:
        return f"Error al guardar los datos: {str(e)}", 500
    finally:
        if conexion:
            conexion.close()
