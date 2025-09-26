from sam import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader #gerenciamneto de login
def load_usuario(id_usuario):
    return Usuario.queryy.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Intenger, primary_key = True) #diz que é a chave primaria
    nome = database.Column(database.String, nullable = False) # diz que o tipo número inteiro e que é um campo obrigatório
    email = database.Column(database.String, nullable = False, unique = True) # diz que o tipo é string, que é um campo obrigatório e que em todo o banco de dados a informação deve ser única(não deve haver repetidos)
    senha = database.Column(database.String, nullable = False)  # diz que o tipo é string e que é um campo obrigatório

class Paciente(database.Model):
    id = database.Column(database.Intenger, primary_key = True)
    nome = database.Column(database.String, nullable = False)

class Medicamento(database.Model):
    id = database.Column(database.Intenger, primary_key = True)
    nome = database.Column(database.String, nullable = False)
    lote = database.Column(database.Intenger, nullable = False)
    forma_adm = database.Column(database.String, nullable = False) 

class Calculadora(database.Model):
    id = id = database.Column(database.Intenger, primary_key = True)
    qtd_prescrita = database.Column(database.Intenger, nullable = False)
    un_prescrita = database.Column(database.String, nullable = False)
    qtd_requerida = database.Column(database.Intenger)
    un_requerida = database.Column(database.String, nullable = False)