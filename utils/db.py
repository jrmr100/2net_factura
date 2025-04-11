import os

from utils.connect_db import conn, cursor
from datetime import date, datetime, timedelta
import mariadb
from utils.logger import logger



def buscar_factura(table_name, id_cliente):

    sql_string = f"""
            SELECT emitido, id, total
            FROM {table_name}
            WHERE idcliente = ?
            ORDER BY emitido DESC
            LIMIT 1;
            """

    try:
        # Ejecuto el query de SQL con el cursor
        cursor.execute(sql_string, (id_cliente,))

        # Obtengo la fecha de emision de la ultima factura
        resultados = cursor.fetchone()
        if resultados:
            logger.debug("Cliente: " + str(id_cliente) +
                        " - Ultima factura encontrada:" + str(resultados[1]) +
                        " - Fecha de emision: " + str(resultados[0]))
            return "exito", resultados
        else:
            logger.info("Cliente: " + str(id_cliente) + " - No posee facturas.")
            return "error", "Cliente no posee facturas."


    except mariadb.Error as e:
        logger.info("Cliente: " + str(id_cliente) + " - Except al buscar la factura: " + str(e))
        return "except", str(e)

def crear_factura(id_cliente, emision_last_factura, vencimiento, valor_servicio):
    # Nombre de la tabla
    table_name = "facturas"

    un_dia = timedelta(days=1)

    # Mantengo toda la fecha pero cambio el mes a abril
    emision_new_factura = emision_last_factura.replace(month=4)


    # Cambio formato a datetime y agrego un dia
    emision_new_factura = datetime.combine(emision_new_factura, datetime.min.time()) + un_dia # Cambio a formato datetime y agrego un dia

    # Calculo para definir el monto de la nueva factura
    dias_facturables = (datetime(2025, 4, 30) - emision_new_factura) + un_dia
    valor_dia = valor_servicio/30
    total_factura = valor_dia * dias_facturables.days
    total_factura = f"{total_factura:.2f}"



    # campos de la tabla facturas
    legal = 0
    idcliente = id_cliente
    emitido = emision_new_factura
    vencimiento = vencimiento
    pago = 0000 - 00 - 00
    total = total_factura
    tipo = 1
    cobrado = 0
    iva_igv = 0
    sub_total = total_factura
    total_khipu = 0
    siro = 0
    siroconcepto = 0
    percepcion_afip = 0
    saldo = 0

    sql_string = f"INSERT INTO {table_name} (legal, idcliente, emitido, vencimiento, pago, total, tipo, cobrado, iva_igv, sub_total, total_khipu, siro, siroconcepto, percepcion_afip, saldo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

    try:
        # Pasar los valores de las variables como una tupla
        cursor.execute(sql_string, (
        legal, idcliente, emitido, vencimiento, pago, total, tipo, cobrado, iva_igv, sub_total, total_khipu, siro,
        siroconcepto, percepcion_afip, saldo,))

        # Hacer commit para guardar los cambios
        conn.commit()
        logger.info("Cliente: " + str(id_cliente) + " - Factura creada con exito")
        return "exito", "Factura creada con exito"
    except mariadb.Error as e:
        logger.info("cliente: " + str(id_cliente) + " - Except al crear la factura: " + str(e))
        return "except", str(e)

def descripcion_factura(id_factura, cantidad, id_cliente):
    # Nombre de la tabla
    table_name = "facturaitems"

    # campos de la tabla facturas
    idfactura = id_factura
    descripcion = os.getenv("DESCRIPCION_ITEM")
    cantidad = cantidad
    idalmacen = 0
    impuesto = 0
    block = 1
    impuesto911 = 0
    tipoitem = 0
    montodescuento = 0


    sql_string = f"INSERT INTO {table_name} (idfactura, descripcion, cantidad, idalmacen, impuesto, block, impuesto911, tipoitem, montodescuento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"

    try:
        # Pasar los valores de las variables como una tupla
        cursor.execute(sql_string, (
        idfactura[1], descripcion, cantidad, idalmacen, impuesto, block, impuesto911, tipoitem, montodescuento,))

        # Hacer commit para guardar los cambios
        conn.commit()
        logger.info("Cliente: " + str(id_cliente) + " - Descripcion agregada a la factura " + str(id_factura[1]))
        return "exito"
    except mariadb.Error as e:
        logger.info("Cliente: " + str(id_cliente) + " - Except al agregar la descripcion: " + str(e))
