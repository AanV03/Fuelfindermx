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
from models.Correo_utils import enviar_correo
import xml.etree.ElementTree as ET
import xmltodict, json, uuid


app = Flask(__name__)
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


@app.route("/IniciarSesion")
def iniciar_sesion():
    return render_template("IniciarSesion.html")


tokens = {}

@app.route("/ConfEmail", methods=["GET", "POST"])
def solicitar_actualizacion_contrasena():
    if request.method == "POST":
        email = request.form.get("email")
        token = str(uuid.uuid4())  # Generar un token único
        tokens[token] = email  # Almacenar el token y el email

        # Enviar correo al usuario
        enviar_correo(email, token)
        flash(
            "Se ha enviado un enlace a tu correo para actualizar la contraseña.",
            "success",
        )
        return redirect(url_for("iniciar_sesion"))

    return render_template("ConfEmail.html")


@app.route("/NewContraseña", methods=["GET", "POST"])
def actualizar_contrasena_route():
    token = request.args.get("token")
    if request.method == "POST":
        nueva_contraseña = request.form.get("nueva_contraseña")
        email = tokens.get(token)  # Obtener el email usando el token

        if email and actualizar_contraseña(email, nueva_contraseña):
            flash("Contraseña actualizada exitosamente.", "success")
            del tokens[token]  # Eliminar el token después de usarlo
            return redirect(url_for("iniciarSesion"))
        else:
            flash("Ocurrió un error al actualizar la contraseña.", "danger")
            return redirect(url_for("ConfEmail"))

    return render_template(
        "NewContraseña.html", token=token
    )  # Renderizar el formulario de actualización


@app.route("/ConfToken")
def Conf_token():
    return render_template("ConfToken.html")


@app.route("/CreateAcc", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        print("Solicitud POST recibida")
        # Obtener datos del formulario
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")  # Incluimos el apellido
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
    return "Cuenta creada exitosamente."


@app.route("/Gasolineras")
def Gasolineras():
    return render_template("Gasolineras.html")


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
