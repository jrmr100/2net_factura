import os

from utils.connect_db import conn, cursor
from datetime import date, datetime, timedelta
import mariadb
from utils.logger import logger
from utils.csv_files import agregar_csv



def buscar_factura(table_name, id_cliente, cedula, nombre, today):

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
            data_csv = str(id_cliente) + "," + cedula + "," + nombre + ",," + "Cliente no posee facturas.\n"
            agregar_csv(os.getenv("CSV_NOPROCESADOS") + "-" + str(today) + ".csv", data_csv)
            logger.info("Cliente: " + str(id_cliente) + " - No posee facturas.")
            print("ERROR - Cliente: " + str(id_cliente) + " - No posee facturas.")
            return "error", "Cliente no posee facturas."


    except mariadb.Error as e:
        data_csv = str(id_cliente) + "," + str(e) + "\n"
        agregar_csv(os.getenv("CSV_NOPROCESADOS") + "-" + str(today) + ".csv", data_csv)
        logger.info("Cliente: " + str(id_cliente) + " - Except al buscar la factura: " + str(e))
        logger.info("ERROR - Cliente: " + str(id_cliente) + " - Except al buscar la factura: " + str(e))
        return "except", str(e)

def nueva_factura(id_cliente, cedula, nombre, emision_last_factura, vencimiento, valor_servicio, today):
    # Nombre de la tabla
    table_name = "facturas"

    un_dia = timedelta(days=1)

    # Mantengo toda la fecha pero cambio el mes a abril
    # valida si el dia de la fecha es 31


    if emision_last_factura.day == 31:
        emision_last_factura = emision_last_factura.replace(day=30)
    emision_new_factura = emision_last_factura.replace(month=4)


    # Cambio formato a datetime y agrego un dia
    emision_new_factura = datetime.combine(emision_new_factura, datetime.min.time()) + un_dia # Cambio a formato datetime y agrego un dia

    # Calculo para definir el monto de la nueva factura
    dias_facturables = (datetime(2025, 4, 30) - emision_new_factura) + un_dia
    valor_dia = valor_servicio/30
    total_factura = valor_dia * dias_facturables.days
    total_factura = f"{total_factura:.2f}"

    # campos de la tabla facturas
    legal = 0  # Nro de factura fiscal
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

    data_csv = str(legal) + "," +str(idcliente) + "," + cedula + "," + nombre + "," + str(emitido) + "," + str(vencimiento) + "," + str(pago) +\
               "," + total + "," + str(tipo) + ","  + str(cobrado) + "," + str(iva_igv) + "," + sub_total +\
               "," + str(total_khipu) + "," + str(siro) + "," + str(siroconcepto) + "," + str(percepcion_afip) +\
               "," + str(saldo) + "\n"

    try:
        sql_string = f"INSERT INTO {table_name} (legal, idcliente, emitido, vencimiento, pago, total, tipo, cobrado, iva_igv, sub_total, total_khipu, siro, siroconcepto, percepcion_afip, saldo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        # Pasar los valores de las variables como una tupla
        # cursor.execute(sql_string, (
        # legal, idcliente, emitido, vencimiento, pago, total, tipo, cobrado, iva_igv, sub_total, total_khipu, siro,
        # siroconcepto, percepcion_afip, saldo,))

        # Hacer commit para guardar los cambios

        # conn.commit()

        agregar_csv(os.getenv("CSV_NUEVAS") + "-" + str(today) + ".csv", data_csv)
        logger.info("Cliente: " + str(id_cliente) + " - Factura nueva creada con exito")
        return "exito", "Factura nueva creada con exito", total_factura
    except mariadb.Error as e:
        data_csv = str(id_cliente) + "," + cedula + "," + nombre + "," + "," + str(e)
        agregar_csv(os.getenv("CSV_NOPROCESADOS") + "-" + str(today) + ".csv", data_csv)
        logger.info("cliente: " + str(id_cliente) + " - Except al crear la factura: " + str(e))
        print("cliente: " + str(id_cliente) + " - Except al crear la factura: " + str(e))
        return "except", str(e)

