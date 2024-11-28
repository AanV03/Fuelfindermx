from conexion import obtener_conexion
from werkzeug.security import generate_password_hash
import re

def nueva_contraseña(email, nueva_contraseña, confirmar_contraseña):
    """
    Lógica para actualizar la contraseña en la base de datos.
    Verifica que las contraseñas coincidan y luego las guarda.
    """
    
    if nueva_contraseña != confirmar_contraseña:
        return "Las contraseñas no coinciden.", False
    
    # Validación de la complejidad de la contraseña
    if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$', nueva_contraseña):
        return "La contraseña debe tener al menos 8 caracteres, incluyendo una letra y un número.", False

    try:
        # Establecer la conexión a la base de datos
        conexion = obtener_conexion()
        if conexion is None:
            return "No se pudo establecer conexión con la base de datos.", False

        with conexion.cursor() as cursor:
            query = "UPDATE usuarios SET contrasena = ? WHERE email = ?"
            cursor.execute(query, (generate_password_hash(nueva_contraseña), email))
            conexion.commit()

        return "Contraseña actualizada correctamente.", True

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return "Error al actualizar la contraseña.", False
    
    finally:
        if conexion:
            conexion.close()
