import pyodbc

# Datos de conexión (puedes considerar cargarlos desde un archivo .env)
server = 'fuelfindermx.database.windows.net'
database = 'fuelfinder'
PORT = '1433'
username = 'fuelfinderadmin'
password = 'Automovil21'
driver = '{ODBC Driver 17 for SQL Server}'
encrypt = 'yes'
trust_server_certificate = 'yes'

def obtener_conexion():
    """Establece conexión segura con Azure SQL Database."""
    try:
        conexion = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};PORT={PORT};DATABASE={database};UID={username};PWD={password};Encrypt={encrypt};TrustServerCertificate={trust_server_certificate}'
        )
        print("Conexión exitosa a Azure SQL Database.")
        return conexion
    except Exception as e:
        print("Error al conectar con Azure SQL Database:", e)
        return None
