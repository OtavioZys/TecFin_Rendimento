from time import sleep
from datetime import date 
from rendimento_models import Item
from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from rendimento_funcoes import get_cobrancas_rendimento, data_formatada

@login_required
def index_extrato(request):
    hoje = date.today().strftime('%d-%m-%Y')
    lista_dicionarios = []
    lista_cobrancas = get_cobrancas_rendimento()
    try:
        for cobranca in lista_cobrancas:
            Item.objects.using('adm_int').create(
                natureza=cobranca['natureza'],
                dataLancto=cobranca['dataLancto'],
                nrDocumento=cobranca['nrDocumento'],
                cpfCnpj=cobranca['cpfCnpj'],
                nomeContraparte=cobranca['nomeContraparte'],
                agenciaContraparte=cobranca['agenciaContraparte'],
                contaContraparte=cobranca['contaContraparte'],
                valor=cobranca['valor'],
                saldoAtual=cobranca['saldoAtual'],
                saldoAnterior=cobranca['saldoAnterior'],
                tipoOperacao=cobranca['tipoOperacao'],
                codigo=cobranca['codigo'],
                descricao=cobranca['descricao'],
                complemento=cobranca['complemento'],
                categoria=cobranca['categoria'],
                dia_consulta=hoje,
                intervalo_consulta=data_formatada() 
            )
            sleep(1.5)
            dicionario = {
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
                'dia_consulta': hoje,
                'intervalo_consulta': data_formatada() 
            }
            lista_dicionarios.append(dicionario)
        
        context = {
            'usuario': request.user.first_name,
            'segment': 'apps_extrato_dashboard',
            'itens_lista': lista_dicionarios,
        }

        return render(request, 'extrato/index.html', context)
    except Exception as error:
        print(error)