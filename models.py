from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, func
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session, Session
from werkzeug.security import generate_password_hash, check_password_hash

#base de dados

engine = create_engine(
    "sqlite:///flashlog.db",
    echo=True
)


db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()



class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    senha = Column(String(255), nullable=False)
    criado_em = Column(DateTime, nullable=False)

    def setar_senha_hash(self,senha):
        self.senha = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha, senha)

    def serialize(self):
        dados = {

            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "criado_em": self.criado_em,



        }
        return dados



class Encomenda(Base):
    __tablename__ = 'encomendas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    fragilidade = Column(String(255), nullable=False)
    tipo = Column(String(255), nullable=False)
    criado_em = Column(DateTime, nullable=False, server_default=func.now())

    def serialize(self):
        dados = {

            "id": self.id,
            "nome": self.nome,
            "fragilidade": self.fragilidade,
            "tipo": self.tipo,
            "criado_em": self.criado_em
        }

        return dados

class Entregador(Base):
    __tablename__ = 'entregadores'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    veiculo = Column(String(255), nullable=False)
    criado_em = Column(DateTime, nullable=False, server_default=func.now())


    def serialize(self):


        dados = {
            "id": self.id,
            "nome": self.nome,
            "veiculo": self.veiculo,
            "criado_em": self.criado_em

        }

        return dados

class CentroDeTranporcacao(Base):
    __tablename__ = 'centro_de_transporcacoes'
    id = Column(Integer, primary_key=True)
    localizacao = Column(String(255), nullable=False)
    nome = Column(String(255), nullable=False)
    criado_em = Column(DateTime, nullable=False, server_default=func.now())

    def serialize(self):
        dados = {

            "id": self.id,
            "localizacao": self.localizacao,
            "nome": self.nome,
            "criado_em": self.criado_em

        }

        return dados







class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nome = Column(String(250), nullable=False)
    endereco = Column(String(250), nullable=False)
    produto = Column(String(250), nullable=False)
    criado_em = Column(DateTime, nullable=False, server_default=func.now())


    def serialize(self):
        dados = {

            "id": self.id,
            "nome": self.nome,
            "endereco": self.endereco,
            "produto": self.produto,
            "criado_em": self.criado_em
        }

        return dados


Base.metadata.create_all(engine)  # Cria as tabelas
