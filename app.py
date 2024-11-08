from flask import Flask, jsonify, request, Response
import xml.etree.ElementTree as ET
import xmltodict
import json

app=Flask(__name__)

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

    if formato == 'json':
        return jsonify(data_dict)
    
    elif formato == 'xml':
        xml_datax   = ET.Element("places")

        for place in data_dict['places']['place']:
            place_elem = ET.SubElement(xml_dicc,"place")
            for key, value in place.items():
                elem = ET.SubElement(place_elem, key)
                elem.text = str(value)
        
        xml_string = ET.tostring(xml_data, encoding='utf-8')
        return Response(xml_string, mimetype='application/xml')
    else:
        return jsonify({"error": "Formato no soportado"}), 400
    
#Extrae los precios usando el id de los lugares
def xml_precios():
    with open("prices.xml","r") as prices:
        xml_precios = prices.read()
        diccionario = xmltodict.parse(xml_precios)
    return diccionario

@app.route('/api/precios', methods=['GET'])
def precios():
    formatos = request.args.get('formato','json')
    data_dicts = xml_precios()

    for precio in data_dicts['places']['place']:
        print(precio)

    return jsonify(data_dicts)

    
if __name__ == '__main__':
    app.run(debug=True)

