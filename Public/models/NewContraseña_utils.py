from conexion import obtener_conexion
from werkzeug.security import generate_password_hash
import re

def actualizar_contraseña(email, nueva_contraseña):

    conexion = None
    try:
        conexion = obtener_conexion()  # Usar la función de conexión de conexion.py
        if conexion is None:
            return "No se pudo establecer conexión con la base de datos.", 500
            
        with conexion.cursor() as cursor:
            query = "UPDATE usuarios SET contrasena = ? WHERE email = ?"
            cursor.execute(query,(generate_password_hash(nueva_contraseña), email))
            conexion.commit()
        return "Contraseña actualizada correctamente.", True

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        if conexion:
            conexion.close()
