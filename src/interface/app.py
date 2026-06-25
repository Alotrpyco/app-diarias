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

from utils.diarias import(
    calcular_dias_diaria
)

from utils.formatadores import(
    formatar_moeda   
)

from utils.logger import log_auditoria

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def iniciar_sistema():

    app = ctk.CTk()
    app.title("SETUR/AL - Sistema de Cálculo de Diárias")
    app.geometry("900x800")

#=====================LOGO(SETUR)=========================
    logo = ctk.CTkImage(
        light_image=Image.open("logo_setur.png"),
        size=(140,140)
    )

    ctk.CTkLabel(app, imagem=logo, text="").pack(pady=10)

    ctk.CTkLabel(
        app, 
        text="Secretaria de Estado do Turismo de Alagoas",
        font=("Arial", 14)
    ).pack(pady=(0,20))
    app.mainloop()

