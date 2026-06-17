# app.py
from flask import Flask, render_template, url_for, flash, request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin

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

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class UsuarioLogado(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('id', '1'))
        self.nome = user_data.get('nome', 'Administrador')
        self.email = user_data.get('email', 'admin@email.com')
        self.foto = f"https://ui-avatars.com/api/?name={self.nome}&background=random&color=fff&size=128"


@login_manager.user_loader
def load_user(user_id):
    try:
        for u in get_usuarios():
            if str(u.get("id")) == str(user_id):
                return UsuarioLogado(u)
    except:
        pass

    return UsuarioLogado({
        "id": user_id,
        "nome": "Usuário Local",
        "email": "local@email.com"
    })


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('form-email')
        senha = request.form.get('form-senha')

        try:
            usuarios = get_usuarios()

            for usuario in usuarios:
                if usuario.get("email") == email:
                    login_user(UsuarioLogado(usuario))
                    flash("Login realizado com sucesso!", "success")
                    return redirect(url_for('rastreio'))

            flash("Usuário não encontrado.", "danger")

        except Exception as e:
            flash(f"Erro: {e}", "danger")

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        try:
            post_usuario(
                request.form.get('form-nome'),
                request.form.get('form-email'),
                request.form.get('form-senha')
            )

            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            flash(str(e), 'danger')

    return render_template('cadastro.html')


@app.route('/cliente', methods=['GET', 'POST'])
def cliente():
    if request.method == 'POST':
        try:
            post_clientes(
                nome=request.form.get('form-nome'),
                email=request.form.get('form-email'),
                senha=request.form.get('form-senha'),
                endereco=request.form.get('form-endereco')
            )

            flash('Cliente cadastrado com sucesso!', 'success')
            return redirect(url_for('cliente'))

        except Exception as e:
            flash(f'Erro ao cadastrar cliente: {e}', 'danger')

    try:
        clientes = get_clientes()
    except:
        clientes = []

    return render_template('clientes.html', clientes=clientes)


@app.route('/galpao', methods=['GET', 'POST'])
def galpao():
    if request.method == 'POST':
        try:
            post_galpao(
                nome=request.form.get('form-nome'),
                localizacao=request.form.get('form-localizacao'),
                capacidade=request.form.get('form-capacidade')
            )

            flash('Galpão cadastrado com sucesso!', 'success')
            return redirect(url_for('galpao'))

        except Exception as e:
            flash(f'Erro ao cadastrar galpão: {e}', 'danger')

    try:
        galpoes = get_galpoes()
    except:
        galpoes = []

    return render_template('galpao.html', repositorios=galpoes)


@app.route('/encomendas', methods=['GET', 'POST'])
def encomendas():

    if request.method == 'POST':

        nome = request.form.get('form-nome')
        fragilidade = request.form.get('form-fragilidade')
        tipo = request.form.get('form-tipo')
        remetente = request.form.get('form-remetente')

        try:
            post_encomendas(
                nome=nome,
                fragilidade=fragilidade,
                tipo=tipo,
                remetente=remetente
            )

            flash('Encomenda cadastrada com sucesso!', 'success')

        except Exception as e:
            print(e)
            flash('Erro ao cadastrar encomenda.', 'danger')

        return redirect(url_for('encomendas'))

    try:
        encomendas_lista = get_encomendas()

        busca = request.args.get('busca', '').strip()

        if busca:

            encomendas_lista = [
                e for e in encomendas_lista
                if busca.lower() in str(
                    e.get('codigo_rastreio', '')
                ).lower()
            ]

    except Exception as e:
        print(e)
        encomendas_lista = []

    return render_template(
        'encomendas.html',
        encomendas=encomendas_lista
    )

@app.route('/rastreio', methods=['GET', 'POST'])
def rastreio():
    if request.method == 'POST':
        try:
            post_movimentacao(
                situacao=request.form.get('form-situacao'),
                codigo_rastreio=request.form.get('form-codigo-rastreio'),
                galpao_id=int(request.form.get('form-galpao-id'))
            )

            flash('Movimentação salva com sucesso!', 'success')
            return redirect(url_for('rastreio'))

        except Exception as e:
            flash(f'Erro ao salvar movimentação: {e}', 'danger')

    try:
        movimentacoes = get_movimentacao()
    except:
        movimentacoes = []

    try:
        encomendas = get_encomendas()
    except:
        encomendas = []

    try:
        entregadores = get_entregadores()
    except:
        entregadores = []

    return render_template(
        'rastreio.html',
        movimentacoes=movimentacoes,
        encomendas=encomendas,
        entregadores=entregadores
    )

@app.route('/dashboard')
@login_required
def dashboard():

    try:
        movimentacoes = get_movimentacao()
    except:
        movimentacoes = []

    try:
        encomendas = get_encomendas()
    except:
        encomendas = []

    try:
        galpoes = get_galpoes()
    except:
        galpoes = []

    try:
        entregadores = get_entregadores()
    except:
        entregadores = []

    return render_template(
        'rastreio.html',
        movimentacoes=movimentacoes,
        encomendas=encomendas,
        galpoes=galpoes,
        entregadores=entregadores
    )
if __name__ == '__main__':
    app.run(debug=True, port=5004)
