import csv

def leer_csv(archivo_csv):
    with open(archivo_csv, 'r') as archivo:
        lector = csv.reader(archivo)
        return list(lector)