from flask import Flask, jsonify, request, Response, render_template
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
            "cre_id": place.get("cre_id"),
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
            "prices": [ ]
            #{
                    #"type": gas["@type"],
                    #"price": float(gas["#text"])
                #}
                #for gas in place["gas_price"]
        }

        for gas in place["gas_price"]:
            place_info["prices"].append({
                "type": gas["@type"],  # Accedemos al atributo type
                "price": float(gas["#text"])  # Obtenemos el valor del precio
            })

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

    
if __name__ == '__main__':
    app.run(debug=True)

