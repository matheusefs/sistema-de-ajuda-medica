from flask import render_template, url_for, redirect, flash
from sqlalchemy.exc import IntegrityError
from sam import app, database, bcrypt
from sam.models import Usuario, Medicamento, Historico, Paciente
from flask_login import login_required, login_user, logout_user, current_user
from sam.forms import FormLogin, FormCadastro, FormConversao, FormPaciente, FormMedicamento
from sam.utils import converter_unidades, para_mg

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("calculadora", id_usuario=usuario.id))
        else:
            flash("Email ou senha inválidos. Por favor, tente novamente.", "danger")
    return render_template("login.html", form=form_login)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form_cadastro = FormCadastro()
    
    if form_cadastro.validate_on_submit():
        if form_cadastro.senha.data != form_cadastro.confirmacao_senha.data:
            flash("As senhas não coincidem.", "error")
        else:
            try:
                senha_hashed = bcrypt.generate_password_hash(form_cadastro.senha.data)
                usuario = Usuario(
                    nome=form_cadastro.nome.data,
                    email=form_cadastro.email.data,
                    senha=senha_hashed
                )
                database.session.add(usuario)
                database.session.commit()
                login_user(usuario, remember=True)
                return redirect(url_for("calculadora", id=usuario.id))
            except IntegrityError:
                database.session.rollback()
                flash("Este email já está cadastrado.", "error")
    else:
        # Exibe mensagens de erro do próprio WTForms
        for field, errors in form_cadastro.errors.items():
            for error in errors:
                flash(f"{error}", "error")

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

        try:
            # Tenta converter as unidades
            convertido = converter_unidades(valor, origem, destino)

            if convertido is not None:
                # Converte para mg apenas se forem unidades de peso
                if origem in ["g", "mg", "mcg"] and destino in ["g", "mg", "mcg"]:
                    dose_mg = para_mg(convertido, destino)
                    limite_seguro_mg = 4000
                    if dose_mg > limite_seguro_mg:
                        flash(f"Atenção: A dose convertida é alta, avalie a conversão com cuidado", "error")

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

        except ValueError as e:
            # Mostra aviso se a conversão for inválida (ex: peso ↔ volume)
            flash(str(e), "error")
            resultado = None

    return render_template("calculadora.html", form=form_calculadora, resultado=resultado, historicos = historicos)

@app.route("/pacientes/novo", methods=["GET", "POST"])
@login_required
def novo_paciente():
    form = FormPaciente()
    if form.validate_on_submit():

        paciente = Paciente(
            nome=form.nome.data,
            cpf=form.cpf.data,
            data_nascimento=form.data_nascimento.data,
            observacoes=form.observacoes.data
        )
        
        database.session.add(paciente)

        try:
            database.session.commit()
            flash("Paciente cadastrado com sucesso!", "success")
            return redirect(url_for("novo_paciente"))
        except IntegrityError:
            database.session.rollback()
            flash("Erro: CPF já cadastrado!", "error")
        
        flash(f"Paciente {paciente.nome} cadastrado com sucesso!", "success")
        return redirect(url_for("novo_paciente"))
    
    return render_template("novo_paciente.html", form=form)

@app.route("/novomedicamento", methods=["GET", "POST"])
def adicionar_medicamento():
    form = FormMedicamento()

    if form.validate_on_submit():
        nome = form.nome.data
        observacoes = form.observacoes.data

        # Verificar se o medicamento já existe
        existente = Medicamento.query.filter_by(nome=nome).first()
        if existente:
            flash("Este medicamento já está cadastrado!", "error")
        else:
            novo_medicamento = Medicamento(nome=nome, observacoes=observacoes)
            database.session.add(novo_medicamento)
            database.session.commit()
            flash(f"Medicamento '{nome}' adicionado com sucesso!", "success")
            return redirect(url_for("adicionar_medicamento"))

    return render_template("adicionar_medicamento.html", form=form)

@app.route("/logout")
def logout():
    logout_user
    return redirect(url_for("homepage"))



