import requests
codigo_host = "http://10.135.232.38:5001"


def PostClientes(nome,email,senha,endereco):
    url = f"{codigo_host}/cadastrar_clientes"


    dados = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "endereco": endereco
    }

    response = requests.post(url, json=dados)

    return response.json()


'''
def get_exemplo():
    url = f"{codigo_host}/get_exemplo"
    
    response = requests.get(url)
    
    return response.json()
'''