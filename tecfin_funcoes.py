import json
import locale
from tecfin_models import Prorrogacao
from tecfin_getters import get_prorrogacoes
from datetime import datetime, timedelta, date 

locale.setlocale(locale.LC_ALL, '')

def data_formatada():
    ano = int(date.today().strftime('%Y'))
    mes = int(date.today().strftime('%m'))
    dia1 = int((date.today() - timedelta(days=1)).strftime('%d'))
    dia2 = int((date.today() - timedelta(days=2)).strftime('%d'))
    form23 = datetime(year=ano, month=mes, day=dia2, hour=23, minute=0, second=0)
    form22 = datetime(year=ano, month=mes, day=dia1, hour=22, minute=59, second=59)
    format = f'{form23} à {form22}'

    return format

def checa_dia(filtro):
    data = date.today() - timedelta(days=filtro)
    lista_feriados = [
            {'dia': 1, 'mes': 1, 'feriado': 'Ano-Novo'},
            {'dia': 21, 'mes': 4, 'feriado': 'Tiradentes'},
            {'dia': 1, 'mes': 5, 'feriado': 'Dia do Trabalhador'},
            {'dia': 7, 'mes': 9, 'feriado': 'Declaração da Independência'},
            {'dia': 12, 'mes': 10, 'feriado': 'Nossa Sra Aparecida'},
            {'dia': 2, 'mes': 11, 'feriado': 'Finados'},
            {'dia': 15, 'mes': 11, 'feriado': 'Proclamação da República'},
            {'dia': 25, 'mes': 12, 'feriado': 'Natal'}
        ]
    is_feriado = bool
    dia = int(data.strftime('%d'))
    mes = int(data.strftime('%m'))
    for feriado in lista_feriados:
        if feriado['mes'] == mes and feriado['dia'] == dia:
            print(f"Dia {dia}/{mes} é o feriado {feriado['feriado']}")
            is_feriado = True
            break
        else:
            is_feriado = False 
    
    return is_feriado

def get_cobrancas_tecfin():
    data = int(date.today().strftime('%w'))
    if data == 1:
        sexta = date.today() - timedelta(days=3)
        feriado = checa_dia(3)
        if feriado:
            pass 
        else:
            lista_prorrogacoes = []
            try:
                tecfin_json = get_prorrogacoes(sexta)
                prorrogacoes = tecfin_json['content']
                for prorrogacao in prorrogacoes:
                    cobrancaid = Prorrogacao.objects.using('adm_int').filter(cobrancaId=prorrogacao['cobrancaId']).values()
                    if cobrancaid:
                        print(f"Registro da cobrança {prorrogacao['cobrancaId']} encontrado!")
                    else:
                        lista_prorrogacoes.append(dict(prorrogacao))

                return lista_prorrogacoes
            except Exception as error:
                print(error)
    else:
        # ontem = (datetime.now() - timedelta(days=1)).replace(microsecond=0)
        ontem = date.today() - timedelta(days=1)
        feriado = checa_dia(1)
        if feriado:
            pass 
        else:
            lista_prorrogacoes = []
            try:
                tecfin_json = get_prorrogacoes(ontem)
                prorrogacoes = tecfin_json['content']
                for prorrogacao in prorrogacoes:
                    cobrancaid = Prorrogacao.objects.using('adm_int').filter(cobrancaId=prorrogacao['cobrancaId']).values()
                    if cobrancaid:
                        print(f"Registro da cobrança {prorrogacao['cobrancaId']} encontrado!")
                    else:
                        lista_prorrogacoes.append(dict(prorrogacao))
                
                return lista_prorrogacoes
            except Exception as error:
                print(error)


def get_cobrancas_ids():
    data = int(date.today().strftime('%w'))
    if data == 1:
        sexta = datetime.now() - timedelta(days=3)
        feriado = checa_dia(3)
        if feriado:
            pass 
        else:
            lista_ids = Prorrogacao.objects.using('adm_int').exclude(
                    dataContratacao__gte=date.today()
                ).filter(
                    dataContratacao__gte=datetime.date(sexta)
                ).values_list('cobrancaId', flat=True)

            return lista_ids
    else:
        # ontem = (datetime.now() - timedelta(days=1)).replace(microsecond=0)
        ontem = datetime.now() - timedelta(days=1)
        feriado = checa_dia(1)
        if feriado:
            pass 
        else:
            lista_ids = Prorrogacao.objects.using('adm_int').exclude(
                    dataContratacao__gte=date.today()
                ).filter(
                    dataContratacao__gte=datetime.date(ontem)
                ).values_list('cobrancaId', flat=True)

            return lista_ids
