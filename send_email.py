import io
import pandas as pd
from post_office import mail
from apps.tecfin.models import LogTecfin
from datetime import date, timedelta, datetime
from apps.tecfin.relatorios_tecfin import cobrancasId_tecfin, cobrancasId_extrato, relatorio_tecfin


def envia_relatorios():
    extrato = cobrancasId_extrato()
    tecfin = cobrancasId_tecfin()
    if len(extrato) == len(tecfin):
        dia = int((date.today()).strftime('%w'))
        relatorio_normal = []
        if dia == 1:
            sexta = date.today() - timedelta(days=3)
            tecfin = relatorio_tecfin(sexta)
            for item in tecfin:
                dc_aware = item['dataContratacao']
                dc_unaware = dc_aware.replace(tzinfo=None)
                objeto = {
                    'Cobrança ID': item['cobrancaId'],
                    'Nosso Número': item['nossoNumero'],
                    'Data da Contratação': dc_unaware,
                    'Dia da Consulta': item['dia_consulta'],
                    'Intervalo da Consulta': item['intervalo_consulta'],
                    'ID Cliente SGV': item['clienteIdSgv'],
                    'Cliente da Contratação': item['clienteDaContratacao'],
                    'Nome da Empresa': item['nomeEmpresa'],
                    'Valor do Boleto SGV': float(item['valorBoletoSgv']),
                    'Valor do Repasse Grupo Card': float(item['valorRepasseGrupoCard'])
                }
                relatorio_normal.append((objeto))
            df = pd.DataFrame(relatorio_normal, columns=[
                'Cobrança ID',
                'Nosso Número',
                'Data da Contratação',
                'Dia da Consulta',
                'Intervalo da Consulta',
                'ID Cliente SGV',
                'Cliente da Contratação',
                'Nome da Empresa',
                'Valor do Boleto SGV',
                'Valor do Repasse Grupo Card',
            ])
            dt_file_sexta = (date.today() - timedelta(days=3)).strftime('%d-%m')
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)
            mail.send(
                targets,
                sender,
                subject=f"Relatório TecFin {dt_file_sexta}",
                message=f"""
                Olá,\
        
                Segue em anexo o relatório TecFin do dia {dt_file_sexta} para validação.
                """,
                html_message=f"""
                Olá,\
        
                Segue em anexo o relatório TecFin do dia {dt_file_sexta} para validação.
                """,
                attachments={
                    f'tecfin_{dt_file_sexta}.xlsx': buffer
                }
            )
        else:
            ontem = date.today() - timedelta(days=1)
            tecfin = relatorio_tecfin(ontem)
            for item in tecfin:
                dc_aware = item['dataContratacao']
                dc_unaware = dc_aware.replace(tzinfo=None)
                objeto = {
                    'Cobrança ID': item['cobrancaId'],
                    'Nosso Número': item['nossoNumero'],
                    'Data da Contratação': dc_unaware,
                    'Dia da Consulta': item['dia_consulta'],
                    'Intervalo da Consulta': item['intervalo_consulta'],
                    'ID Cliente SGV': item['clienteIdSgv'],
                    'Cliente da Contratação': item['clienteDaContratacao'],
                    'Nome da Empresa': item['nomeEmpresa'],
                    'Valor do Boleto SGV': float(item['valorBoletoSgv']),
                    'Valor do Repasse Grupo Card': float(item['valorRepasseGrupoCard']),
                }
                relatorio_normal.append((objeto))
            df = pd.DataFrame(relatorio_normal, columns=[
                'Cobrança ID',
                'Nosso Número',
                'Data da Contratação',
                'Dia da Consulta',
                'Intervalo da Consulta',
                'ID Cliente SGV',
                'Cliente da Contratação',
                'Nome da Empresa',
                'Valor do Boleto SGV',
                'Valor do Repasse Grupo Card',
            ])
            dt_file_ontem = (date.today() - timedelta(days=1)).strftime('%d-%m')
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)
            mail.send(
                targets,
                sender,
                subject=f"Relatório TecFin {dt_file_ontem}",
                message=f"""
                        Olá,\
    
                        Segue em anexo o relatório TecFin do dia {dt_file_ontem} para validação.
                        """,
                html_message=f"""
                        Olá,\
    
                        Segue em anexo o relatório TecFin do dia {dt_file_ontem} para validação.
                        """,
                attachments={
                    f'tecfin_{dt_file_ontem}.xlsx': buffer
                }
            )
    else:
        dia = int((date.today()).strftime('%w'))
        if len(extrato) == 1:
            print(f"Extrato possui somente {len(extrato)} cobrança.")
        else:
            print(f"Extrato possui {len(extrato)} cobranças.")
        if len(tecfin) == 1:
            print(f"TecFin possui somente {len(tecfin)} cobrança.")
        else:
            print(f"TecFin possui {len(tecfin)} cobranças.")
        res = [x for x in extrato + tecfin if x not in extrato or x not in tecfin]
        print(f"Cobranças não validadas entre as origens: {res}")
        relatorio_diferenca = []
        if dia == 1:
            sexta = date.today() - timedelta(days=3)
            tecfin = relatorio_tecfin(sexta)
            for item in tecfin:
                dc_aware = item['dataContratacao']
                dc_unaware = dc_aware.replace(tzinfo=None)
                objeto = {
                    'Cobrança ID': item['cobrancaId'],
                    'Cobranças não validadas': res,
                    'Quantidade de Cobranças no Extrato': len(extrato),
                    'Quantidade de Cobranças da TecFin': len(tecfin),
                    'Nosso Número': item['nossoNumero'],
                    'Data da Contratação': dc_unaware,
                    'Dia da Consulta': item['dia_consulta'],
                    'Intervalo da Consulta': item['intervalo_consulta'],
                    'ID Cliente SGV': item['clienteIdSgv'],
                    'Cliente da Contratação': item['clienteDaContratacao'],
                    'Nome da Empresa': item['nomeEmpresa'],
                    'Valor do Boleto SGV': item['valorBoletoSgv'],
                    'Valor do Repasse Grupo Card': item['valorRepasseGrupoCard'],
                }
                relatorio_diferenca.append((objeto))
            df = pd.DataFrame(relatorio_diferenca, columns=[
                'Cobrança ID',
                'Cobranças não validadas',
                'Quantidade de Cobranças no Extrato',
                'Quantidade de Cobranças da TecFin',
                'Nosso Número',
                'Data da Contratação',
                'Dia da Consulta',
                'Intervalo da Consulta',
                'ID Cliente SGV',
                'Cliente da Contratação',
                'Nome da Empresa',
                'Valor do Boleto SGV',
                'Valor do Repasse Grupo Card',
            ])
            dt_file_sexta = (date.today() - timedelta(days=3)).strftime('%d-%m')
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)
            mail.send(
                targets,
                sender,
                subject=f"Relatório TecFin {dt_file_sexta}",
                message=f"""
                        Olá,\

                        Segue em anexo o relatório TecFin do dia {dt_file_sexta} para validação. Notar que as cobranças {res} foram identificadas em inconformidade nas origens!
                        """,
                html_message=f"""
                        Olá,\

                        Segue em anexo o relatório TecFin do dia {dt_file_sexta} para validação. Notar que as cobranças {res} foram identificadas em inconformidade nas origens!
                        """,
                attachments={
                    f'tecfin_{dt_file_sexta}.xlsx': buffer
                }
            )
        else:
            ontem = date.today() - timedelta(days=1)
            tecfin = relatorio_tecfin(ontem)
            dt_file_ontem = (date.today() - timedelta(days=1)).strftime('%d-%m')
            for item in tecfin:
                dc_aware = item['dataContratacao']
                dc_unaware = dc_aware.replace(tzinfo=None)
                objeto = {
                    'Cobrança ID': item['cobrancaId'],
                    'Cobranças não validadas': res,
                    'Quantidade de Cobranças no Extrato': len(extrato),
                    'Quantidade de Cobranças da TecFin': len(tecfin),
                    'Nosso Número': item['nossoNumero'],
                    'Data da Contratação': dc_unaware,
                    'Dia da Consulta': item['dia_consulta'],
                    'Intervalo da Consulta': item['intervalo_consulta'],
                    'ID Cliente SGV': item['clienteIdSgv'],
                    'Cliente da Contratação': item['clienteDaContratacao'],
                    'Nome da Empresa': item['nomeEmpresa'],
                    'Valor do Boleto SGV': item['valorBoletoSgv'],
                    'Valor do Repasse Grupo Card': item['valorRepasseGrupoCard'],
                }
                relatorio_diferenca.append((objeto))
            df = pd.DataFrame(relatorio_diferenca, columns=[
                'Cobrança ID',
                'Cobranças não validadas',
                'Quantidade de Cobranças no Extrato',
                'Quantidade de Cobranças da TecFin',
                'Nosso Número',
                'Data da Contratação',
                'Dia da Consulta',
                'Intervalo da Consulta',
                'ID Cliente SGV',
                'Cliente da Contratação',
                'Nome da Empresa',
                'Valor do Boleto SGV',
                'Valor do Repasse Grupo Card',
            ])
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)
            mail.send(
                targets,
                sender,
                subject=f"Relatório TecFin {dt_file_ontem}",
                message=f"""
                                Olá,\

                                Segue em anexo o relatório TecFin do dia {dt_file_ontem} para validação. Notar que as cobranças {res} foram identificadas em inconformidade nas origens!
                                """,
                html_message=f"""
                                Olá,\

                                Segue em anexo o relatório TecFin do dia {dt_file_ontem} para validação. Notar que as cobranças {res} foram identificadas em inconformidade nas origens!
                                """,
                attachments={
                    f'tecfin_{dt_file_ontem}.xlsx': buffer
                }
            )


def alerta_erro(codigo, erro, api):
    error = f'API {api} da TecFin retornou o seguinte erro : {erro} - Código {codigo}'
    mail.send(
        targets,
        sender,
        subject=f"!!!ERRO API TECFIN!!! Código de erro: {codigo}",
        message=f"""
                    ATENÇÃO,\
                    
                    API {api}: {erro}!
                    """
    )
    err = LogTecfin.objects.using('adm_int').create(
        processo="tecfin",
        data_registro=date.today(),
        data_hora_registro=datetime.now(),
        erro=error
    )
    print(err)

