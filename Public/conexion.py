import pyodbc

# Configuración de conexión con Azure SQL Database
server = 'mi-servidor.database.windows.net'
database = 'nombre_base_datos'
username = 'mi_usuario'
password = 'mi_contraseña'
driver = '{ODBC Driver 18 for SQL Server}'
encrypt = 'yes'
trust_server_certificate = 'yes'

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