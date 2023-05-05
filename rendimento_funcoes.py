import locale
from datetime import datetime, timedelta, date
from time import sleep

from apps.extrato.models import Item
from apps.extrato.getters import get_extrato

locale.setlocale(locale.LC_ALL, '')


def data_formatada_extrato():
    data = int(date.today().strftime('%w'))
    if data == 1:
        ano = int(date.today().strftime('%Y'))
        mes = int((date.today() - timedelta(days=4)).strftime('%m'))
        dia1 = int((date.today() - timedelta(days=3)).strftime('%d'))
        dia2 = int((date.today() - timedelta(days=4)).strftime('%d'))
        form23 = datetime(year=ano, month=mes, day=dia2, hour=23, minute=0, second=0)
        form22 = datetime(year=ano, month=mes, day=dia1, hour=22, minute=59, second=59)
        sexta_format = f'{form23} à {form22}'

        return sexta_format
    else:
        ano = int(date.today().strftime('%Y'))
        mes = int((date.today() - timedelta(days=2)).strftime('%m'))
        dia1 = int((date.today() - timedelta(days=1)).strftime('%d'))
        dia2 = int((date.today() - timedelta(days=2)).strftime('%d'))
        form23 = datetime(year=ano, month=mes, day=dia2, hour=23, minute=0, second=0)
        form22 = datetime(year=ano, month=mes, day=dia1, hour=22, minute=59, second=59)
        ontem_format = f'{form23} à {form22}'

        return ontem_format


