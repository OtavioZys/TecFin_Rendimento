import json
import locale
from rendimento_getters import get_extrato
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

def get_cobrancas_rendimento():
    data = int(date.today().strftime('%w'))
    if data == 1:
        sexta = (date.today() - timedelta(days=3)).strftime('%m-%d-%Y')
        feriado = checa_dia(3)
        if feriado:
            pass 
        else:
            lista_cobrancas = []
            try:
                extrato_json = get_extrato(sexta)
                lista_value = dict(extrato_json['value'])
                for cobranca in lista_value['itens']:
                    lista_cobrancas.append(json.dumps(cobranca))

                return lista_cobrancas
            except Exception as error:
                print(error)
    else:
        # ontem = (datetime.now() - timedelta(days=1)).replace(microsecond=0)
        ontem = (date.today() - timedelta(days=1)).strftime('%m-%d-%Y')
        feriado = checa_dia(1)
        if feriado:
            pass 
        else:
            lista_cobrancas = []
            try:
                extrato_json = get_extrato(ontem)
                lista_value = dict(extrato_json['value'])
                for cobranca in lista_value['itens']:
                    lista_cobrancas.append(json.dumps(cobranca))
                
                return lista_cobrancas
            except Exception as error:
                print(error)