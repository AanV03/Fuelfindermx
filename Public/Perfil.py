from flask import Flask, render_template, session
import pyodbc
from conexion import obtener_conexion

app = Flask(__name__)
app.secret_key = "tu_secreto"

@app.route('/perfil')
def perfil():
    # Verifica si hay una sesión activa
    if 'user_id' not in session:
        return "No estás logueado", 403
    
    user_id = session['user_id']
    connection = obtener_conexion()

    try:
        with connection.cursor() as cursor:
            # Consulta para obtener los datos del usuario
            query_user = """
                SELECT Nombre, Apellido, Email, FechaCreacion
                FROM Usuarios
                WHERE id = ?
            """
            cursor.execute(query_user, (user_id,))
            user_data = cursor.fetchone()  # Obtén los datos del usuario

            # Consulta para obtener los datos del vehículo
            query_vehicle = """
                SELECT Marca, Modelo, Anio, CapacidadTanque
                FROM Vehiculos
                WHERE user_id = ?
            """
            cursor.execute(query_vehicle, (user_id,))
            vehicle_data = cursor.fetchone()  # Obtén los datos del vehículo
    
    finally:
        connection.close()
    
    # Renderiza el HTML con los datos obtenidos
    return render_template('Perfil.html', user=user_data, vehicle=vehicle_data)

if __name__ == "__main__":
    app.run(debug=True)
