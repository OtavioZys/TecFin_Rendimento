import re
from rendimento_models import Item 
from datetime import date, timedelta


def soma_valoresExtratoRendimento(lista):
    lista_valores = []
    for item in lista:
        compl = f"Tecfin - CobrancaID: {item}"
        qs = Item.objects.using('adm_int').filter(complemento__exact=compl).values('valor')
        for value in qs:
            valor = value['valor']
            lista_valores.append(float(valor))
    total = sum(lista_valores)

    return round(total, 2)


def get_moneyplus():
    data = int(date.today().strftime('%w'))
    lista = []
    if data == 1:
        sexta = (date.today() - timedelta(days=3)).strftime('%d-%m-%Y')
        money = "MONEY PLUS"
        cp = "0000000000"
        mp = Item.objects.using('adm_int').filter(
            contaContraparte__exact=cp
        ).filter(
            nomeContraparte__contains=money
        ).filter(
            dia_consulta__exact=sexta
        ).values('valor', 'nrDocumento', 'dataLancto')

        for item in mp:
            valor_raw = str(item['valor'])
            valor = re.sub("[Decimal(')]", "", valor_raw)
            doc = item['nrDocumento']
            data = item['dataLancto']

            report = {
                'documento': doc,
                'valor': valor,
                'data': data.strftime('%d/%m/%Y')
            }
            lista.append(report)

        return lista
    else:
        ontem = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
        money = "MONEY PLUS"
        cp = "0000000000"
        mp = Item.objects.using('adm_int').filter(
            contaContraparte__exact=cp
        ).filter(
            nomeContraparte__contains=money
        ).filter(
            dia_consulta__exact=ontem
        ).values('valor', 'nrDocumento', 'dataLancto')

        for item in mp:
            valor_raw = str(item['valor'])
            valor = re.sub("[Decimal(')]", "", valor_raw)
            doc = item['nrDocumento']
            data = item['dataLancto']

            report = {
                'documento': doc,
                'valor': valor,
                'data': data.strftime('%d/%m/%Y')
            }
            lista.append(report)

        return lista
