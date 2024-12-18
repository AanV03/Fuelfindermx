from flask import (
    Flask,
    jsonify,
    request,
    Response,
    render_template,
    redirect,
    url_for,
    session,
    flash,
)
from werkzeug.security import generate_password_hash
from models.Perfil_utils import (
    obtener_datos_usuario,
    obtener_datos_vehiculos,
)  # Importar las funciones
from models.Registro_utils import (
    registrar_usuario,
)  # Importar la función para registrar usuarios
from models.Verificacion_utils import verificar_correo
from models.NewContraseña_utils import nueva_contraseña
import xml.etree.ElementTree as ET
import xmltodict, json, uuid
from flask_mail import Mail,Message 
import bcrypt
from conexion import obtener_conexion

app = Flask(__name__)
mail = Mail(app)


@app.route("/")
def inicioandindex():
    return render_template("inicio.html")

@app.route("/Inicio")
def inicio():
    return render_template("inicio.html")

@app.route("/Mapa")
def index():
    return render_template("mapa.html")


# Funcion que convierte el XML a un diccionario en Python
def xml_data():
    with open("lugares.xml", "r") as archivo:
        xml_data = archivo.read()
        diccionario = xmltodict.parse(xml_data)
    return diccionario


# Extrae la informacion y la muestra. Lugares
@app.route("/api/ubicaciones", methods=["GET"])
def gasolineras():
    formato = request.args.get("formato", "json")
    data_dict = xml_data()

    lugares = []
    for place in data_dict["places"]["place"]:
        lugares.append(
            {
                "name": place.get("name"),
                "place_id": place.get("@place_id"),
                "x": float(place.get("x", 0)),
                "y": float(place.get("y", 0)),
            }
        )

    if formato == "json":
        return jsonify(lugares)
    else:
        return jsonify({"error": "Formato no soportado"}), 400


# Extrae los precios usando el id de los lugares
def xml_precios():
    with open("precios_actualizado.xml", "r") as archivo:
        xml_data = archivo.read()
        diccionario = xmltodict.parse(xml_data)
    return diccionario


@app.route("/api/precios", methods=["GET"])
def precios():
    formato = request.args.get("formato", "json")
    data_dict = xml_precios()

    # Construir la respuesta
    precios_data = []
    for place in data_dict["places"]["place"]:
        place_info = {
            "place_id": place["@place_id"],
            "prices": [
                {
                    "type": gas.get("@type"),  # Accedemos al atributo type
                    "price": float(gas.get("#text", 0)),  # Obtenemos el precio
                }
                for gas in place.get("gas_price", [])  # Iteramos sobre gas_price
            ],
        }

        precios_data.append(place_info)

    # Respuesta en JSON
    if formato == "json":
        return jsonify(precios_data)

    # Respuesta en XML
    elif formato == "xml":
        root = ET.Element("places")
        for place in precios_data:
            place_elem = ET.SubElement(root, "place", {"place_id": place["place_id"]})
            for price in place["prices"]:
                price_elem = ET.SubElement(
                    place_elem, "gas_price", {"type": price["type"]}
                )
                price_elem.text = str(price["price"])

        xml_string = ET.tostring(root, encoding="utf-8")
        return Response(xml_string, mimetype="application/xml")

    else:
        return jsonify({"error": "Formato no soportado"}), 400


@app.route("/api/precios-ubicaciones", methods=["GET"])
def precios_ubicaciones():
    formato = request.args.get("formato", "json")

    # Llamar directamente a las funciones que procesan los datos
    ubicaciones = gasolineras().json  # Utiliza la función del endpoint
    precios_data = xml_precios()  # Procesa directamente el XML

    # Extraer precios desde el XML procesado
    precios = []
    for place in precios_data["places"]["place"]:
        place_info = {
            "place_id": place["@place_id"],
            "prices": [
                {"type": gas.get("@type"), "price": float(gas.get("#text", 0))}
                for gas in place.get("gas_price", [])
            ],
        }
        precios.append(place_info)

    # Combinar los datos por place_id
    estaciones = []
    for ubicacion in ubicaciones:
        precios_relacionados = next(
            (p for p in precios if p["place_id"] == ubicacion["place_id"]), None
        )
        if precios_relacionados:
            estaciones.append({**ubicacion, "prices": precios_relacionados["prices"]})

    # Calcular precio más bajo y más alto
    mas_bajo = min(
        estaciones,
        key=lambda x: next(
            (p["price"] for p in x["prices"] if p["type"] == "Regular"), float("inf")
        ),
    )
    mas_alto = max(
        estaciones,
        key=lambda x: next(
            (p["price"] for p in x["prices"] if p["type"] == "Regular"), float("-inf")
        ),
    )

    # Construir respuesta
    resultado = {"estaciones": estaciones, "mas_bajo": mas_bajo, "mas_alto": mas_alto}

    # Respuesta en JSON o XML
    if formato == "json":
        return jsonify(resultado)
    else:
        return jsonify({"error": "Formato no soportado"}), 400


