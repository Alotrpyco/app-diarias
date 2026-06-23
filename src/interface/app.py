from PIL import Image
from datetime import datetime
import webbrowser
import logging 
import customtkinter as ctk


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

from utils.logger import log_auditoria

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def iniciar_sistema():

    app = ctk.CTk()
    app.title("SETUR/AL - Sistema de Cálculo de Diárias")
    app.geometry("900x800")



