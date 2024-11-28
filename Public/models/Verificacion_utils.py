import bcrypt
from conexion import obtener_conexion

def verificar_correo(correo):
    """
    Verifica si el correo existe en la base de datos.
    Retorna True si el correo existe, de lo contrario False.
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = "SELECT COUNT(*) FROM usuarios WHERE Email = '" + correo +"'"
            cursor.execute(query)
            #resultado = cursor.fetchone()
            return True  # Devuelve True si el correo existe
    except Exception as e:
        print(f"Error al verificar el correo: {e}")
        return False
    finally:
        conexion.close()
