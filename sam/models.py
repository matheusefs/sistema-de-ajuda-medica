from sam import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader #gerenciamneto de login
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key = True) # define id como chave primária
    nome = database.Column(database.String, nullable = False) # define como string e dado obrigatório
    email = database.Column(database.String, nullable = False, unique = True) # diz que o tipo é string, que é um campo obrigatório e que em todo o banco de dados a informação deve ser única(não deve haver repetidos)
    senha = database.Column(database.String, nullable = False)  # diz que o tipo é string e que é um campo obrigatório

class Paciente(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    cpf = database.Column(database.String(14), nullable=False, unique=True)
    historicos = database.relationship("Historico", backref="paciente_obj", lazy=True)


class Medicamento(database.Model):
    id = database.Column(database.Integer, primary_key = True)
    nome = database.Column(database.String, nullable = False)

class Historico(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    unidade_origem = database.Column(database.String, nullable = False)
    unidade_destino = database.Column(database.String, nullable = False)
    valor_origem = database.Column(database.Float, nullable = False)
    valor_convertido = database.Column(database.Float, nullable = False)
    data_adm = database.Column(database.DateTime, nullable = False)
    lote = database.Column(database.String, nullable = False)
    forma_adm = database.Column(database.String, nullable = False) 
    usuario_id = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable = False)
    paciente_id = database.Column(database.Integer, database.ForeignKey("paciente.id"), nullable = False)
    usuario = database.relationship("Usuario", backref="historicos_usuario")
    medicamento_id = database.Column(database.Integer, database.ForeignKey("medicamento.id"), nullable=False)
    medicamento = database.relationship("Medicamento", backref="historicos")