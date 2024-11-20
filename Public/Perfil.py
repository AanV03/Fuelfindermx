from flask import Flask, render_template, session, flash, redirect, url_for
from conexion import obtener_conexion

app = Flask(__name__)
app.secret_key = "tu_secreto"

@app.route('/perfil')
def perfil():
    # Verifica si hay una sesión activa
    if 'user_id' not in session:
        flash("No estás logueado", 'danger')
        return redirect(url_for('iniciar_sesion'))  # Redirige a la página de inicio de sesión
    
    user_id = session['user_id']
    connection = obtener_conexion()

    try:
        with connection.cursor() as cursor:
            # Consulta para obtener los datos del usuario
            query_user = """
                SELECT Nombre, Apellido, Email, FechaCreacion
                FROM Usuarios
                WHERE UsuarioID = ?
            """
            cursor.execute(query_user, (user_id,))
            user_data = cursor.fetchone()  # Obtén los datos del usuario

            if user_data is None:
                flash("Usuario no encontrado", 'danger')
                return redirect(url_for('inicio'))  # Redirige a la página principal si no se encuentra el usuario

            # Consulta para obtener los datos del vehículo
            query_vehicle = """
                SELECT Marca, Modelo, Año, CapacidadTanque
                FROM Vehiculos
                WHERE UsuarioID = ?
            """
            cursor.execute(query_vehicle, (user_id,))
            vehicle_data = cursor.fetchall()  # Obtén los datos de todos los vehículos del usuario
    
    except Exception as e:
        flash(f"Ocurrió un error al cargar tu perfil: {e}", 'danger')
        return redirect(url_for('inicio'))  # Redirige en caso de error

    finally:
        connection.close()

    # Renderiza el HTML con los datos obtenidos
    return render_template('Perfil.html', user=user_data, vehicles=vehicle_data)

if __name__ == "__main__":
    app.run(debug=True)
