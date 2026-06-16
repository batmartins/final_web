import requests

codigo_host = "http://10.135.232.7:5001"


def post_clientes(nome, email, senha, endereco):
    url = f"{codigo_host}/cadastro_clientes"

    dados = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "endereco": endereco
    }

    response = requests.post(url, json=dados)

    return response.json()


def get_clientes():
    url = f"{codigo_host}/buscar_clientes"

    response = requests.get(url)

    return response.json()


def post_encomendas(nome, fragilidade, tipo, remetente):
    url = f"{codigo_host}/cadastro_clientes"

    dados = {
        "nome": nome,
        "fragilidade": fragilidade,
        "tipo": tipo,
        "remetente": remetente
    }

    response = requests.post(url, json=dados)

    return response.json()


def get_encomendas():
    url = f"{codigo_host}/listar_encomendas"

    response = requests.get(url)

    return response.json()


def post_usuario(nome, email, senha, ):
    url = f"{codigo_host}/cadastro_usuario"

    dados = {
        "nome": nome,
        "email": email,
        "senha": senha
    }
    response = requests.post(url, json=dados)

    return response.json()
def get_usuarios():

    url = f"{codigo_host}/buscar_usuarios"

    response = requests.get(url)

    return response.json()



def post_entregador(nome, veiculo ):
    url = f"{codigo_host}/cadastro_entregador"

    dados = {
        "nome": nome,
        "veiculo": veiculo
    }

    response = requests.post(url, json=dados)
    return response.json()

def get_entregadores():
    url = f"{codigo_host}/buscar_entregadores"

    response = requests.get(url)

    return response.json()


def post_movimentacao(situacao, codigo_rastreio, galpao_id):
    url = f"{codigo_host}/cadastro_movimentacao"

    dados = {
        "situacao": situacao,
        "codigo_rastreio": codigo_rastreio,
        "galpao_id": galpao_id
    }

    response = requests.post(url, json=dados)

    return response.json()


def get_galpao():
    url = f"{codigo_host}/buscar_galpao/1"

    response = requests.get(url)

    return response.json()

def get_galpoes():
    url = f"{codigo_host}/listar_galpoes"

    response = requests.get(url)

    return response.json()

def get_movimentacao():
    url = f"{codigo_host}/buscar_movimentacao"

    response = requests.get(url)

    return response.json()


def post_galpao(nome, localizacao, capacidade):
    url = f"{codigo_host}/buscar_galpao"

    dados = {
        "nome": nome,
        "localizacao": localizacao,
        "capacidade": capacidade
    }

    response = requests.post(url, json=dados)

    return response.json()


def put_usuario(id, nome, email, senha):
    url = f"{codigo_host}/editar_usuario"

    dados = {
        "id": id,
        "nome": nome,
        "email": email,
        "senha": senha
    }

    response = requests.put(url, json=dados)

    return response.json()

def put_encomenda(id_, nome_, fragilidade_, tipo_, remetente_):
    url = f"{codigo_host}/editar_encomenda"

    dados = {
        "id_": id_,
        "nome_": nome_,
        "fragilidade_": fragilidade_,
        "tipo_": tipo_,
        "remetente_": remetente_
    }

    response = requests.put(url, json=dados)

    return response.json()



def put_cliente(id_, nome_, email_, senha_, endereco_, produto_):
    url = f"{codigo_host}/editar_cliente"

    dados = {
        "id_": id_,
        "nome": nome_,
        "email": email_,
        "senha": senha_,
        "endereco": endereco_,
        "produto": produto_
    }

    response = requests.put(url, json=dados)

    return response.json()


def put_entregador(id, nome, veiculo):
    url = f"{codigo_host}/editar_entregador"

    dados = {
        "id": id,
        "nome": nome,
        "veiculo": veiculo
    }

    response = requests.put(url, json=dados)

    return response.json()

def put_galpao(id_, nome_, locaizacao_, capacidade_):
    url = f"{codigo_host}/buscar_galpao"

    dados = {
        "id": id_,
        "nome": nome_,
        "localizacao": locaizacao_,
        "capacidade": capacidade_
    }

    response = requests.put(url, json=dados)

    return response.json()


