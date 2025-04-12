import csv
import os

def leer_csv(archivo_csv):
    with open(archivo_csv, 'r') as archivo:
        lector = csv.reader(archivo)
        return list(lector)

def crear_csv():
    def crear_archivo(archivo_csv, cabecera):
        try:
            with open(archivo_csv, 'w') as archivo:
                archivo.write(cabecera)
            return "Archivo creado: " + archivo_csv
        except Exception as e:
            print(e)
            return "Error creando archivo:" +  archivo_csv + " - " + str(e)

    # Facturas nuevas
    cabecera_csv = "legal, idcliente, emitido, vencimiento, pago, total, tipo, cobrado, iva_igv, sub_total,\
 total_khipu, siro, siroconcepto, percepcion_afip, saldo\n"
    crear_facturas_nuevas = crear_archivo(os.getenv("CSV_NUEVAS"), cabecera_csv)

    # Descripciones
    cabecera_csv = "idfactura, descripcion, cantidad, idalmacen, impuesto, block, impuesto911, tipoitem, montodescuento\n"
    crear_descripciones = crear_archivo(os.getenv("CSV_DESCRIPCION"), cabecera_csv)

    # No procesados
    cabecera_csv = "idcliente, Descripcion\n"
    crear_noprocesados = crear_archivo(os.getenv("CSV_NOPROCESADOS"), cabecera_csv)

    return [crear_facturas_nuevas, crear_descripciones, crear_noprocesados]



def agregar_csv(archivo_csv, data):
    with open(archivo_csv, 'a') as archivo:
        archivo.write(data)