def checa_dia_extrato(filtro):
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
    """
    VERIFICA DIA, SE SEGUNDA FAZ BAIXA DO EXTRATO DE SEXTA, DO CONTRÁRIO FAZ BAIXA DO DIA ANTERIOR NORMALMENTE, PRIMEIRA VERIFICAÇÃO VALIDA SE JÁ HOUVE REGISTRO DO DADO
    TABELA POR MEIO DO CAMPO NRDOCUMENTO. A SEGUNDA VALIDAÇÃO VERIFICA SE O REGISTRO É DO TIPO MONEYPLUS, SE SIM VERIFICA SE O CAMPO NOMECONTRAPARTE É NULO, SE SIM PREENCHE
    O CAMPO
    """
    data = int(date.today().strftime('%w'))
    if data == 1:
        sexta = (date.today() - timedelta(days=3)).strftime('%m-%d-%Y')
        feriado = checa_dia_extrato(3)
        if feriado:
            return []
        else:
            lista_cobrancas = []
            try:
                print(sexta)
                lista_value_sexta = get_extrato(sexta)
                for cobranca in lista_value_sexta['itens']:
                    qs = Item.objects.using('adm_int').filter(nrDocumento=cobranca['nrDocumento']).values()
                    if qs:
                        print(f"Documento já inserido na tabela: {cobranca['nrDocumento']}")
                    else:
                        if cobranca['natureza'] == 'C' and cobranca['cpfCnpj'] == 'cpf_client' and cobranca[
                            'agenciaContraparte'] == '00000' and cobranca['contaContraparte'] == '0000000000':
                            if not cobranca['nomeContraparte'] or cobranca['nomeContraparte'] == '' or cobranca[
                                'nomeContraparte'] is None:
                                moneyplus_sem_nomeContraparte = {
                                    'natureza': cobranca['natureza'],
                                    'dataLancto': cobranca['dataLancto'],
                                    'nrDocumento': cobranca['nrDocumento'],
                                    'cpfCnpj': cobranca['cpfCnpj'],
                                    'nomeContraparte': 'MONEY PLUS SCM',
                                    'agenciaContraparte': cobranca['agenciaContraparte'],
                                    'contaContraparte': cobranca['contaContraparte'],
                                    'valor': cobranca['valor'],
                                    'saldoAtual': cobranca['saldoAtual'],
                                    'saldoAnterior': cobranca['saldoAnterior'],
                                    'tipoOperacao': cobranca['tipoOperacao'],
                                    'codigo': cobranca['historico']['codigo'],
                                    'descricao': cobranca['historico']['descricao'],
                                    'complemento': cobranca['historico']['complemento'],
                                    'categoria': cobranca['historico']['categoria'],
                                }
                                lista_cobrancas.append(moneyplus_sem_nomeContraparte)
                            else:
                                moneyplus_com_nomeContraparte = {
                                    'natureza': cobranca['natureza'],
                                    'dataLancto': cobranca['dataLancto'],
                                    'nrDocumento': cobranca['nrDocumento'],
                                    'cpfCnpj': cobranca['cpfCnpj'],
                                    'nomeContraparte': cobranca['nomeContraparte'],
                                    'agenciaContraparte': cobranca['agenciaContraparte'],
                                    'contaContraparte': cobranca['contaContraparte'],
                                    'valor': cobranca['valor'],
                                    'saldoAtual': cobranca['saldoAtual'],
                                    'saldoAnterior': cobranca['saldoAnterior'],
                                    'tipoOperacao': cobranca['tipoOperacao'],
                                    'codigo': cobranca['historico']['codigo'],
                                    'descricao': cobranca['historico']['descricao'],
                                    'complemento': cobranca['historico']['complemento'],
                                    'categoria': cobranca['historico']['categoria'],
                                }
                                lista_cobrancas.append(moneyplus_com_nomeContraparte)
                        else:
                            dictio = {
                                'natureza': cobranca['natureza'],
                                'dataLancto': cobranca['dataLancto'],
                                'nrDocumento': cobranca['nrDocumento'],
                                'cpfCnpj': cobranca['cpfCnpj'],
                                'nomeContraparte': cobranca['nomeContraparte'],
                                'agenciaContraparte': cobranca['agenciaContraparte'],
                                'contaContraparte': cobranca['contaContraparte'],
                                'valor': cobranca['valor'],
                                'saldoAtual': cobranca['saldoAtual'],
                                'saldoAnterior': cobranca['saldoAnterior'],
                                'tipoOperacao': cobranca['tipoOperacao'],
                                'codigo': cobranca['historico']['codigo'],
                                'descricao': cobranca['historico']['descricao'],
                                'complemento': cobranca['historico']['complemento'],
                                'categoria': cobranca['historico']['categoria'],
                            }
                            lista_cobrancas.append(dictio)
                return lista_cobrancas
            except Exception as error:
                print(error)
                return []
       else:
        # ontem = (datetime.now() - timedelta(days=1)).replace(microsecond=0)
        ontem = (date.today() - timedelta(days=1)).strftime('%m-%d-%Y')
        feriado = checa_dia_extrato(1)
        if feriado:
            return []
        else:
            lista_cobrancas = []
            try:
                lista_value = get_extrato(ontem)
                for cobranca in lista_value['itens']:
                    qs = Item.objects.using('adm_int').filter(nrDocumento=cobranca['nrDocumento']).values()
                    if qs:
                        print(f"Documento já inserido na tabela: {cobranca['nrDocumento']}")
                    else:
                        if cobranca['natureza'] == 'C' and cobranca['cpfCnpj'] == 'cpf_client' and cobranca[
                            'agenciaContraparte'] == '00000' and cobranca['contaContraparte'] == '0000000000':
                            if not cobranca['nomeContraparte'] or cobranca['nomeContraparte'] == '' or cobranca[
                                'nomeContraparte'] is None:
                                moneyplus_sem_nomeContraparte = {
                                    'natureza': cobranca['natureza'],
                                    'dataLancto': cobranca['dataLancto'],
                                    'nrDocumento': cobranca['nrDocumento'],
                                    'cpfCnpj': cobranca['cpfCnpj'],
                                    'nomeContraparte': 'MONEY PLUS SCM',
                                    'agenciaContraparte': cobranca['agenciaContraparte'],
                                    'contaContraparte': cobranca['contaContraparte'],
                                    'valor': cobranca['valor'],
                                    'saldoAtual': cobranca['saldoAtual'],
                                    'saldoAnterior': cobranca['saldoAnterior'],
                                    'tipoOperacao': cobranca['tipoOperacao'],
                                    'codigo': cobranca['historico']['codigo'],
                                    'descricao': cobranca['historico']['descricao'],
                                    'complemento': cobranca['historico']['complemento'],
                                    'categoria': cobranca['historico']['categoria'],
                                }
                                lista_cobrancas.append(moneyplus_sem_nomeContraparte)
                            else:
                                moneyplus_com_nomeContraparte = {
                                    'natureza': cobranca['natureza'],
                                    'dataLancto': cobranca['dataLancto'],
                                    'nrDocumento': cobranca['nrDocumento'],
                                    'cpfCnpj': cobranca['cpfCnpj'],
                                    'nomeContraparte': cobranca['nomeContraparte'],
                                    'agenciaContraparte': cobranca['agenciaContraparte'],
                                    'contaContraparte': cobranca['contaContraparte'],
                                    'valor': cobranca['valor'],
                                    'saldoAtual': cobranca['saldoAtual'],
                                    'saldoAnterior': cobranca['saldoAnterior'],
                                    'tipoOperacao': cobranca['tipoOperacao'],
                                    'codigo': cobranca['historico']['codigo'],
                                    'descricao': cobranca['historico']['descricao'],
                                    'complemento': cobranca['historico']['complemento'],
                                    'categoria': cobranca['historico']['categoria'],
                                }
                                lista_cobrancas.append(moneyplus_com_nomeContraparte)
                        else:
                            dictio = {
                                'natureza': cobranca['natureza'],
                                'dataLancto': cobranca['dataLancto'],
                                'nrDocumento': cobranca['nrDocumento'],
                                'cpfCnpj': cobranca['cpfCnpj'],
                                'nomeContraparte': cobranca['nomeContraparte'],
                                'agenciaContraparte': cobranca['agenciaContraparte'],
                                'contaContraparte': cobranca['contaContraparte'],
                                'valor': cobranca['valor'],
                                'saldoAtual': cobranca['saldoAtual'],
                                'saldoAnterior': cobranca['saldoAnterior'],
                                'tipoOperacao': cobranca['tipoOperacao'],
                                'codigo': cobranca['historico']['codigo'],
                                'descricao': cobranca['historico']['descricao'],
                                'complemento': cobranca['historico']['complemento'],
                                'categoria': cobranca['historico']['categoria'],
                            }
                            lista_cobrancas.append(dictio)
                return lista_cobrancas
            except Exception as error:
                print(error)
                return []
