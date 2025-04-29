# Cargo las variables de entorno previo a mis modulos
from dotenv import load_dotenv
import os
app_dir = os.path.join(os.path.dirname(__file__))
load_dotenv(".env")

from utils.connect_db import conn, cursor
from utils.db import buscar_factura, nueva_factura, descripcion_factura, saldo_favor
from datetime import date, datetime, timedelta
from utils.logger import logger
from utils.csv_files import crear_csv, leer_csv, agregar_csv



today = date.today()
un_dia = timedelta(days=1)

#Datos de prueba
# table_name = "facturas"
# id_cliente = 9177
fecha_inicio = date(2025, 4, 2)
fecha_fin = date(2025, 4, 29)
fecha_max = date(2025, 4, 30)
vencimiento = date(2025, 4, 30)

# Crear CSV para almacenar salidas
resultado_csv = crear_csv(today)
for resultado in resultado_csv:
    print("Resultado - " + str(resultado))
    logger.info("Procesando creacion de archivos: " + str(resultado))


# Leer lista de usuarios activos de MW
usuarios_mw = leer_csv(os.getenv("ARCHIVO_CSV"))
logger.info("Procesando archivo de usuarios activos: " + str(len(usuarios_mw)))
for usuario in usuarios_mw[1:]:
    id_cliente = usuario[1]
    cedula = usuario[2]
    nombre = f'"{usuario[3]}"'
    correo = usuario[14]
    plan = usuario[6]

    ##### BUSCO LA FECHA DE EMISION DE LA ULTIMA FACTURA DEL CLIENTE ###########
    table_name = "facturas"
    emision_last_factura = buscar_factura(table_name, id_cliente, cedula, nombre, today)
    factura = False
    if emision_last_factura[0] == "exito":
        if fecha_inicio <= emision_last_factura[1][0] <= fecha_fin:
            factura = True
        else:
            causa = "Fecha de emision fuera de rango (2 al 29 de Abril)"
            data_csv = str(id_cliente) + "," + cedula + "," + nombre + "," + str(
                emision_last_factura[1][0]) + "," + causa + "\n"
            agregar_csv(os.getenv("CSV_NOPROCESADOS") + "-" + str(today) + ".csv", data_csv)
            logger.error(f"Cliente: {str(id_cliente)} - nombre: {nombre} - {causa}")
            print(f"ERROR - Cliente: {str(id_cliente)} - nombre: {nombre} - Fecha ultima factura: {str(emision_last_factura[1][0])} - {causa}")
            continue


    if len(cedula) > 8:
        causa = "Cedula es mayor a 8 digitos"
        data_csv = str(id_cliente) + "," + cedula + "," + nombre + "," + str(
            emision_last_factura[1][0]) + "," + causa + "\n"
        agregar_csv(os.getenv("CSV_NOPROCESADOS") + "-" + str(today) + ".csv", data_csv)
        logger.error(f"Cliente: {str(id_cliente)} - nombre: {nombre} - {causa}")
        print(f"ERROR - Cliente: {str(id_cliente)} - nombre: {nombre} - {causa}")
        continue
    # Filtro los que son convenios
    if "convenio" in nombre.lower() or "convenio" in plan.lower():
        causa = "Convenio"
        data_csv = str(id_cliente) + "," + cedula + "," + nombre + "," + str(
            emision_last_factura[1][0]) + "," + causa + "\n"
        agregar_csv(os.getenv("CSV_NOPROCESADOS") + "-" + str(today) + ".csv", data_csv)
        logger.error(f"Cliente: {str(id_cliente)} - nombre: {nombre} - {causa}")
        print(f"ERROR - Cliente: {str(id_cliente)} - nombre: {nombre} - {causa}")
        continue



    # Solo si la factura existe y esta en la fecha correcta
    if factura is True:

        ############## AGREGO SALDO AL CLIENTE SEGUN SU FACTURA ###############
        saldo_agregado = saldo_favor(emision_last_factura[1][0], today, emision_last_factura[1][2], id_cliente, cedula, nombre, fecha_inicio)

# Cierro la conexion con la base de datos
if cursor:
    cursor.close()
if conn:
    conn.close()


# TODO: Cuales usuarios procesar? solo activos, los suspendidos tambien debe agregarse la factura cierto, si pagan se activaran? R.- Suspendidos se deben poner disable
# TODO: Que hacer con el campo legal (nro fiscal) en la facturas (MW2 no tiene nro de control en factura)

# TODO: Obtener lista de clientes automaticas
# TODO: Revisar logger y print
# TODO: Limpiar registros viudos de tabla facturaitems