def descripcion_factura(id_factura, cantidad, id_cliente, cedula, nombre, today):
    # Nombre de la tabla
    table_name = "facturaitems"

    # campos de la tabla facturaitems
    idfactura = id_factura
    descripcion = os.getenv("DESCRIPCION_ITEM")
    cantidad = cantidad
    idalmacen = 0
    impuesto = 0
    block = 1
    impuesto911 = 0
    tipoitem = 0
    montodescuento = 0

    data_csv = id_cliente + "," + cedula + "," + nombre + "," + str(idfactura[1]) + "," + descripcion +\
               "," + str(cantidad) + "," + str(idalmacen) + "," + str(impuesto) + "," + str(block) +\
               "," + str(impuesto911) + "," + str(tipoitem) + "," + str(montodescuento) + "\n"


    try:
        sql_string = f"INSERT INTO {table_name} (idfactura, descripcion, cantidad, idalmacen, impuesto, block, impuesto911, tipoitem, montodescuento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
        # Pasar los valores de las variables como una tupla
        # cursor.execute(sql_string, (
        # idfactura[1], descripcion, cantidad, idalmacen, impuesto, block, impuesto911, tipoitem, montodescuento,))

        # Hacer commit para guardar los cambios
        # conn.commit()
        agregar_csv(os.getenv("CSV_DESCRIPCION") + "-" + str(today) + ".csv", data_csv)
        logger.info("Cliente: " + str(id_cliente) + " - Descripcion agregada a la factura " + str(id_factura[1]))
        return "exito"
    except mariadb.Error as e:
        data_csv = str(id_cliente) + "," + cedula + "," + nombre + ",," + str(e)
        agregar_csv(os.getenv("CSV_NOPROCESADOS") + "-" + str(today) + ".csv", data_csv)
        logger.info("Cliente: " + str(id_cliente) + " - Except al agregar la descripcion: " + str(e))
        print("Cliente: " + str(id_cliente) + " - Except al agregar la descripcion: " + str(e))

def saldo_favor(emision_last_factura, today, monto, id_cliente, cedula, nombre, fecha_inicio):
    # Nombre de la tabla
    table_name = "saldos"

    idorigen = 0
    iddestino = 0
    estado = "no cobrado"
    fecha = date(2025,5,1)
    descripcion = "Saldo a favor por cambios en facturación"
    codigopasarela = ""
    moneda = 1

    valor_dia = monto / 30  # Calculo el valor por dia de cada servicio

    dos_dias = timedelta(days=2)

    # Calculo los dias desde el 2 hasta la fecha de emision de la ultima factura mas un dia
    dias_saldo = (emision_last_factura - fecha_inicio) + dos_dias

    # Calculo el monto del saldo a agregar
    monto_saldo = int(dias_saldo.days) * valor_dia
    monto_saldo = f"{monto_saldo:.2f}"  # quito decimales
    monto_saldo = float(monto_saldo) * -1  # El saldo debe ser negativo para ser cargado

    try:
        sql_string = f"INSERT INTO {table_name} (iduser, idorigen, iddestino, estado, monto, fecha, descripcion, codigopasarela, moneda) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
        # Pasar los valores de las variables como una tupla
        #cursor.execute(sql_string, (
        #id_cliente, idorigen, iddestino, estado, monto, fecha, descripcion, codigopasarela, moneda))
        # Hacer commit para guardar los cambios
        # conn.commit()

        data_csv = f"{str(id_cliente)}, {idorigen} , {iddestino}, {estado}, {monto_saldo}, {fecha}, {descripcion}, {codigopasarela}, {moneda}\n"

        agregar_csv(os.getenv("CSV_NUEVAS") + "-" + str(today) + ".csv", data_csv)
        logger.info("Cliente: " + str(id_cliente) + " - Saldo agregado con exito")

        print(f"EXITO - Cliente: {str(id_cliente)} : {nombre} - Fecha ultima factura: {emision_last_factura} - Dias saldo {dias_saldo.days} - monto saldo: {monto_saldo}")
        return "exito", "Saldo agregado con exito", data_csv
    except mariadb.Error as e:
        data_csv = str(id_cliente) + "," + cedula + "," + nombre + "," + "," + str(e) + "\n"
        agregar_csv(os.getenv("CSV_NOPROCESADOS") + "-" + str(today) + ".csv", data_csv)
        logger.info("cliente: " + str(id_cliente) + " - Except al agregar saldo: " + str(e))
        print("ERROR - cliente: " + str(id_cliente) + " - Except al agregar saldo: " + str(e))
        return "except", str(e)
