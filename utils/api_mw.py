import requests
import json
from dotenv import load_dotenv
from utils.logger import logger
import time


import os

load_dotenv()


def conectar(headers, body, endpoint, metodo):
    try:
        if metodo == "GET":

            response = requests.get(endpoint,
                                    headers=headers,
                                    timeout=15)
        elif metodo == "POST":

            response = requests.post(endpoint,
                                     headers=headers, json=body,
                                     timeout=15)

        response_decode = response.content.decode("utf-8")
        api_response = json.loads(response_decode)
        return "success", api_response
    except Exception as error:
        return "except", str(error)

def buscar_factura(id_mw1):
    intentos = 0
    estado = 0
    while intentos < 3:
        headers = {"content-type": "application/json"}
        body = {"token": os.getenv("TOKEN_MW"), "idcliente": id_mw1, "estado": estado}
        endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_FACTURAS")

        api_response = conectar(headers, body, endpoint,"POST")
        if api_response[0] == "success":
            logger.info("Facturas encontradas\n" + str(api_response))
            return api_response
        elif api_response[0] == "except":
            intentos += 1
            print(f"Error en el intento {intentos}: {api_response[1]}. Reintentando en 5 segundos...")
            logger.info(f"Error en el intento {intentos}: {api_response[1]}. Reintentando en 5 segundos...")
            time.sleep(5)  # Espera antes de reintentar
    print("Máximo de intentos alcanzado. Búsqueda fallida.")
    return None  # Todos los intentos fallaron

def crear_factura(id_mw1, vencimiento):
    intentos = 0
    while intentos < 3:
        headers = {"content-type": "application/json"}
        body = {"token": os.getenv("TOKEN_MW"), "idcliente": id_mw1, "vencimiento": vencimiento}
        endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_FACTURAS")

        api_response = conectar(headers, body, endpoint, "POST")





