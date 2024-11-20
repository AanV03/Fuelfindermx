from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash  # Para cifrar la contraseña
from conexion import obtener_conexion  # Importar la función de conexión

# Configuración de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route('/')
def modificar_datos():
    """Renderiza la página para modificar datos."""
    return render_template('modificar_datos.html')

@app.route('/guardar', methods=['POST'])
def guardar_datos():
    """Guarda los datos personales y del vehículo en la base de datos."""
    try:
        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')

        # Datos del vehículo (permitir varios vehículos)
        vehiculos = []
        for i in range(1, 6):  # Suponiendo que un usuario pueda registrar hasta 5 vehículos
            marca = request.form.get(f'marca_{i}')
            modelo = request.form.get(f'modelo_{i}')
            año = request.form.get(f'año_{i}')
            capacidad_tanque = request.form.get(f'capacidad_tanque_{i}')
            if marca and modelo and año and capacidad_tanque:  # Si hay datos para ese vehículo
                vehiculos.append({
                    'marca': marca,
                    'modelo': modelo,
                    'año': año,
                    'capacidad_tanque': capacidad_tanque
                })

        # Validar que los campos personales no estén vacíos
        if not nombre or not apellido or not email or not contraseña:
            flash('Todos los campos personales son obligatorios', 'danger')
            return redirect(url_for('modificar_datos'))

        # Cifrar la contraseña
        contraseña_cifrada = generate_password_hash(contraseña)

        # Obtener la conexión a la base de datos desde 'conexion.py'
        conn = obtener_conexion()

        # Verificar si la conexión fue exitosa
        if conn is None:
            flash('Error de conexión a la base de datos', 'danger')
            return redirect(url_for('modificar_datos'))

        # Usar un cursor con contexto para asegurar el cierre
        with conn.cursor() as cursor:
            # Actualizar los datos personales en la base de datos
            cursor.execute("""
                UPDATE Usuarios
                SET Nombre = ?, Apellido = ?, Email = ?, Contraseña = ?
                WHERE Email = ?
            """, (nombre, apellido, email, contraseña_cifrada, email))  # Asumimos que el correo es único

            # Actualizar los datos de los vehículos del usuario
            for vehiculo in vehiculos:
                cursor.execute("""
                    UPDATE Vehiculos
                    SET Marca = ?, Modelo = ?, Año = ?, Capacidad_Tanque = ?
                    WHERE UsuarioID = (SELECT UsuarioID FROM Usuarios WHERE Email = ?)
                    AND VehiculoID = ?
                """, (vehiculo['marca'], vehiculo['modelo'], vehiculo['año'], vehiculo['capacidad_tanque'], email, vehiculo['vehiculo_id']))  # Relacionamos con el UsuarioID y VehiculoID

            # Confirmar los cambios
            conn.commit()

        flash('Datos guardados correctamente', 'success')
        return redirect(url_for('modificar_datos'))

    except Exception as e:
        flash(f'Ocurrió un error: {e}', 'danger')
        return redirect(url_for('modificar_datos'))

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
