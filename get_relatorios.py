import locale
import pandas as pd 
from datetime import date 
from rendimento_models import Item
from tecfin_models import Prorrogacao

locale.setlocale(locale.LC_ALL, '')

def relatorio_tecfin(data):
    lista = []
    try:
        info = Prorrogacao.objects.using('adm_int').exclude(
            dataContratacao__gte=date.today()
        ).filter(
            dataContratacao__gte=data
        ).order_by('nomeEmpresa').values()
        for item in info:
            objeto = {
                'id': item['id'],
                'statusdacontratacao': item['statusDaContratacao'],
                'cpfcnpj': item['cpfCnpj'],
                'linhadigitavelsgv': item['linhaDigitavelSgv'],
                'nossonumero': item['nossoNumero'],
                'linhadigitavelprorrogacao': item['linhaDigitavelProrrogacao'],
                'datacontratacao': item['dataContratacao'],
                'dataprimeiracontratacao': item['dataPrimeiraContratacao'],
                'clienteidsgv': item['clienteIdSgv'],
                'clientedacontratacao': item['clienteDaContratacao'],
                'scorecliente': item['scoreCliente'],
                'nomeempresa': item['nomeEmpresa'],
                'cobrancaid': item['cobrancaId'],
                'valorboletosgv': item['valorBoletoSgv'],
                'vencimentoboletosgv': item['vencimentoBoletoSgv'],
                'valorboletoprorrogacao': item['valorBoletoProrrogacao'],
                'valorrepassegrupocard': item['valorRepasseGrupoCard'],
                'datarepassemoneygc': item['dataRepasseMoneyGc'],
                'vencimentoboletoprorrogacao': item['vencimentoBoletoProrrogacao'],
                'prazo': item['prazo'],
                'datapagamentoprorrogacao': item['dataPagamentoProrrogacao'],
                'dia_consulta': item['dia_consulta'],
                'intervalo_consulta': item['intervalo_consulta']
            }
            lista.append(objeto)
        df = pd.DataFrame(lista, columns=[
            'id',
            'statusdacontratacao',
            'cpfcnpj',
            'linhadigitavelsgv',
            'nossonumero',
            'linhadigitavelprorrogacao',
            'datacontratacao',
            'dataprimeiracontratacao',
            'clienteidsgv',
            'clientedacontratacao',
            'scorecliente',
            'nomeempresa',
            'cobrancaid',
            'valorboletosgv',
            'vencimentoboletosgv',
            'valorboletoprorrogacao',
            'valorrepassegrupocard',
            'datarepassemoneygc',
            'vencimentoboletoprorrogacao',
            'prazo',
            'datapagamentoprorrogacao',
            'dia_consulta',
            'intervalo_consulta'
        ])

        return df
    except Exception as error:
        print(error)

def relatorio_extrato(data):
    lista = []
    try:
        info = Item.objects.using('adm_int').exclude(
            dataLancto__gte=date.today()
        ).filter(
            dataLancto__gte=data
        ).filter(
            complemento__contains='Tecfin'
        ).filter(
            contaContraparte__isnull=True
        ).values()
        for item in info:
            objeto = {
                'natureza': item['natureza'],
                'datalancto': item['dataLancto'],
                'nrdocumento': item['nrDocumento'],
                'cpfcnpj': item['cpfCnpj'],
                'nomecontraparte': item['nomeContraparte'],
                'agenciacontraparte': item['agenciaContraparte'],
                'contacontraparte': item['contaContraparte'],
                'valor': item['valor'],
                'saldoatual': item['saldoAtual'],
                'saldoanterior': item['saldoAnterior'],
                'tipooperacao': item['tipoOperacao'],
                'id': item['id'],
                'descricao': item['descricao'],
                'complemento': item['complemento'],
                'categoria': item['categoria'],
                'codigo': item['codigo'],
                'dia_consulta': item['dia_consulta'],
                'intervalo_consulta': item['intervalo_consulta']
            }
            lista.append(objeto)
        df = pd.DataFrame(lista, columns=[
            'natureza',
            'datalancto',
            'nrdocumento',
            'cpfcnpj',
            'nomecontraparte',
            'agenciacontraparte',
            'contacontraparte',
            'valor',
            'saldoatual',
            'saldoanterior',
            'tipooperacao',
            'id',
            'descricao',
            'complemento',
            'categoria',
            'codigo',
            'dia_consulta',
            'intervalo_consulta'
        ])
        
        return df
    except Exception as error:
        print(error)