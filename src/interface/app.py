from PIL import Image
from datetime import datetime
import webbrowser
import logging 

from constantes.config import (
    DIARIAS,
    CARGOS_GRUPOS
)

from constantes.links import (
    abrir_site_setur,
    abrir_banco_central,
    abrir_cotacao_bcb,
    abrir_decreto
)

from utils.formatadores import(
    formatar_moeda,
    calcular_dias_diaria
)

#============================================================
"""""
====SISTEMA DE AUDITORIA (LOGGING)=====
Responsável por registrar eventos importantes do sistema,
como cálculos realizados, geração e erros.
Os registros são armazenados em um arquivo .log para rastreabilidade.
"""""

logging.basicConfig(
    filename="auditoria_diarias.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)

def log_auditoria(mensagem):
    logging.info(mensagem)
#===========================================================

