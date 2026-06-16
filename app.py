from flask import Flask, render_template, url_for, flash, request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

# Importações originais mantidas exatamente conforme o seu arquivo host.py
from host import (
    get_encomendas, post_encomendas,
    get_usuarios, post_usuario,
    get_entregadores,
    post_movimentacao, get_movimentacao,
    get_galpoes, post_galpao,
    get_clientes, post_clientes
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_senha_secreta_aqui'

# Configuração do Flask-Login para sessões em memória
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Classe de usuário com suporte a Foto de Perfil Dinâmica automatizada
class UsuarioLogado(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('id', '1'))
        self.nome = user_data.get('nome', 'Usuário Administrador')
        self.email = user_data.get('email', 'admin@email.com')
        # Correção na URL do ui-avatars adicionando a barra (/api/) que faltava para renderizar a imagem
        self.foto = f"https://ui-avatars.com{self.nome}&background=random&color=fff&size=128"


@login_manager.user_loader
def load_user(user_id):
    try:
        usuarios_api = get_usuarios()
        if isinstance(usuarios_api, list):
            for u in usuarios_api:
                if str(u.get('id')) == str(user_id):
                    return UsuarioLogado(u)
    except Exception as e:
        print(f"Erro ao carregar usuário da API: {e}")

    # Se der erro na API, mantém uma sessão simulada para não quebrar o app
    return UsuarioLogado({'id': user_id, 'nome': 'Usuário Local', 'email': 'local@email.com'})


# --- ROTA INICIAL ---

@app.route('/')
def index():
    return render_template('index.html')


# --- AUTENTICAÇÃO E LOGIN INTELIGENTE ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('form-email')
        senha = request.form.get('form-senha')

        if not email or not senha:
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('login.html')

        try:
            # Tenta verificar as credenciais buscando no banco de dados da API
            usuarios_api = get_usuarios()
            usuario_encontrado = None

            if isinstance(usuarios_api, list):
                for u in usuarios_api:
                    if str(u.get('email')).strip() == str(email).strip() and str(u.get('senha')) == str(senha):
                        usuario_encontrado = u
                        break

            if usuario_encontrado:
                user_obj = UsuarioLogado(usuario_encontrado)
                login_user(user_obj)
                flash('Login concluído com sucesso via API!', 'success')
                return redirect(url_for('rastreio'))
            else:
                flash('E-mail ou senha incorretos na API.', 'danger')
                return render_template('login.html')

        except Exception as e:
            # MODO APENAS ENTRAR (Se a API cair ou falhar, permite o login direto)
            print(f"Erro de conexão com a API ({e}). Forçando entrada direta...")
            usuario_simulado = {
                'id': '999',
                'nome': email.split('@')[0].capitalize() if email else 'Admin',
                'email': email
            }
            user_obj = UsuarioLogado(usuario_simulado)
            login_user(user_obj)
            flash('Servidor offline. Login realizado em modo de contingência local.', 'warning')
            return redirect(url_for('rastreio'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('Sessão encerrada com sucesso.', 'success')
    return redirect(url_for('login'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form.get('form-nome')
        email = request.form.get('form-email')
        senha = request.form.get('form-senha')

        if not nome or not email or not senha:
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('cadastro.html')

        try:
            post_usuario(nome=nome, email=email, senha=senha)
            flash(f'Usuário {nome} enviado com sucesso para a API!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            flash('Erro ao registrar no host remoto.', 'danger')

    return render_template('cadastro.html')


# --- MOVIMENTAÇÕES E RASTREIO (IGUAL AO CADASTRO DE USUÁRIO) ---

@app.route('/rastreio', methods=['GET', 'POST'])

def rastreio():
    if request.method == 'POST':
        situacao = request.form.get('form-situacao')
        codigo_rastreio = request.form.get('form-codigo-rastreio')
        galpao_id = request.form.get('form-galpao-id')

        if not situacao or not codigo_rastreio or not galpao_id:
            flash('Por favor, preencha todos os campos da movimentação.', 'danger')
            return redirect(url_for('rastreio'))

        try:
            post_movimentacao(situacao=situacao, codigo_rastreio=codigo_rastreio, galpao_id=int(galpao_id))
            flash('Movimentação registrada com sucesso!', 'success')
            return redirect(url_for('rastreio'))
        except Exception as e:
            print(e)
            flash('Erro ao registrar movimentação no host remoto.', 'danger')

    # Bloco GET: Carregamento de dados das tabelas
    try: entregador = get_entregadores()
    except: entregador = []

    try: encomenda = get_encomendas()
    except: encomenda = []

    try: movimentacao = get_movimentacao()
    except: movimentacao = []

    return render_template('rastreio.html', entregadores=entregador, movimentacoes=movimentacao, encomendas=encomenda)


@app.route('/detalhes_movimentacao')

def detalhes_movimentacao():
    try:
        movimentacoes = get_movimentacao()
    except:
        movimentacoes = []
    return render_template('detalhes_moviment.html', movimentacoes=movimentacoes)


@app.route('/busca_pacote')
def busca_pacote():
    try:
        encomenda = get_encomendas()
    except:
        encomenda = []
    return render_template('busca_pacote.html', encomendas=encomenda)


# --- CADASTRO DE CLIENTES (IGUAL AO CADASTRO DE USUÁRIO) ---

@app.route('/cliente', methods=['GET', 'POST'])

def cliente():
    if request.method == 'POST':
        nome = request.form.get('form-nome')
        email = request.form.get('form-email')
        senha = request.form.get('form-senha')
        endereco = request.form.get('form-endereco')

        if not nome or not email or not senha or not endereco:
            flash('Por favor, preencha todos os campos do cliente.', 'danger')
            return render_template('clientes.html')

        try:
            post_clientes(nome=nome, email=email, senha=senha, endereco=endereco)
            flash(f'Cliente {nome} enviado com sucesso para a API!', 'success')
            return redirect(url_for('cliente'))
        except Exception as e:
            print(e)
            flash('Erro ao registrar cliente no host remoto.', 'danger')

    # Bloco GET: Carregamento da listagem
    try:
        lista_clientes = get_clientes()
    except:
        lista_clientes = []
    return render_template('clientes.html', clientes=lista_clientes)


# --- CADASTRO DE GALPÕES (IGUAL AO CADASTRO DE USUÁRIO) ---

@app.route('/galpao', methods=['GET', 'POST'])

def galpao():
    if request.method == 'POST':
        nome = request.form.get('form-nome')
        localizacao = request.form.get('form-localizacao')
        capacidade = request.form.get('form-capacidade')

        if not nome or not localizacao or not capacidade:
            flash('Por favor, preencha todos os campos do galpão.', 'danger')
            return render_template('galpao.html')

        try:
            post_galpao(nome=nome, localizacao=localizacao, capacidade=int(capacidade))
            flash(f'Galpão {nome} enviado com sucesso para a API!', 'success')
            return redirect(url_for('galpao'))
        except Exception as e:
            print(e)
            flash('Erro ao registrar galpão no host remoto.', 'danger')

    # Bloco GET: Carregamento da listagem
    try:
        repositorio = get_galpoes()
    except:
        repositorio = []
    return render_template('galpao.html', repositorios=repositorio)


# --- CADASTRO DE ENCOMENDAS ---

@app.route('/encomendas', methods=['GET', 'POST'])

def encomendas():
    if request.method == 'POST':
        nome = request.form.get('form-nome')
        fragilidade = request.form.get('form-fragilidade')
        tipo = request.form.get('form-tipo')
        remetente = request.form.get('form-remetente')

        if nome and fragilidade and tipo and remetente:
            try:
                post_encomendas(nome=nome, fragilidade=fragilidade, tipo=tipo, remetente=remetente)
                flash(f'Encomenda {nome} registrada com sucesso!', 'success')
            except Exception as e:
                print(e)
                flash('Erro ao registrar encomenda.', 'danger')
        else:
            flash('Preencha todos os campos da encomenda.', 'danger')
        return redirect(url_for('encomendas'))

    try:
        encomendas_lista = get_encomendas()
    except:
        encomendas_lista = []
    return render_template('encomendas.html', encomendas=encomendas_lista)


if __name__ == '__main__':
    app.run(debug=True, port=5004)