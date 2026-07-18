from datetime import datetime


def calcular_periodo(data_inicio, data_fim):
    """
    Calcula o período da viagem.
    """
    if data_fim <= data_inicio:
        raise ValueError("A data/hora final deve ser posterior à inicial.")

    horas = (data_fim - data_inicio).total_seconds() / 3600
    pernoite = data_inicio.date() != data_fim.date()

    dias = (data_fim.date() - data_inicio.date()).days + 1

    return {
        "horas": horas,
        "pernoite": pernoite,
        "dias": dias
    }


def calcular_quantidade_diarias(periodo):
    """
    Calcula a quantidade de diárias.

    Regras:

    • Sem pernoite:
        - ½ diária.

    • Com pernoite:
        - quantidade de dias corridos menos ½ diária
          referente ao dia do retorno.
    """

    if not periodo["pernoite"]:
        return 0.5, "½ diária (sem pernoite)"

    dias = periodo["dias"]

    quantidade = dias - 0.5  # Subtrai ½ diária do dia do retorno

    if quantidade == 1:
        descricao = "1 diária"
    elif quantidade.is_integer():
        descricao = f"{int(quantidade)} diárias"
    else:
        descricao = f"{quantidade:.1f} diárias".replace(".", ",")

    return quantidade, descricao


def aplica_reducao(grupo):
    """
    Verifica se o grupo está sujeito à redução das diárias
    prevista no Decreto Estadual nº 90.173/2023.

    O Grupo I não está sujeito à redução.
    Os demais grupos terão a redução aplicada quando cabível.

    Retorna:
        True  -> aplica a redução.
        False -> não aplica a redução.
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
    if quantidade == 0.5 and aplica_reducao(grupo):
        return valor_unitario * 0.5

    return quantidade * valor_unitario