import logging


"""""
====SISTEMA DE AUDITORIA (LOGGING)=====
Responsável por registrar eventos importantes do sistema,
como cálculos realizados, geração e erros.
Os registros são armazenados em um arquivo .log para rastreabilidade.
"""

logging.basicConfig(
    filename="auditoria_diarias.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)

def log_auditoria(mensagem):
    logging.info(mensagem)
