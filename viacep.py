import requests

def buscar_endereco(cep):
    endereco = f"viacep.com.br/ws/{cep}/json/"

    result = requests.get(endereco)

    return result.json()