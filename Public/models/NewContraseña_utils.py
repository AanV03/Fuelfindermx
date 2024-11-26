import sqlite3
from werkzeug.security import generate_password_hash

def obtener_conexion():
    # Aquí debes implementar la lógica para conectarte a tu base de datos
    return sqlite3.connect('tu_base_de_datos.db')

def actualizar_contraseña(email, nueva_contraseña):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        # Actualizar la contraseña en la base de datos
        cursor.execute('UPDATE usuarios SET contrasena = ? WHERE email = ?', 
                       (generate_password_hash(nueva_contraseña), email))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()