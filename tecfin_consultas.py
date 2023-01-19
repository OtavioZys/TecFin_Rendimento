from tecfin_models import Prorrogacao

def soma_boletosSGV(lista):
    lista_valores = []
    for item in lista:
        qs = Prorrogacao.objects.using('adm_int').filter(cobrancaId__exact=item).values('valorBoletoSgv')
        for value in qs:
            valor = value['valorBoletoSgv']
            lista_valores.append(float(valor))
    total = round(sum(lista_valores), 2)

    return total

def soma_repasseCARD(lista):
    lista_valores = []
    for item in lista:
        qs = Prorrogacao.objects.using('adm_int').filter(cobrancaId=item).values('valorRepasseGrupoCard')
        for value in qs:
            lista_valores.append(value['valorRepasseGrupoCard'])
    total = round(sum(lista_valores), 2)

    return total


