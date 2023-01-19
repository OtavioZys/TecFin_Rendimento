import requests 
from configs import RENDIMENTO_USER, RENDIMENTO_ACCESSKEY, RENDIMENTO_ENCODED_AUTH, RENDIMENTO_DOMAIN, RENDIMENTO_TOKEN_ENDPOINT, RENDIMENTO_EXTRATO_ENDPOINT

def get_token():
    urllogin = f"{RENDIMENTO_DOMAIN}{RENDIMENTO_TOKEN_ENDPOINT}"
    payload = 'grant-type=client_credentials'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': RENDIMENTO_ENCODED_AUTH
    }

    response = requests.request("POST", urllogin, headers=headers, data=payload)
    if response.status_code == 200:
        token = response.json()
        token = token['access_token']
        return token
    else:
        print(f'ERRO! API get_token Rendimento retornou erro HTTP {response.status_code}')
        return 0


def get_extrato(data):
    url = f'{RENDIMENTO_DOMAIN}{RENDIMENTO_EXTRATO_ENDPOINT}?dataInicio={data}&dataFinal={data}'
    token = get_token()
    headers = {
        'ChaveAcesso': RENDIMENTO_ACCESSKEY,
        'access_token': token,
        'Content-Type': 'application/json',
        'dataInicio': data,
        'dataFinal': data,
        'client_id': RENDIMENTO_USER,
        'Authorization': RENDIMENTO_ENCODED_AUTH
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'ERRO! API get_extrato Rendimento retornou erro HTTP {response.status_code}')
        return []