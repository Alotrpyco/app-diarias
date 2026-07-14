from PIL import Image
from datetime import datetime
from tkinter import messagebox
import tkinter as tk
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
        size=(275,175)
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
    resultado = ctk.CTkTextbox(app, width=800, height=250)
    resultado.pack(padx=20, pady=20)

    texto_cache = {"conteudo": ""}
    def calcular():

        try:
            inicio = datetime.strptime(
                f"{data_inicio.get()} {hora_inicio.get()}",
                "%d/%m/%Y %H:%M"
            )

            fim = datetime.strptime(
                f"{data_fim.get()} {hora_fim.get()}",
                "%d/%m/%Y %H:%M"
            )

            grupo = grupo_var.get()
            tipo = tipo_var.get()
            local = localidade_var.get()

      #=======CÁLCULO PARA O PERÍODO DA VIAGEM NACIONAL=============
    
            periodo = calcular_periodo(inicio, fim)

            if periodo["pernoite"]:
                pernoite = "Houve pernoite"
            else:
                pernoite = "Não houve pernoite"

            quantidade, descricao = calcular_quantidade_diarias(periodo)

            horas = periodo["horas"]

            valor_unitario = DIARIAS[grupo][tipo][local]

            total = calcular_valor(
                quantidade,
                valor_unitario,
                grupo
            )

            texto = (
                f"Duração: {horas:.1f} horas\n\n"
                f"{descricao}\n\n"
            )

       # ======== VIAGEM NACIONAL===================
            
            if tipo == "Nacional":

                texto += (
                    f"Grupo: {grupo}\n\n"
                    f"Localidade: {local}\n\n"
                    f"Quantidade de Diárias: {quantidade}\n\n"
                    f"{pernoite}\n\n"
                    f"Valor Unitário: R$ {formatar_moeda(valor_unitario)}\n\n"
                    f"Total: R$ {formatar_moeda(total)}\n\n"
                    f"Cargos do grupo:\n"
                    f"{', '.join(CARGOS_GRUPOS[grupo])}"
                )

       # ======== VIAGEM INTERNACIONAL ===================
            else:

                if not cotacao.get():
                    raise ValueError(
                        "Informe a cotação para viagens internacionais."
                    )

                cotacao_valor = float(
                    cotacao.get().replace(",", ".")
                )

                total_reais = total * cotacao_valor

                texto = (
                    f"Grupo: {grupo}\n\n"
                    f"Tipo: {tipo}\n\n"
                    f"Localidade: {local}\n\n"
                    f"Afastamento: {periodo['dias']} dias\n\n"
                    f"Quantidade de Diárias: {quantidade}\n\n"
                    f"Valor Unitário: US$ {formatar_moeda(valor_unitario)}\n\n"
                    f"Cotação: R$ {formatar_moeda(cotacao_valor)}\n\n"
                    f"Total em Dólar: US$ {formatar_moeda(total)}\n\n"
                    f"Total em Reais: R$ {formatar_moeda(total_reais)}\n\n"
                    f"Cargos do grupo:\n"
                    f"{', '.join(CARGOS_GRUPOS[grupo])}"
                )

            resultado.delete("1.0", "end")
            resultado.insert("1.0", texto)

            texto_cache["conteudo"] = texto

            log_auditoria(
                grupo=grupo,
                tipo=tipo,
                localidade=local,
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                total=total if tipo == "Nacional" else total_reais
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro)
            )
    # ===== BOTÕES DE CÁLCULO E LINKS ÚTEIS =========
    frame_btn = ctk.CTkFrame(app)
    frame_btn.pack(fill="x", padx=20)

    ctk.CTkButton(
            frame_btn,
            text="Calcular",
            command=calcular
        ).pack(side="left", padx=10, pady=10)

    ctk.CTkButton(
            frame_btn,
            text="Portal SETUR",
            command=abrir_site_setur
        ).pack(side="left", padx=10)

    ctk.CTkButton(
            frame_btn,
            text="Banco Central",
            command=abrir_banco_central
        ).pack(side="left", padx=10)
    
    ctk.CTkButton(
            frame_btn,
            text="Cotação BCB",
            command=abrir_cotacao_bcb
        ).pack(side="left", padx=10)
    
    ctk.CTkButton(
            frame_btn,
            text="Decreto",
            command=abrir_decreto
        ).pack(side="left", padx=10)
   
    
    app.mainloop()
