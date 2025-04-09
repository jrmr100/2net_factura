from utils.logger import logger
import os
import mariadb


conn = None
cursor = None
try:
    # Establecer la conexión a la base de datos
    conn = mariadb.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    # Crear un cursor para ejecutar consultas
    cursor = conn.cursor()

except mariadb.Error as e:
        print(f"Error al conectar o consultar la base de datos: {e}")

finally:
    # Cerrar el cursor y la conexión si están abiertos
    if cursor:
        cursor.close()
    if conn:
        conn.close()
