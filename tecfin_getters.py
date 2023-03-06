import json
import requests
from apps.tecfin.send_email import alerta_erro
from integracoes_card.settings import TECFIN_USER, TECFIN_PASSWORD, TECFIN_DOMAIN, TECFIN_LOGIN_ENDPOINT, \
    TECFIN_PRORROGACOES_ENDPOINT


def tecfin_login():
    """
    FAZ LOGIN NA API TECFIN E RETORNA O ACCESS TOKEN
    """
    url = f'{TECFIN_DOMAIN}{TECFIN_LOGIN_ENDPOINT}'
    payload = json.dumps({
        "login": TECFIN_USER,
        "senha": TECFIN_PASSWORD
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        resposta = response.json()
        access_token = resposta['token']['access_token']

        return access_token
    else:
        print(f'ERRO! API tecfin_login retornou erro HTTP {response.status_code}')
        cod = response.status_code
        erro = response.text
        alerta_erro(cod, erro, "tecfin_login")
        return 0


def get_prorrogacoes(data):
    """
    CONECTA NA API TECFIN E RETORNA AS PRORROGAÇÕES DA DATA FORNECIDA
    """
    token = tecfin_login()
    url = f'{TECFIN_DOMAIN}{TECFIN_PRORROGACOES_ENDPOINT}?page=0&size=9000&order=DESC&dataInicial={data}&dataFinal={data}'
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    else:
        print(f'ERRO! API get_prorrogacoes retornou erro HTTP {response.status_code}')
        cod = response.status_code
        erro = response.text
        alerta_erro(cod, erro, "tecfin_prorrogacoes")
        return []
