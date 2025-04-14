# Cargo las variables de entorno previo a mis modulos
from dotenv import load_dotenv
import os
app_dir = os.path.join(os.path.dirname(__file__))
load_dotenv(".env")

from utils.connect_db import conn, cursor
from utils.db import buscar_factura, nueva_factura, descripcion_factura
from datetime import date, datetime, timedelta
from utils.logger import logger
from utils.csv_files import crear_csv, leer_csv, agregar_csv



today = date.today()
un_dia = timedelta(days=1)

#Datos de prueba
# table_name = "facturas"
# id_cliente = 9177
fecha_max = date(2025, 3, 30)
vencimiento = date(2025, 4, 30)

# Crear CSV para almacenar salidas
resultado_csv = crear_csv()
for resultado in resultado_csv:
    print("Resultado - " + str(resultado))
    logger.info("Procesando creacion de archivos: " + str(resultado))


# Leer lista de usuarios activos de MW
usuarios_mw = leer_csv(os.getenv("ARCHIVO_CSV"))
logger.info("Procesando archivo de usuarios activos: " + str(len(usuarios_mw)))
for usuario in usuarios_mw[1:]:
    id_cliente = usuario[1]
    cedula = usuario[2]
    nombre = usuario[3]
    correo = usuario[14]

    ##### BUSCO LA FECHA DE EMISION DE LA ULTIMA FACTURA DEL CLIENTE ###########
    table_name = "facturas"
    emision_last_factura = buscar_factura(table_name, id_cliente, cedula, nombre)
    factura = False
    if emision_last_factura[0] == "exito":
        if emision_last_factura[1][0] < fecha_max:  # Valido si la factura es anterior al 1 de Abril
            factura = True
    else:
        print(emision_last_factura[1])

    # Solo si la factura existe y esta en la fecha correcta
    if factura is True:
        ##### CREO LA NUEVA FACTURA PRORATEADA AL MISMO CLIENTE ###########
        crear_factura = nueva_factura(id_cliente, cedula, nombre, emision_last_factura[1][0], vencimiento, emision_last_factura[1][2])
        if crear_factura[0] == "exito":
            # Busco la nueva factura creada
            last_factura = buscar_factura(table_name, id_cliente, cedula, nombre)
            if last_factura[0] == "exito":
                # Le agrego la descripcion
                desc_fact = descripcion_factura(last_factura[1], crear_factura[2], id_cliente, cedula, nombre)
                print("Cliente: " + str(id_cliente) + " - " +
                      "Factura creada: " + str(last_factura[1][1]) +
                    " - Fecha de emision: " + str(last_factura[1][0]))
            else:
                print(last_factura[1])
        else:
            print(crear_factura[1])
    else:
        data_csv = str(id_cliente) + "," + cedula + "," + nombre + "," + str(emision_last_factura[1][0]) + ", Emisión en Abril? tiene factura?\n"
        agregar_csv(os.getenv("CSV_NOPROCESADOS"), data_csv)

        logger.info("Cliente: " + str(id_cliente) + " - No se proceso la factura - Emision: " + str(emision_last_factura[1][0]))
        print("Cliente: " + str(id_cliente) + " - No se proceso la factura - Emision: " + str(emision_last_factura[1][0]))

# Cierro la conexion con la base de datos
if cursor:
    cursor.close()
if conn:
    conn.close()


# TODO: Cuales usuarios procesar? solo activos, los suspendidos tambien debe agregarse la factura cierto, si pagan se activaran?
# TODO: joseph: Clientes con fecha de emision Abril (crear nuevas facturas con descuentos?)
# TODO: Validar nuevamente si la factura sera libre, por tema seniat y los permisos
# TODO: Que hacer con el campo legal (nro fiscal) en la facturas (MW2 no tiene nro de control en factura)

# TODO: Obtener lista de clientes automaticas
# TODO: Revisar logger y print
# TODO: Almacenar procesados y fallidos
# TODO: Limpiar registros viudos de tabla facturaitems
# TODO: Crear archivo que simule la creacion de la factura para validar antes



