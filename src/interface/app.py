from PIL import Image
from datetime import datetime
from tkinter import messagebox
import webbrowser
import logging 
import customtkinter as ctk

from src.constantes.config import (
    DIARIAS,
    CARGOS_GRUPOS
)

from src.constantes.links import (
    abrir_site_setur,
    abrir_banco_central,
    abrir_cotacao_bcb,
    abrir_decreto
)

from src.utils.diarias import(
    calcular_periodo,
    calcular_quantidade_diarias,
    aplica_reducao,
    calcular_valor
    
)

from src.utils.formatadores import(
    formatar_moeda   
)

from src.utils.logger import log_auditoria

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def iniciar_sistema():

    app = ctk.CTk()
    app.title("SETUR/AL - Sistema de Cálculo de Diárias")
    app.geometry("900x800")

    #=====================LOGO DA SETUR=====================
    logo = ctk.CTkImage(
        light_image=Image.open("image/logo_setur.png"),
        size=(140,140)
    )

    ctk.CTkLabel(app, image=logo, text="").pack(pady=10)

    ctk.CTkLabel(
        app, 
        text="Secretaria de Estado do Turismo de Alagoas",
        font=("Arial", 14)
    ).pack(pady=(0,20))    

    #========================QUADRO=========================
    frame = ctk.CTkFrame(app)
    frame.pack(fill="x", padx=20, pady=20)

    localidade_var = ctk.StringVar()
    grupo_var = ctk.StringVar(value="Grupo I")

    ctk.CTkLabel(frame, text="Grupo").grid(row=0, column=0, padx=10, pady=10)

    grupo_menu = ctk.CTkOptionMenu(
        frame,
        variable=grupo_var,
        values=list(DIARIAS.keys())
    )
    grupo_menu.grid(row=0, column=1)

    def mostrar_cargos():
        grupos = grupo_var.get()
        cargos = "\n".join(CARGOS_GRUPOS[grupos])
            
        messagebox.showinfo("Cargos do Grupo", cargos)

    ctk.CTkButton(
        frame,
        text="Ver Cargos",
        command=mostrar_cargos,
        width=120
    ).grid(row=0, column=2, padx=10)

    #=====================TIPO DE VIAGEM====================
    ctk.CTkLabel(frame, text="Tipo").grid(row=2, column=0)

    tipo_var = ctk.StringVar(value="Nacional")

    tipo_menu = ctk.CTkOptionMenu(
        frame,
        variable=tipo_var,
        values=["Nacional", "Internacional"]
    )
    tipo_menu.grid(row=1, column=1)

    #=================LOCALIDADES============================
    ctk.CTkLabel(frame, text="Localidade").grid(row=2, column=0)

    localidade_menu = ctk.CTkOptionMenu(
        frame,
        variable=localidade_var,
        values=[]
    )
    localidade_menu.grid(row=2, column=1)

    def atualizar_localidades(*args):
        grupo = grupo_var.get()
        tipo = tipo_var.get()

        locais = list(DIARIAS[grupo][tipo].keys())

        localidade_menu.configure(values=locais)

        if locais:
            localidade_var.set(locais[0])
        
    grupo_var.trace_add("write", atualizar_localidades)
    tipo_var.trace_add("write", atualizar_localidades)

    atualizar_localidades()
    
    #===================DATAS & HORAS INICIAIS ==============
    ctk.CTkLabel(frame, text="Data Inicial").grid(row=3, column=0)
    data_inicio = ctk.CTkEntry(frame)
    data_inicio.grid(row=3, column=1)

    ctk.CTkLabel(frame, text="Hora Inicial").grid(row=3, column=2)
    hora_inicio = ctk.CTkEntry(frame)
    hora_inicio.grid(row=3, column=3)

    #=======================DATAS & HORAS FINAIS==============
    ctk.CTkLabel(frame, text="Data Final").grid(row=4, column=0)
    data_fim = ctk.CTkEntry(frame)
    data_fim.grid(row=4, column=1)

    ctk.CTkLabel(frame, text="Hora Final").grid(row=4, column=2)
    hora_fim = ctk.CTkEntry(frame)
    hora_fim.grid(row=4, column=3)

    # ============CAIXA PARA DIGITAR O VALOR DA COTAÇÃO========
    ctk.CTkLabel(frame, text="Cotação da Moeda ").grid(row=5, column=0)

    cotacao = ctk.CTkEntry(frame)
    cotacao.grid(row=5, column=1)

    #==QUADRO QUE SERÁ EXIBIDO AS INFORMÇÕES DAS DIÁRIAS======
    resultado = ctk.CTkTextbox(app, width=800, height=275)
    resultado.pack(padx=20, pady=20)

    texto_cache = {"conteudo": ""}
    
    app.mainloop()