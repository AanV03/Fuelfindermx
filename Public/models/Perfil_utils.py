# perfil_utils.py
from conexion import obtener_conexion

def obtener_datos_usuario(user_id):
    """Obtiene los datos del usuario desde la base de datos."""
    connection = obtener_conexion()
    try:
        with connection.cursor() as cursor:
            query_user = """
                SELECT Nombre, Apellido, Email, FechaCreacion
                FROM Usuarios
                WHERE UsuarioID = ?
            """
            cursor.execute(query_user, (user_id,))
            return cursor.fetchone()  # Devuelve los datos del usuario
    except Exception as e:
        raise Exception(f"Error al obtener los datos del usuario: {e}")
    finally:
        connection.close()

def obtener_datos_vehiculos(user_id):
    """Obtiene los datos de los vehículos del usuario desde la base de datos."""
    connection = obtener_conexion()
    try:
        with connection.cursor() as cursor:
            query_vehicle = """
                SELECT Marca, Modelo, Año, CapacidadTanque
                FROM Vehiculos
                WHERE UsuarioID = ?
            """
            cursor.execute(query_vehicle, (user_id,))
            return cursor.fetchall()  # Devuelve los datos de los vehículos
    except Exception as e:
        raise Exception(f"Error al obtener los datos del vehículo: {e}")
    finally:
        connection.close()
