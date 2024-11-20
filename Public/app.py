from flask import Flask, jsonify, request, Response, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from conexion import obtener_conexion  # Importar la función de conexión
import xml.etree.ElementTree as ET
import xmltodict
import json

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('mapa.html')

#Funcion que convierte el XML a un diccionario en Python
def xml_data():
    with open("lugares.xml" , "r") as archivo:
        xml_data = archivo.read()
        diccionario = xmltodict.parse(xml_data)
    return diccionario



#Extrae la informacion y la muestra. Lugares
@app.route('/api/ubicaciones', methods=['GET'])
def gasolineras():
    formato = request.args.get('formato', 'json')
    data_dict = xml_data()

    lugares = []
    for place in data_dict['places']['place']:
        lugares.append({
            "name": place.get("name"),
            "place_id": place.get("@place_id"),
            "x": float(place.get("x", 0)),
            "y": float(place.get("y", 0))
        })

    if formato == 'json':
        return jsonify(lugares)
    else:
        return jsonify({"error": "Formato no soportado"}), 400
    
#Extrae los precios usando el id de los lugares
def xml_precios():
    with open("precios_actualizado.xml", "r") as archivo:
        xml_data = archivo.read()
        diccionario = xmltodict.parse(xml_data)
    return diccionario

@app.route('/api/precios', methods=['GET'])
def precios():
    formato = request.args.get('formato', 'json')
    data_dict = xml_precios()

    # Construir la respuesta
    precios_data = []
    for place in data_dict['places']['place']:
        place_info = {
            "place_id": place["@place_id"],
            "prices": [
                {
                    "type": gas.get("@type"),       # Accedemos al atributo type
                    "price": float(gas.get("#text", 0))  # Obtenemos el precio
                }
                for gas in place.get("gas_price", [])  # Iteramos sobre gas_price
            ]
        }

        precios_data.append(place_info)

    # Respuesta en JSON
    if formato == 'json':
        return jsonify(precios_data)

    # Respuesta en XML
    elif formato == 'xml':
        root = ET.Element("places")
        for place in precios_data:
            place_elem = ET.SubElement(root, "place", {"place_id": place["place_id"]})
            for price in place["prices"]:
                price_elem = ET.SubElement(place_elem, "gas_price", {"type": price["type"]})
                price_elem.text = str(price["price"])
        
        xml_string = ET.tostring(root, encoding='utf-8')
        return Response(xml_string, mimetype='application/xml')

    else:
        return jsonify({"error": "Formato no soportado"}), 400

@app.route('/IniciarSesion')
def iniciar_sesion():
    return render_template('IniciarSesion.html')







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






    
if __name__ == '__main__':
    app.run(debug=True)

