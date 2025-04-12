import mariadb
import os


try:
    conn = mariadb.connect(
        host=os.getenv("HOST_MW"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    # Crear un cursor para ejecutar consultas
    cursor = conn.cursor()
except mariadb.Error as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit(1)