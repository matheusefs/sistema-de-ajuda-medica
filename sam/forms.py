# Cria os formulários do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, FloatField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from sam.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
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
    valor = FloatField("Valor a ser convertido", validators=[DataRequired()])
    unidade_origem = SelectField("De", choices=[("g", "Gramas"), ("mg", "Miligramas"), ("mcg", "Microgramas")])
    unidade_destino = SelectField("Para", choices=[("g", "Gramas"), ("mg", "Miligramas"), ("mcg", "Microgramas")])
    data_adm = DateField("Data de administração", format="%Y-%m-%d", validators=[DataRequired()])
    id_medicamento = SelectField("Medicamento", coerce=int, validators=[DataRequired()])
    lote = StringField("Lote do medicamento", validators=[DataRequired(), Length(max=50)])
    forma_adm = SelectField("Forma de administração", choices=[("oral", "Oral"), ("sublingual", "Sublingual"),("retal", "Retal"),("intravenosa", "Intravenosa"),("intramuscular", "Intramuscular"),("subcutanea", "Subcutânea")])
    id_paciente = SelectField("Paciente", coerce=int, validators=[DataRequired()])
    botao_confirmacao = SubmitField("Converter e salvar")

