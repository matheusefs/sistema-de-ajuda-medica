from flask import render_template, url_for, redirect
from sam import app, database, bcrypt
from sam.models import Usuario
from flask_login import login_required, login_user, logout_user, current_user
from sam.forms import FormLogin, FormCadastro
from werkzeug.utils import secure_filename
import os

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("login.html", form=form_login)

@app.route("/cadastro")
def cadastro():
    form_cadastro =  FormCadastro()

    

    
