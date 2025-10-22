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
    nome = database.Column(database.String(100), nullable=False)  # Nome do paciente
    data_nascimento = database.Column(database.Date, nullable=False)  # Data de nascimento
    cpf = database.Column(database.String(14), nullable=False, unique=True)  # CPF formatado
    observacoes = database.Column(database.Text, nullable=True)  # Observações médicas

    def __repr__(self):
        return f"<Paciente {self.nome} - CPF: {self.cpf}>"

class Medicamento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100), nullable=False, unique=True)  # Nome único do medicamento
    observacoes = database.Column(database.Text, nullable=True)  # Observações adicionais (opcional)

    def __repr__(self):
        return f"<Medicamento {self.nome}>"

class Historico(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    unidade_origem = database.Column(database.String, nullable=False)
    unidade_destino = database.Column(database.String, nullable=False)
    valor_origem = database.Column(database.Float, nullable=False)
    valor_convertido = database.Column(database.Float, nullable=False)
    data_adm = database.Column(database.DateTime, nullable=False)
    lote = database.Column(database.String, nullable=False)
    forma_adm = database.Column(database.String, nullable=False)
    
    usuario_id = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)
    paciente_id = database.Column(database.Integer, database.ForeignKey("paciente.id"), nullable=False)
    medicamento_id = database.Column(database.Integer, database.ForeignKey("medicamento.id"), nullable=False)

    usuario = database.relationship("Usuario", backref="historicos_usuario", lazy=True)
    paciente = database.relationship("Paciente", backref="historicos_paciente", lazy=True)
    medicamento = database.relationship("Medicamento", backref="historicos_medicamento", lazy=True)

