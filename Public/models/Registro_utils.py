from conexion import obtener_conexion
#from werkzeug.security import generate_password_hash
import bcrypt
import re

def registrar_usuario(nombre, apellido, email, contraseña, confirmar_contraseña):
    "Función para registrar un nuevo usuario en la base de datos."
    
    # Validar contraseñas
    if contraseña != confirmar_contraseña:
        return "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.", 400

    # Cifrar la contraseña
    salt = bcrypt.gensalt()
    contraseña_cifrada = bcrypt.hashpw(contraseña.encode('utf-8'), salt).decode('utf-8')

    print('pase por aqui y si falle 22')
    
    # Conectar a la base de datos y guardar los datos
    conexion = None
    try:
        conexion = obtener_conexion()  # Usar la función de conexión de conexion.py
        if conexion is None:
            return "No se pudo establecer conexión con la base de datos.", 500
            
        with conexion.cursor() as cursor:
            # Insertar el usuario junto con la pregunta de seguridad y la respuesta
            query = """
            INSERT INTO dbo.Usuarios (Nombre, Apellido, Email, Contraseña)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (nombre, apellido,email, contraseña_cifrada))
            conexion.commit()

        return "Cuenta creada exitosamente.", 200
    except Exception as e:
        return f"Error al guardar los datos: {str(e)}", 500
    finally:
        if conexion:
            conexion.close()
