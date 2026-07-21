from datetime import datetime


def calcular_periodo(data_inicio, data_fim):
    """
    Calcula o período da viagem.
    """
    if data_fim <= data_inicio:
        raise ValueError("A data/hora final deve ser posterior à inicial.")

    horas = (data_fim - data_inicio).total_seconds() / 3600

    pernoite = data_inicio.date() != data_fim.date()
    
    # conta os dias de partida e chegada
    dias = (data_fim.date() - data_inicio.date()).days + 1

    return {
        "horas": horas,
        "pernoite": pernoite,
        "dias": dias,
        "retorno": data_fim
    }


def calcular_quantidade_diarias(periodo):
  
    if not periodo["pernoite"]:
        return 0.5, "½ diária (sem pernoite)"
    
    dias = periodo["dias"]
    retorno = periodo["retorno"]

    # diárias completas dos dias intermediários
    quantidade = dias - 2

    # diária do dia da partida
    quantidade += 1
    
    # verifica o horário de retorno
    if retorno.hour >= 12:
        quantidade += 0.5
    else:
        quantidade += 1

    if quantidade == 1:
        descricao = "1 diária"
    elif quantidade == int(quantidade):
        descricao = f"{int(quantidade)} diárias"
    else:
        descricao = f"{quantidade} diárias"

    return quantidade, descricao


def aplica_reducao(grupo):
    """
    Verifica se o grupo está sujeito à redução das diárias
    prevista no Decreto Estadual nº 90.173/2023.

    O Grupo I não está sujeito à redução.
    """

    grupos_sem_reducao = [
        "Grupo I",
    ]

    return grupo not in grupos_sem_reducao


def calcular_valor(quantidade, valor_unitario, grupo):
    """
    Calcula o valor total das diárias.
    """

    # Caso seja meia diária
    if quantidade == 0.5:
        return valor_unitario * 0.5

    return quantidade * valor_unitario