import logging
from datetime import datetime

# Configuro los parámetros y formatos del logging
now = datetime.now()
today = now.strftime('%d%m%Y')
logging.basicConfig(handlers=[logging.FileHandler(filename="log/2net_factura_" + today + ".log", encoding='utf-8', mode='a+')],
                    level=10, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)