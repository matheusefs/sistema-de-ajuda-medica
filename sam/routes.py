from flask import render_template, url_for, redirect
from sam import app, database, bcrypt
from sam.models import Usuario
from flask_login import login_required, login_user, logout_user, current_user
from sam.forms import FormLogin, FormCriarConta, FormFoto
from werkzeug.utils import secure_filename
import os

@app.route("/")
def homepage():
    form_login = FormLogin

@app.route("/")