import re
import pandas as pd
from apps.extrato.models import Item
from apps.tecfin.models import Prorrogacao
from datetime import datetime, date, timedelta


def cobrancasId_extrato():
    lista_ids = []
    data = (date.today()).strftime('%d-%m-%Y')
    compl = f"Tecfin - CobrancaID"
    qs = Item.objects.using('adm_int').filter(dia_consulta=data).filter(complemento__contains=compl).values('complemento')
    for query in qs:
        cobranca = query['complemento']
        x = re.search("Tecfin - CobrancaID:", cobranca)
        if x:
            id_extrato = re.sub("Tecfin - CobrancaID: ", "", cobranca)
            id_extrato = int(id_extrato)
            lista_ids.append(id_extrato)

    return lista_ids


def cobrancasId_tecfin():
    lista_ids = []
    data = (date.today()).strftime('%d-%m-%Y')
    qs = Prorrogacao.objects.using('adm_int').filter(dia_consulta=data).values('cobrancaId')
    for query in qs:
        cobran = query['cobrancaId']
        lista_ids.append(int(cobran))

    return lista_ids


def relatorio_tecfin(data):
    """
    FAZ CONSULTA NO BD FILTRADO POR DATA E EXTRAI OS DADOS, RETORNA EM FORMATO DATAFRAME
    """
    lista = []
    try:
        info = Prorrogacao.objects.using('adm_int').exclude(
            dataContratacao__gte=datetime.now()
        ).filter(
            dataContratacao__gte=data
        ).order_by('nomeEmpresa').values()
        return info
    except Exception as error:
        print(error)
