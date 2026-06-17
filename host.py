import requests

codigo_host = "http://127.0.0.1:5001"


# ==========================
# USUÁRIOS
# ==========================

def post_usuario(nome, email, senha):
    url = f"{codigo_host}/cadastro_usuario"

    dados = {
        "nome": nome,
        "email": email,
        "senha": senha
    }

    response = requests.post(url, json=dados)
    return response.json()


def get_usuarios():
    # Sua API não possui /listar_usuarios
    return []


def buscar_usuario(usuario_id):
    url = f"{codigo_host}/buscar_usuario/{usuario_id}"

    response = requests.get(url)
    return response.json()


# ==========================
# CLIENTES
# ==========================

def post_clientes(nome, email, senha, endereco):
    url = f"{codigo_host}/cadastro_cliente"

    dados = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "endereco": endereco
    }

    response = requests.post(url, json=dados)
    return response.json()


def get_clientes():
    url = f"{codigo_host}/listar_clientes"

    response = requests.get(url)
    return response.json()


def buscar_cliente(cliente_id):
    url = f"{codigo_host}/buscar_cliente/{cliente_id}"

    response = requests.get(url)
    return response.json()


# ==========================
# ENCOMENDAS
# ==========================

def post_encomendas(nome, fragilidade, tipo, remetente):
    url = f"{codigo_host}/cadastro_encomendas"

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


def buscar_encomenda(codigo_rastreio):
    url = f"{codigo_host}/buscar_encomenda/{codigo_rastreio}"

    response = requests.get(url)
    return response.json()


# ==========================
# GALPÕES
# ==========================

def post_galpao(nome, localizacao, capacidade):
    url = f"{codigo_host}/cadastro_galpao"

    dados = {
        "nome": nome,
        "localizacao": localizacao,
        "capacidade": capacidade
    }

    response = requests.post(url, json=dados)
    return response.json()


def get_galpoes():
    url = f"{codigo_host}/listar_galpoes"

    response = requests.get(url)
    return response.json()


def buscar_galpao(galpao_id):
    url = f"{codigo_host}/buscar_galpao/{galpao_id}"

    response = requests.get(url)
    return response.json()


# ==========================
# MOVIMENTAÇÕES
# ==========================

def post_movimentacao(situacao, codigo_rastreio, galpao_id):
    url = f"{codigo_host}/cadastro_movimentacao"

    dados = {
        "situacao": situacao,
        "codigo_rastreio": codigo_rastreio,
        "galpao_id": galpao_id
    }

    response = requests.post(url, json=dados)
    return response.json()


def get_movimentacao():
    url = f"{codigo_host}/listar_movimentacoes"

    response = requests.get(url)
    return response.json()


def buscar_movimentacao(codigo_rastreio):
    url = f"{codigo_host}/buscar_movimentacao/{codigo_rastreio}"

    response = requests.get(url)
    return response.json()


# ==========================
# ENTREGADORES
# ==========================

def post_entregador(nome, veiculo):
    url = f"{codigo_host}/cadastro_entregador"

    dados = {
        "nome": nome,
        "veiculo": veiculo
    }

    response = requests.post(url, json=dados)
    return response.json()


def get_entregadores():
    # Sua API não possui /listar_entregadores
    return []


def buscar_entregador(entregador_id):
    url = f"{codigo_host}/buscar_entregador/{entregador_id}"

    response = requests.get(url)
    return response.json()


# ==========================
# CENTRO DE TRANSPORTE
# ==========================

def post_centro_transporte(nome, localizacao):
    url = f"{codigo_host}/cadastro_centro_transporte"

    dados = {
        "nome": nome,
        "localizacao": localizacao
    }

    response = requests.post(url, json=dados)
    return response.json()


def buscar_centro_transporte(centro_id):
    url = f"{codigo_host}/buscar_centro_transporte/{centro_id}"

    response = requests.get(url)
    return response.json()


# ==========================
# VEÍCULOS
# ==========================

def post_veiculo(modelo):
    url = f"{codigo_host}/cadastro_veiculos"

    dados = {
        "modelo": modelo
    }

    response = requests.post(url, json=dados)
    return response.json()


def get_veiculos():
    url = f"{codigo_host}/listar_veiculos"

    response = requests.get(url)
    return response.json()


def buscar_veiculo(veiculo_id):
    url = f"{codigo_host}/buscar_veiculo/{veiculo_id}"

    response = requests.get(url)
    return response.json()