@app.route("/IniciarSesion", methods=['GET','POST'])
def iniciar_sesion():
    if request.method == "POST":
        # Obtener los datos del formulario
        email = request.form.get("email")
        password = request.form.get("contraseña")

        # Verificar campos vacíos
        if not email or not password:
            flash("Por favor, completa todos los campos", "warning")
            return render_template("IniciarSesion.html")

        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            # Consultar la contraseña almacenada en la base de datos
            cursor.execute("SELECT UsuarioID, contraseña FROM usuarios WHERE email = ?", (email,))
            result = cursor.fetchone()

            if result:
                user_id, stored_password_hash = result

                # Verificar contraseña
                if bcrypt.checkpw(password.encode("utf-8"), stored_password_hash.encode("utf-8")):
                    session["user"] = user_id #Se guarda la sesion
                    flash("Inicio de sesión exitoso", "success")
                    print('si hubo conexion papu')
                    return redirect(url_for("inicio"))  # Redirige al perfil
                else:
                    flash("Contraseña incorrecta", "danger")
                    print('mamaste papu sin contra')
            else:
                flash("El correo no está registrado", "danger")
                print('mamaste papu')

        except Exception as e:
            print(f"Error al verificar el inicio de sesión: {e}")
            flash("Ocurrió un error. Inténtalo de nuevo.", "danger")
        finally:
            conexion.close()

        return render_template("IniciarSesion.html")  # Renderizar en caso de error

    # Si el método es GET, renderiza la página de inicio de sesión
    return render_template("IniciarSesion.html")


@app.route("/CerrarSesion")
def cerrar_sesion():
    session.pop('user', None)
    flash('Sesion cerrada exitosamente', 'success')
    return redirect(url_for('inicio'))


app.secret_key='hello'
app.config['SECRET_KEY'] = 'hello'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'fuelfindermx@gmail.com'  # Cambia por tu correo
app.config['MAIL_PASSWORD'] = 'hjvf gqca laih svsm'  # Cambia por tu contraseña

@app.route('/send_email', methods=['GET'])
def send_email(email):
    msg_title='prueba de correo'
    sender = 'noreply@app.com'
    msg = Message(msg_title, sender=sender, recipients=[email])
    msg_body = 'Este es el cuerpo del mensaje'
    data = {
        'app_name':'Nombre de la aplicación que envia el email',
        'title': msg_title,
        'body':msg_body
    } 
    try:
        mail.send(msg)
        return 'mensaje enviado'
    except Exception as ex:
        print(ex)
        return f'Mensaje no enviado {ex}'


@app.route('/ConfirmarEmail', methods=['GET', 'POST'])
def recuperar_contrasena():
    """
    Ruta para manejar la solicitud de recuperación de contraseña.
    """
    if request.method == 'POST':
        email = request.form.get('email')  # Obtiene el correo ingresado en el formulario
        
        # Verificar si el correo existe en la base de datos
        if verificar_correo(email):
            # Enviar el correo si el usuario existe
            if send_email(email):
                print('a wiwi')
                return jsonify({'success': True, 'message': 'Correo enviado exitosamente.'})
            else:
                print('pipipi')
                return jsonify({'success': False, 'message': 'Error al enviar el correo.'}), 500
        else:
            print('pipi')
            return jsonify({'success': False, 'message': 'El correo no está registrado.'}), 404
            
    
    # Si es GET, muestra el formulario
    return render_template('ConfirmarEmail.html')


@app.route('/NuevaContraseña', methods=['GET', 'POST'])
def restablecer_contrasena():
    """
    Ruta para manejar el restablecimiento de contraseña.
    """
    if request.method == 'POST':
        email = request.form.get('email')  # Puedes recibir este dato como parte del formulario
        nueva_contrasena = request.form.get('nueva_contraseña')
        confirmar_contrasena = request.form.get('confirmar_contraseña')

        # Llamar a la función de actualización de contraseña
        mensaje, exito = nueva_contraseña(email, nueva_contrasena, confirmar_contrasena)
        
        if exito:
            return jsonify({'success': True, 'message': mensaje})
        else:
            return jsonify({'success': False, 'message': mensaje}), 400

    return render_template('NewContraseña.html')


@app.route("/ConfToken")
def Conf_token():
    return render_template("ConfToken.html")


@app.route("/CreateAcc", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        print("Solicitud POST recibida")

        # Obtener datos del formulario
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        email = request.form.get("email")
        contraseña = request.form.get("contraseña")
        confirmar_contraseña = request.form.get("confirmar-contraseña")
        
        # Usar la función registrar_usuario para manejar la lógica de registro
        resultado = registrar_usuario(
            nombre, apellido, email, contraseña, confirmar_contraseña
        )
        print(resultado)

        # Si la cuenta se creó exitosamente, redirigir a la página de éxito
        if resultado == 200:
            return redirect(url_for("inicio"))

        # Si hubo un error, mostrar el mensaje de error
        flash(resultado, "danger")
        return render_template("CreateAcc.html")

    else:
        print("Solicitud GET recibida")
        print("no entre ", request.form.get("nombre"))

    return render_template("CreateAcc.html")


@app.route("/success")
def success():
    return render_template("inicio.html")


@app.route("/ModDatos")
def Mod_Datos():
    return render_template("ModDatos.html")


# funcion para obtener datos de la base de datos para perfil
@app.route("/Perfil")
def perfil():
# Verifica si hay una sesión activa
    user_id = session.get("user")
    if not user_id:
        flash("No estás logueado", "danger")
        return redirect(url_for("iniciar_sesion"))

    try:
        user_id = int(user_id)  # Asegúrate de que sea un entero
    except ValueError:
        flash("El ID del usuario en la sesión no es válido.", "danger")
        return redirect(url_for("iniciar_sesion"))

    # Obtener los datos del usuario y los vehículos
    try:
        user_data = obtener_datos_usuario(user_id)
        if not user_data:
            flash("Usuario no encontrado", "danger")
            return redirect(url_for("inicio"))

        
    except Exception as e:
        flash("Ocurrió un error al cargar tu perfil.", "danger")
        app.logger.error(f"Error al cargar perfil: {e}")
        return redirect(url_for("inicio"))

    return render_template("Perfil.html", user=user_data)

@app.route("/Reporte")
def Reporte():
    return render_template("Reporte.html")


if __name__ == "__main__":
    app.run(debug=True)
