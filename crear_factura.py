# Cargo las variables de entorno previo a mis modulos
from dotenv import load_dotenv
import os
app_dir = os.path.join(os.path.dirname(__file__))
load_dotenv(".env")

from utils.logger import logger
from utils.leer_csv import leer_csv
from utils.db import leer_tabla
from datetime import date

sql_string_facturas = "SELECT * FROM facturas;"
leer_facturas = leer_tabla(sql_string_facturas)






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
