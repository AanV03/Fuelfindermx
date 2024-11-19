from flask import Flask, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from conexion import obtener_conexion  # Importar la función de conexión

app = Flask(__name__)

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        confirmar_contraseña = request.form.get('confirmar_contraseña')

        # Validar contraseñas
        if contraseña != confirmar_contraseña:
            return "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.", 400

        # Cifrar la contraseña
        contraseña_cifrada = generate_password_hash(contraseña)

        # Guardar los datos en la base de datos
        try:
            conexion = obtener_conexion()  # Usar la función del archivo conexion.py
            if conexion is None:
                return "No se pudo establecer conexión con la base de datos.", 500

            with conexion.cursor() as cursor:
                query = """
                INSERT INTO Usuarios (Nombre, Apellido, Email, Contraseña)
                VALUES (?, ?, ?, ?)
                """
                cursor.execute(query, (nombre, apellido, email, contraseña_cifrada))
                conexion.commit()

            return redirect(url_for('success'))
        except Exception as e:
            return f"Error al guardar los datos: {e}", 500
        finally:
            if conexion:
                conexion.close()

    return render_template('CreateAcc.html')

@app.route('/success')
def success():
    return "Cuenta creada exitosamente."

if __name__ == '__main__':
    app.run(debug=True)
