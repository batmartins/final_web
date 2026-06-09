from flask import Flask, render_template, url_for, flash, request, redirect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.testing.pickleable import User

from models import db_session, Usuario
from sqlalchemy import select, and_, func
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
app = Flask(__name__)
#mover para .env
app.config['SECRET_KEY'] = 'sua_senha'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@login_manager.user_loader
def load_user(user_id):
    user = select(Usuario).where(Usuario.id == int(user_id))
    return db_session.execute(user).scalar_one_or_none()

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     return render_template('rastreio.html')
    if request.method == 'POST':
        email = request.form.get('form-email')
        senha = request.form.get('form-senha')
        '''   if not
        if not email or not senha:
            flash('Por favor, preencha todos os campos', 'danger')
            return render_template('login.html')
        '''
        if email and senha:
            verificar_email = select(Usuario).where(Usuario.email == email)
            resultado_email = db_session.execute(verificar_email).scalar_one_or_none()
            if resultado_email:
                if resultado_email.check_password(senha):
                    #login correto
                    login_user(resultado_email)
                    flash('Login concluído', 'success')
                    return redirect(url_for('rastreio'))
                else:
                    # senha incorreta
                    flash('Senha incorreta', 'danger')
                    return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form.get('form-nome')
        email = request.form.get('form-email')
        senha = request.form.get('form-senha')
        if not nome or not email or not senha:
            flash('Por favor, preencha todos os campos', 'danger')
            return render_template('cadastro.html')
        verifica_email = select(Usuario).where(Usuario.email == email)
        existe_email = db_session.execute(verifica_email).scalar_one_or_none()
        if existe_email:
            flash(f'Email {email} ja cadastrado', 'danger')
            return render_template('cadastro.html')

        try:
            novo_usuario = Usuario(nome=nome, email=email, senha=senha)
            novo_usuario.set_password(senha)
            db_session.add(novo_usuario)
            db_session.commit()
            flash(f'Usuario {nome} cadastrado', 'success')
            return redirect(url_for('login'))
        except SQLAlchemyError as e:
            flash(f'Erro na base de dados ao cadastrar usuario', 'danger')
            print(f'Erro na base de dados: {e}')
            return redirect(url_for('cadastro_usuario'))
        except Exception as e:
            flash(f'erro ao cadastrar usuario', 'danger')
            print(f'Erro ao cadastrar: {e}')
            return redirect(url_for('cadastro_usuario'))
    return render_template('rastreio.html')


@app.route('/rastreio')
def rastreio():
    return render_template('rastreio.html')

@app.route('/busca_pacote')
def busca_pacote():
    return (render_template('busca_pacote.html'))
@app.route('/galpao')
def galpao():
    return render_template('galpao.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cliente')
def cliente():
    return render_template('clientes.html')


if __name__ == '__main__':
    app.run(debug=True, port=5004)