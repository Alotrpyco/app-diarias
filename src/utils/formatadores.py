def formatar_moeda(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

#=====CONDIÇÃO PARA O CALCULO DE DIÁRIAS======
from datetime import datetime

def calcular_dias_diaria(data_inicio, data_fim):
    diferenca = data_fim - data_inicio
    horas = diferenca.total_seconds() / 3600

    if horas <= 12:
        return 0.5, "½ diária (até 12h)", horas

    dias = int(horas // 24)
    resto = horas % 24

    if resto > 12:
        dias += 1
        descricao = f"{dias} diárias"
    else:
        descricao = f"{dias} diárias + ½"

    return dias, descricao, horas


