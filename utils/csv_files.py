import csv
import os


def leer_csv(archivo_csv):
    with open(archivo_csv, 'r') as archivo:
        lector = csv.reader(archivo)
        return list(lector)

def crear_csv(today):
    def crear_archivo(archivo_csv, cabecera):
        try:
            with open(archivo_csv, 'w') as archivo:
                archivo.write(cabecera)
            return "Archivo creado: " + archivo_csv
        except Exception as e:
            print(e)
            return "Error creando archivo:" +  archivo_csv + str(e)

    # Facturas nuevas
    cabecera_csv = "legal, idcliente, cedula, nombre, emitido, vencimiento, pago, total, tipo, cobrado, iva_igv, sub_total,\
 total_khipu, siro, siroconcepto, percepcion_afip, saldo\n"
    crear_facturas_nuevas = crear_archivo(os.getenv("CSV_NUEVAS") + "-" + str(today) + ".csv", cabecera_csv)

    # Descripciones
    cabecera_csv = "id_cliente, cedula, nombre, idfactura, descripcion, cantidad, idalmacen, impuesto, block, impuesto911, tipoitem, montodescuento\n"
    crear_descripciones = crear_archivo(os.getenv("CSV_DESCRIPCION") + "-" + str(today) + ".csv", cabecera_csv)

    # No procesados
    cabecera_csv = "idcliente, cedula, nombre, Fecha_ultima_factura, Descripcion\n"
    crear_noprocesados = crear_archivo(os.getenv("CSV_NOPROCESADOS") + "-" + str(today) + ".csv", cabecera_csv)

    # agregar saldo
    cabecera_csv = "id_cliente, idorigen, iddestino, estado, monto_saldo, fecha, descripcion, codigopasarela, moneda\n"
    crear_agregar_saldo = crear_archivo(os.getenv("CSV_NUEVAS") + "-" + str(today) + ".csv", cabecera_csv)

    # return [crear_facturas_nuevas, crear_descripciones, crear_noprocesados]
    return [crear_agregar_saldo, crear_noprocesados]



def agregar_csv(archivo_csv, data):
    with open(archivo_csv, 'a') as archivo:
        archivo.write(data)