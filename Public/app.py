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
from models.NewContraseña_utils import actualizar_contraseña
import xml.etree.ElementTree as ET
import xmltodict, json, uuid
from flask_mail import Mail,Message 

app = Flask(__name__)
mail = Mail(app)
app.secret_key = "tu_secreto"


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
   if request.method == 'POST':
        # Obtener datos del formulario
        email = request.form.get('email')
        password = request.form.get('password')

        # Verificar si el usuario existe en la base de datos
        conn = get_db_connection()  # Tu función de conexión
        cursor = conn.cursor()

        try:
            # Consulta para obtener el hash de la contraseña basado en el email
            cursor.execute("SELECT password_hash FROM usuarios WHERE email = ?", (email,))
            result = cursor.fetchone()

            if result:
                stored_password_hash = result[0]  # Hash almacenado

                # Comparar la contraseña ingresada con el hash
                if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                    # Si es válida, guardar el inicio de sesión en la sesión
                    session['user'] = email
                    flash('Inicio de sesión exitoso', 'success')
                    return redirect(url_for('dashboard'))  # Cambia 'dashboard' por tu ruta principal
                else:
                    flash('Contraseña incorrecta', 'danger')
            else:
                flash('El correo no está registrado', 'danger')
        except Exception as e:
            print(f"Error al verificar el inicio de sesión: {e}")
            flash('Ocurrió un error. Inténtalo de nuevo.', 'danger')
        finally:
            conn.close()

    # Renderiza el formulario de inicio de sesión si es un GET o si hubo un error
        return render_template("IniciarSesion.html")


@app.route('/security-question/<int:security_question_id>', methods=['GET', 'POST'])
def security_question(security_question_id):
    # Código para manejar la lógica de la pregunta de seguridad.


@app.route("/NewContraseña", methods=["GET", "POST"])
def actualizar_contrasena_route():
    return render_template("NewContraseña.html")  # Renderizar el formulario de actualización


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
        
        # Obtener los valores de la pregunta de seguridad y la respuesta
        security_question_id = request.form.get("security_question_id")
        security_answer = request.form.get("security_answer")

        # Usar la función registrar_usuario para manejar la lógica de registro
        resultado = registrar_usuario(
            nombre, apellido, email, contraseña, confirmar_contraseña, 
            security_question_id, security_answer
        )
        print(resultado)

        # Si la cuenta se creó exitosamente, redirigir a la página de éxito
        if resultado == 200:
            return redirect(url_for("success"))

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
    if "user_id" not in session:
        flash("No estás logueado", "danger")
        return redirect(
            url_for("iniciar_sesion")
        )  # Redirige a la página de inicio de sesión

    user_id = session["user_id"]

    try:
        # Obtener los datos del usuario y los vehículos
        user_data = obtener_datos_usuario(user_id)
        if user_data is None:
            flash("Usuario no encontrado", "danger")
            return redirect(
                url_for("inicio")
            )  # Redirige a la página principal si no se encuentra el usuario

        vehicle_data = obtener_datos_vehiculos(user_id)

    except Exception as e:
        flash(f"Ocurrió un error al cargar tu perfil: {e}", "danger")
        return redirect(url_for("inicio"))  # Redirige en caso de error

    # Renderiza el HTML con los datos obtenidos
    return render_template("Perfil.html", user=user_data, vehicles=vehicle_data)


@app.route("/Reporte")
def Reporte():
    return render_template("Reporte.html")


if __name__ == "__main__":
    app.run(debug=True)
