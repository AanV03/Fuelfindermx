from flask import Flask
import pyodbc

app=Flask(__name__)

# Configuración de conexión con Azure SQL Database
server = 'mi-servidor.database.windows.net'
database = 'fuelfindermx.database.windows.net'
username = 'fuelfinderadmin'
password = 'Automovil21'
driver = '{ODBC Driver 17 for SQL Server}'
encrypt = 'yes'
trust_server_certificate = 'yes'

@app.route("/sql")
def obtener_conexion():
    """Establece conexión segura con Azure SQL Database."""
    try:
        conexion = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt={encrypt};TrustServerCertificate={trust_server_certificate}'
        )
        print("Conexión exitosa a Azure SQL Database.")
        return conexion
    except Exception as e:
        print("Error al conectar con Azure SQL Database:", e)
        return None

    
if __name__ == '__main__':
    app.run(debug=True)