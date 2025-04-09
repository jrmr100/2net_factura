from utils.logger import logger
import os
import mariadb


conn = None
cursor = None
try:
    # Establecer la conexión a la base de datos
    conn = mariadb.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
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

def leer_tabla(sql_string):
    # Ejecutar la consulta SELECT para obtener todos los registros de la tabla
    print(sql_string)
    cursor.execute(sql_string)

    # Obtener todos los resultados de la consulta
    resultados = cursor.fetchall()
    # Imprimir los resultados
    if resultados:
        print("Registros en la tabla facturas:")
        # Obtener los nombres de las columnas (opcional)
        column_names = [i[0] for i in cursor.description]
        print(f"Columnas: {', '.join(column_names)}")
        for fila in resultados:
            print(fila)
    else:
        print(f"La tabla facturas está vacía.")