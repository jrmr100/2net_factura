# Cargo las variables de entorno previo a mis modulos
from dotenv import load_dotenv
import os
app_dir = os.path.join(os.path.dirname(__file__))
load_dotenv(".env")

from utils.logger import logger
from utils.leer_csv import leer_csv
from utils.db import cursor
from datetime import date


# Ejecutar la consulta SELECT para obtener todos los registros de la tabla
cursor.execute("SELECT * FROM facturas")

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



"""
# Leer lista de usuarios activos de MW
usuarios_mw = leer_csv(os.getenv("ARCHIVO_CSV"))
logger.info("Procesando archivo de usuarios activos: " + str(len(usuarios_mw)))

cabecera_csv_salida = "ID, CEDULA, NOMBRE, CORREO, FECHA_VENCIMIENTO\n"

for usuario in usuarios_mw[1:]:
    id = usuario[1]
    cedula = usuario[2]
    nombre = usuario[3]
    correo = usuario[14]

    logger.info("\n####### PROCESANDO USUARIO #############:\n " + str(id) + " - " + str(cedula) + " - " + str(correo))
    print("####### PROCESANDO USUARIO #############:\n " + str(id) + " - " + str(cedula) + " - " + str(correo))

    # Busco la ultima factura
    ultima_factura = buscar_factura(id)
    fecha_vencimiento = ultima_factura[1]["facturas"][0]["vencimiento"]

    ###### Creo factura nueva a partir de fecha de vencimiento##########

    # le sumo un dia a la fecha de vencimiento
    fecha_inicio_factura = (datetime.strptime(fecha_vencimiento, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
    crear_factura = crear_factura(id, fecha_vencimiento)
"""
