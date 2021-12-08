from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    __tablename__= 'usuario'
    id = db.Column(db.Integer, primary_key =True, autoincrement = True)
    nome = db.Column(db.String, nullable = False)
    telefone = db.Column(db.String, nullable = False)
    usuario = db.Column(db.String, nullable = False , unique=True)
    senha = db.Column(db.String, nullable = False)

    def __init__(self, nome, telefone, usuario, senha):
        self.nome = nome
        self.telefone = telefone
        self.usuario = usuario
        self.senha = generate_password_hash(senha)

    def verify_password(self, pwd):
        return check_password_hash(self.senha, pwd)



class Servicos(db.Model, UserMixin):
    __tablename__= 'servicos'
    id_servicos = db.Column(db.Integer, primary_key =True, autoincrement = True)
    nome = db.Column(db.String, nullable = False)
    preco = db.Column(db.String, nullable = False)

    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco



class Clientes(db.Model, UserMixin):
    __tablename__= 'clientes'
    id_cliente = db.Column(db.Integer, primary_key =True, autoincrement = True)
    nome = db.Column(db.String, nullable = False)
    cpf = db.Column(db.String, nullable = False)
    telefone = db.Column(db.String, nullable = False)

    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

        

class ServicosAgendados(db.Model, UserMixin):
    __tablename__= 'servicos_agendados'
    id_servico_agendado = db.Column(db.Integer, primary_key =True, autoincrement = True)
    fk_id_servico = db.Column(db.Integer, nullable = False)
    desc_servico = db.Column(db.String, nullable = False)
    fk_id_cliente = db.Column(db.Integer, nullable = False)
    nm_cliente = db.Column(db.String, nullable = False)
    horario_agendado = db.Column(db.String, nullable = False)
    data_agendamento = db.Column(db.String, nullable = False)
    status = db.Column(db.Integer, nullable = True)
    desc_status = db.Column(db.Integer, nullable = True)

    def __init__(self, fk_id_servico, desc_servico, fk_id_cliente, nm_cliente, horario_agendado, data_agendamento, status, desc_status):
        self.fk_id_servico = fk_id_servico
        self.desc_servico = desc_servico
        self.fk_id_cliente = fk_id_cliente
        self.nm_cliente = nm_cliente
        self.horario_agendado = horario_agendado
        self.data_agendamento = data_agendamento
        self.status = status
        self.desc_status = desc_status


class StatusAgendamento(db.Model, UserMixin):
    __tablename__= 'status_agendamento'
    id_status = db.Column(db.Integer, primary_key =True, autoincrement = True)
    desc_status = db.Column(db.String, nullable = False)


    def __init__(self, id_status, desc_status):
        self.id_status = id_status
        self.desc_status = desc_status

