# conexion.py
import pyodbc

# metele los datos de la base de datos porfavor Bryan.
def obtener_conexion():
    servidor = 'nombre_servidor.database.windows.net'
    base_datos = 'tu_base_de_datos'
    usuario = 'tu_usuario'
    contrasena = 'tu_contraseña'
    driver = 'ODBC Driver 17 for SQL Server'

    try:
        conexion = pyodbc.connect(
            f'DRIVER={driver};SERVER={servidor};DATABASE={base_datos};UID={usuario};PWD={contrasena}'
        )
        return conexion
    except Exception as e:
        print("Error al conectar:", e)
        raise

""" Se supone que hay que implementar esto en app.py para lo de conexion de base de datos

# app.py
from flask import Flask, jsonify, request, Response
import xml.etree.ElementTree as ET
import xmltodict
import json
from conexion import obtener_conexion  # Importa la función de conexión

app = Flask(__name__)

# Ruta que convierte XML a diccionario
def xml_data():
    with open("lugares.xml", "r") as archivo:
        xml_data = archivo.read()
        diccionario = xmltodict.parse(xml_data)
    return diccionario

# Ruta que devuelve la información de gasolineras
@app.route('/api/ubicaciones', methods=['GET'])
def gasolineras():
    formato = request.args.get('formato', 'json')
    data_dict = xml_data()

    if formato == 'json':
        return jsonify(data_dict)
    
    elif formato == 'xml':
        xml_datax = ET.Element("places")

        for place in data_dict['places']['place']:
            place_elem = ET.SubElement(xml_datax, "place")
            for key, value in place.items():
                elem = ET.SubElement(place_elem, key)
                elem.text = str(value)
        
        xml_string = ET.tostring(xml_datax, encoding='utf-8')
        return Response(xml_string, mimetype='application/xml')
    else:
        return jsonify({"error": "Formato no soportado"}), 400

# Ruta que devuelve los precios de las gasolineras
def xml_precios():
    with open("prices.xml", "r") as prices:
        xml_precios = prices.read()
        diccionario = xmltodict.parse(xml_precios)
    return diccionario

@app.route('/api/precios', methods=['GET'])
def precios():
    formatos = request.args.get('formato', 'json')
    data_dicts = xml_precios()

    for precio in data_dicts['places']['place']:
        print(precio)

    return jsonify(data_dicts)

# Nueva ruta para obtener datos desde SQL Server
@app.route('/api/reporte', methods=['GET'])
def reporte():
    formato = request.args.get('formato', 'json')

    try:
        # Conectar a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Realizar una consulta (ejemplo)
        cursor.execute("SELECT TOP 10 * FROM tu_tabla")
        resultados = cursor.fetchall()

        # Preparar los datos para la respuesta
        datos = []
        for fila in resultados:
            datos.append({
                'columna1': fila[0],  # Cambia según tu tabla
                'columna2': fila[1],  # Cambia según tu tabla
                # Agrega más columnas según sea necesario
            })

        cursor.close()
        conexion.close()

        if formato == 'json':
            return jsonify(datos)

        elif formato == 'xml':
            # Generar respuesta en formato XML si se solicita
            xml_datax = ET.Element("reporte")
            for item in datos:
                item_elem = ET.SubElement(xml_datax, "item")
                for key, value in item.items():
                    elem = ET.SubElement(item_elem, key)
                    elem.text = str(value)

            xml_string = ET.tostring(xml_datax, encoding='utf-8')
            return Response(xml_string, mimetype='application/xml')

        else:
            return jsonify({"error": "Formato no soportado"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

"""