# Cria os formulários do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from sam.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = StringField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer login")

class FormCadastro(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    nome = StringField("Nome completo", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirme sua senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Registrar-se")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            return ValidationError("E-mail já cadastrado, Faça login para continuar.")

class FormConversao(FlaskForm):
    valor = FloatField("Valor", validators=[DataRequired()])
    unidade_origem = SelectField("De", choices=[("g", "Gramas"), ("mg", "Miligramas"), ("mcg", "Microgramas")])
    unidade_destino = SelectField("Para", choices=[("g", "Gramas"), ("mg", "Miligramas"), ("mcg", "Microgramas")])
    botao_confirmacao = SubmitField("Converter")

