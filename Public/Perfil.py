from flask import Flask, render_template, session
import pyodbc
from conexion import obtener_conexion

app = Flask(__name__)
app.secret_key = "tu_secreto"



if __name__ == "__main__":
    app.run(debug=True)
