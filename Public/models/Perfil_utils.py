# perfil_utils.py
from conexion import obtener_conexion

def obtener_datos_usuario(email):
    """Obtiene los datos del usuario desde la base de datos utilizando su correo electrónico."""
    connection = obtener_conexion()
    try:
        with connection.cursor() as cursor:
            query_user = """
                SELECT UsuarioID, Nombre, Apellido, Email, FechaCreacion 
                FROM Usuarios 
                WHERE Email = ?
            """
            cursor.execute(query_user, (email,))
            return cursor.fetchone()  # Devuelve los datos del usuario
    except Exception as e:
        raise Exception(f"Error al obtener los datos del usuario: {e}")
    finally:
        connection.close()


def obtener_datos_vehiculos(email):
    """Obtiene los datos de los vehículos del usuario utilizando su correo electrónico."""
    connection = obtener_conexion()
    try:
        with connection.cursor() as cursor:
            query_vehicle = """
                SELECT v.Marca, v.Modelo, v.Año, v.CapacidadTanque 
                FROM Vehiculos v
                INNER JOIN Usuarios u ON v.UsuarioID = u.UsuarioID
                WHERE u.Email = ?
            """
            cursor.execute(query_vehicle, (email,))
            return cursor.fetchall()  # Devuelve los datos de los vehículos
    except Exception as e:
        raise Exception(f"Error al obtener los datos del vehículo: {e}")
    finally:
        connection.close()
