from datetime import date
from django.shortcuts import render 
from tecfin_models import Prorrogacao
from django.contrib.auth.decorators import login_required
from salva_relatorios import salva_relatorios
from tecfin_consultas import soma_boletosSGV, soma_repasseCARD
from rendimento_consultas import soma_valoresExtratoRendimento, get_moneyplus
from tecfin_funcoes import get_cobrancas_tecfin, data_formatada, get_cobrancas_ids

@login_required
def index_tecfin(request):
    hoje = date.today().strftime('%d-%m-%Y')
    lista_dicionarios = []
    lista_cobrancas = get_cobrancas_tecfin()
    try:
        for prorrogacao in lista_cobrancas:
            Prorrogacao.objects.using('adm_int').create(
                id=prorrogacao['id'],
                statusDaContratacao=prorrogacao['statusDaContratacao'],
                cpfCnpj=prorrogacao['cpfCnpj'],
                linhaDigitavelSgv=prorrogacao['linhaDigitavelSgv'],
                nossoNumero=prorrogacao['nossoNumero'],
                linhaDigitavelProrrogacao=prorrogacao['linhaDigitavelProrrogacao'],
                dataContratacao=prorrogacao['dataContratacao'],
                dataPrimeiraContratacao=prorrogacao['dataPrimeiraContratacao'],
                clienteIdSgv=prorrogacao['clienteIdSgv'],
                clienteDaContratacao=prorrogacao['clinteDaContratacao'],
                scoreCliente=prorrogacao['scoreCliente'],
                nomeEmpresa=prorrogacao['nomeEmpresa'],
                cobrancaId=prorrogacao['cobrancaId'],
                valorBoletoSgv=prorrogacao['valorBoletoSgv'],
                vencimentoBoletoSgv=prorrogacao['vencimentoBoletoSgv'],
                valorBoletoProrrogacao=prorrogacao['valorBoletoProrrogacao'],
                valorRepasseGrupoCard=prorrogacao['valorRepasseGrupoCard'],
                dataRepasseMoneyGc=prorrogacao['dataRepasseMoneyGc'],
                vencimentoBoletoProrrogacao=prorrogacao['vencimentoBoletoProrrogacao'],
                prazo=prorrogacao['prazo'],
                dataPagamentoProrrogacao=prorrogacao['dataPagamentoProrrogacao'],
                dia_consulta=hoje,
                intervalo_consulta=data_formatada()
            )
            dicionario = {
                "id": prorrogacao['id'],
                "statusDaContratacao": prorrogacao['statusDaContratacao'],
                "cpfCnpj": prorrogacao['cpfCnpj'],
                "linhaDigitavelSgv": prorrogacao['linhaDigitavelSgv'],
                "nossoNumero": prorrogacao['nossoNumero'],
                "linhaDigitavelProrrogacao": prorrogacao['linhaDigitavelProrrogacao'],
                "dataContratacao": prorrogacao['dataContratacao'],
                "dataPrimeiraContratacao": prorrogacao['dataPrimeiraContratacao'],
                "clienteIdSgv": prorrogacao['clienteIdSgv'],
                "clinteDaContratacao": prorrogacao['clinteDaContratacao'],
                "scoreCliente": prorrogacao['scoreCliente'],
                "nomeEmpresa": prorrogacao['nomeEmpresa'],
                "cobrancaId": prorrogacao['cobrancaId'],
                "valorBoletoSgv": prorrogacao['valorBoletoSgv'],
                "vencimentoBoletoSgv": prorrogacao['vencimentoBoletoSgv'],
                "valorBoletoProrrogacao": prorrogacao['valorBoletoProrrogacao'],
                "valorRepasseGrupoCard": prorrogacao['valorRepasseGrupoCard'],
                "dataRepasseMoneyGc": prorrogacao['dataRepasseMoneyGc'],
                "vencimentoBoletoProrrogacao": prorrogacao['vencimentoBoletoProrrogacao'],
                "prazo": prorrogacao['prazo'],
                "dataPagamentoProrrogacao": prorrogacao['dataPagamentoProrrogacao'],
                "dia_consulta": hoje,
                "intervalo_consulta": data_formatada()
            }
            lista_dicionarios.append(dicionario)
        context = {
            'usuario': request.user.first_name,
            'segment': 'apps_tecfin_dashboard',
            'prorrogacoes': lista_dicionarios
        }

        return render(request, 'tecfin/index.html', context)
    except Exception as error:
        print(error)


@login_required
def valida_cobrancas(request):
    lista_validas = get_cobrancas_ids()
    if not lista_validas:
        print("ERRO! Lista de ID's retornou vazia, checar consulta no BD.")
        context = {'Validas': []}
        return render(request, 'tecfin/erro404.html', context)
    else:
        try:
            soma_prorrogacoes = soma_boletosSGV()
            soma_cobrancas = soma_valoresExtratoRendimento()
            if soma_prorrogacoes == soma_cobrancas:
                print(f"Valores validados. Soma dos boletos SGV: R${soma_prorrogacoes} e soma cobranças do extrato: R${soma_cobrancas}")
            else:
                print(f"Valores não validados. Soma dos boletos SGV: R${soma_prorrogacoes} e soma cobranças do extrato: R${soma_cobrancas}")
            soma_repasse = soma_repasseCARD()
            moneyplus = get_moneyplus()
            if moneyplus is None:
                pass 
            else:
                for item in moneyplus:
                    x = float(item['valor'])
                    if x == soma_repasse:
                        print(f"Valor MoneyPlus: R${x} validado com o total repassado a Card: R${soma_repasse}")
                        break
                    else:
                        pass
            salva_relatorios()
            context = {'Validas': lista_validas}

            return render(request, 'tecfin/valida_cobranca.html', context)
        except Exception as error:
            print(error)

                
