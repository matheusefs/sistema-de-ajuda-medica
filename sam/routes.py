from flask import render_template, url_for, redirect
from sam import app, database, bcrypt
from sam.models import Usuario, Medicamento, Historico, Paciente
from flask_login import login_required, login_user, logout_user, current_user
from sam.forms import FormLogin, FormCadastro, FormConversao
from werkzeug.utils import secure_filename
from sam.utils import converter_unidades
import os

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("calculadora", id_usuario=usuario.id))
    return render_template("login.html", form=form_login)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form_cadastro = FormCadastro()
    if form_cadastro.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_cadastro.senha.data)
        usuario = Usuario(nome = form_cadastro.nome.data, senha = senha, email = form_cadastro.email.data )
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("calculadora", id=usuario.id))
    return render_template("cadastro.html", form=form_cadastro)

@app.route("/calculadora", methods=["GET", "POST"])
def calculadora():
    form_calculadora = FormConversao()
    
    pacientes = Paciente.query.all()
    form_calculadora.id_paciente.choices = [(p.id, f"{p.nome} - CPF: {p.cpf}") for p in pacientes]
    
    medicamentos = Medicamento.query.all()
    form_calculadora.id_medicamento.choices = [(m.id, m.nome) for m in medicamentos]
    
    resultado = None
    historicos = Historico.query.filter_by(usuario_id=current_user.id).order_by(Historico.data_adm.desc()).all()
    
    if form_calculadora.validate_on_submit():
        valor = form_calculadora.valor.data
        origem = form_calculadora.unidade_origem.data
        destino = form_calculadora.unidade_destino.data
        data_adm = form_calculadora.data_adm.data
        lote = form_calculadora.lote.data
        forma_adm = form_calculadora.forma_adm.data
        paciente_id = form_calculadora.id_paciente.data
        medicamento_id = form_calculadora.id_medicamento.data

        convertido = converter_unidades(valor, origem, destino)

        if convertido is not None:
            novo_historico = Historico(
                unidade_origem = origem,
                unidade_destino = destino,
                valor_origem = valor,
                valor_convertido = convertido,
                usuario_id = current_user.id,
                paciente_id = paciente_id,
                data_adm = data_adm,
                medicamento_id = medicamento_id,
                lote = lote,
                forma_adm = forma_adm
            )
            
            database.session.add(novo_historico)
            database.session.commit()

            resultado = convertido
            historicos = Historico.query.filter_by(usuario_id=current_user.id).order_by(Historico.data_adm.desc()).all()

    return render_template("calculadora.html", form=form_calculadora, resultado=resultado, historicos = historicos)
