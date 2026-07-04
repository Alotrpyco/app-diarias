import logging


"""""
====SISTEMA DE AUDITORIA (LOGGING)=====
Responsável por registrar eventos importantes do sistema,
como cálculos realizados, geração e erros.
Os registros são armazenados em um arquivo .log para rastreabilidade.
"""

import logging

logging.basicConfig(
    filename="auditoria_diarias.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)

def log_auditoria(
    grupo,
    tipo,
    localidade,
    quantidade,
    valor_unitario,
    total
):

    mensagem = (
        f"Grupo={grupo} | "
        f"Tipo={tipo} | "
        f"Localidade={localidade} | "
        f"Quantidade={quantidade} | "
        f"Valor Unitário={valor_unitario:.2f} | "
        f"Total={total:.2f}"
    )

    logging.info(mensagem)
