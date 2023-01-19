import os
import io 
import locale
from ftplib import *
from pathlib import Path
from datetime import datetime, timedelta, date 
from configs import FTP_HOSTNAME, FTP_USERNAME, FTP_PASSWORD
from get_relatorios import relatorio_extrato, relatorio_tecfin

locale.setlocale(locale.LC_ALL, '')

def salva_relatorios():
    dia = int((date.today()).strftime('%w'))
    ano = (date.today()).strftime('%Y')
    mes = (date.today()).strftime('%B')
    if dia == 1:
        sexta = datetime.now() - timedelta(days=3)
        sexta_form = sexta.strftime('%d-%m')
        tecfin = relatorio_tecfin(sexta)
        extrato = relatorio_extrato(sexta)
        ###############################? RENDIMENTO ######################################################################################
        path_ano_rendimento = Path(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/Rendimento/{ano}")
        if path_ano_rendimento.exists() and path_ano_rendimento.is_dir():
            print(f"Pasta Rendimento de {ano} já existe")
        else:
            directory_rendimento = ano
            parent_dir_rendimento = "/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/Rendimento"
            path_ano_rendimento2 = os.path.join(parent_dir_rendimento, directory_rendimento)
            os.mkdir(path_ano_rendimento2)
            print(f"Pasta Rendimento de {ano} criada")
        path_mes_rendimento = Path(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/Rendimento/{ano}/{mes}")
        if path_mes_rendimento.exists() and path_mes_rendimento.is_dir():
            print(f"Pasta Rendimento de {mes} já existe")
            file_name = f"extrato_rendimento_{sexta_form}.xlsx"
            extrato.to_excel(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/Rendimento/{ano}/{mes}/{file_name}", index=False)
            print(f"Relatório {file_name} criado e salvo")
        else:
            directory_rendimento2 = mes
            parent_dir_rendimento2 = f"/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/Rendimento/{ano}"
            path_mes_rendimento2 = os.path.join(parent_dir_rendimento2, directory_rendimento2)
            os.mkdir(path_mes_rendimento2)
            print(f"Pasta Rendimento de {mes} criada")
            file_name = f"extrato_rendimento_{sexta_form}.xlsx"
            extrato.to_excel(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/Rendimento/{ano}/{mes}/{file_name}", index=False)
            print(f"Relatório {file_name} criado e salvo")
        ################################? TECFIN ##########################################################################################
        path_ano_tecfin = Path(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/TecFin/{ano}")
        if path_ano_tecfin.exists() and path_ano_tecfin.is_dir():
            print(f"Pasta TecFin de {ano} já existe")
        else:
            directory_tecfin = ano
            parent_dir_tecfin = "/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/TecFin"
            path_ano_tecfin2 = os.path.join(parent_dir_tecfin, directory_tecfin)
            os.mkdir(path_ano_tecfin2)
            print(f"Pasta TecFin de {ano} criada")
        path_mes_tecfin = Path(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/TecFin/{ano}/{mes}")
        if path_mes_tecfin.exists() and path_mes_tecfin.is_dir():
            print(f"Pasta TecFin de {mes} já existe")
            file_name = f"tecfin_{sexta_form}.xlsx"
            tecfin.to_excel(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/TecFin/{ano}/{mes}/{file_name}", index=False)
            print(f"Relatório {file_name} criado e salvo")
        else:
            directory_tecfin2 = mes
            parent_dir_tecfin2 = f"/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/TecFin/{ano}"
            path_mes_tecfin2 = os.path.join(parent_dir_tecfin2, directory_tecfin2)
            os.mkdir(path_mes_tecfin2)
            print(f"Pasta TecFin de {mes} criada")
            file_name = f"tecfin_{sexta_form}.xlsx"
            tecfin.to_excel(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/TecFin/{ano}/{mes}/{file_name}", index=False)
            print(f"Relatório {file_name} criado e salvo")
        ################################? CONECTA E SALVA NO FTP CARD #####################################################################
        ftp = FTP(FTP_HOSTNAME)
        ftp.login(user=FTP_USERNAME, passwd=FTP_PASSWORD)
        ftp.encoding = "utf-8"
        ftp.cwd('/Tecfin/')
        buffer = io.BytesIO()
        file_name = f'tecfin_{sexta_form}.xlsx'
        tecfin.to_excel(buffer)
        buffer.seek(0)
        ftp.storbinary(f'STOR {file_name}', buffer)
        print(f"Relatório {file_name} salvo no FTP da Card.")
    else:
        ontem = datetime.now() - timedelta(days=1)
        ontem_form = ontem.strftime('%d-%m')
        tecfin = relatorio_tecfin(ontem)
        extrato = relatorio_extrato(ontem)
        ###############################? RENDIMENTO ######################################################################################
        path_ano_rendimento = Path(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/Rendimento/{ano}")
        if path_ano_rendimento.exists() and path_ano_rendimento.is_dir():
            print(f"Pasta Rendimento de {ano} já existe")
        else:
            directory_rendimento = ano
            parent_dir_rendimento = "/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/Rendimento"
            path_ano_rendimento2 = os.path.join(parent_dir_rendimento, directory_rendimento)
            os.mkdir(path_ano_rendimento2)
            print(f"Pasta Rendimento de {ano} criada")
        path_mes_rendimento = Path(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/Rendimento/{ano}/{mes}")
        if path_mes_rendimento.exists() and path_mes_rendimento.is_dir():
            print(f"Pasta Rendimento de {mes} já existe")
            file_name = f"extrato_rendimento_{ontem_form}.xlsx"
            extrato.to_excel(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/Rendimento/{ano}/{mes}/{file_name}", index=False)
            print(f"Relatório {file_name} criado e salvo")
        else:
            directory_rendimento2 = mes
            parent_dir_rendimento2 = f"/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/Rendimento/{ano}"
            path_mes_rendimento2 = os.path.join(parent_dir_rendimento2, directory_rendimento2)
            os.mkdir(path_mes_rendimento2)
            print(f"Pasta Rendimento de {mes} criada")
            file_name = f"extrato_rendimento_{ontem_form}.xlsx"
            extrato.to_excel(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/Rendimento/{ano}/{mes}/{file_name}", index=False)
            print(f"Relatório {file_name} criado e salvo")
        ################################? TECFIN ##########################################################################################
        path_ano_tecfin = Path(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/TecFin/{ano}")
        if path_ano_tecfin.exists() and path_ano_tecfin.is_dir():
            print(f"Pasta TecFin de {ano} já existe")
        else:
            directory_tecfin = ano
            parent_dir_tecfin = "/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/TecFin"
            path_ano_tecfin2 = os.path.join(parent_dir_tecfin, directory_tecfin)
            os.mkdir(path_ano_tecfin2)
            print(f"Pasta TecFin de {ano} criada")
        path_mes_tecfin = Path(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/TecFin/{ano}/{mes}")
        if path_mes_tecfin.exists() and path_mes_tecfin.is_dir():
            print(f"Pasta TecFin de {mes} já existe")
            file_name = f"tecfin_{ontem_form}.xlsx"
            tecfin.to_excel(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/TecFin/{ano}/{mes}/{file_name}", index=False)
            print(f"Relatório {file_name} criado e salvo")
        else:
            directory_tecfin2 = mes
            parent_dir_tecfin2 = f"/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/TecFin/{ano}"
            path_mes_tecfin2 = os.path.join(parent_dir_tecfin2, directory_tecfin2)
            os.mkdir(path_mes_tecfin2)
            print(f"Pasta TecFin de {mes} criada")
            file_name = f"tecfin_{ontem_form}.xlsx"
            tecfin.to_excel(f"C:/Users/otavio.zys/Desktop/selenium/tecfin/Relatorios/TecFin/{ano}/{mes}/{file_name}", index=False)
        ################################? CONECTA E SALVA NO FTP CARD #####################################################################
        ftp = FTP(FTP_HOSTNAME)
        ftp.login(user=FTP_USERNAME, passwd=FTP_PASSWORD)
        ftp.encoding = "utf-8"
        ftp.cwd('/Tecfin/')
        buffer = io.BytesIO()
        file_name = f'tecfin_{ontem_form}.xlsx'
        tecfin.to_excel(buffer)
        buffer.seek(0)
        ftp.storbinary(f'STOR {file_name}', buffer)
        print(f"Relatório {file_name} salvo no FTP da Card.")