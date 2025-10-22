# Cria os formulários do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, FloatField, SelectField, DateField, IntegerField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from sam.models import Usuario, Paciente

Email.default_message = "Por favor digite um e-mail válido"

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer login")

class FormCadastro(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email(message='Por favor digite um e-mail válido')])
    nome = StringField("Nome completo", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirme sua senha", validators=[DataRequired(), EqualTo("senha", message="As senhas não coincidem")])
    botao_confirmacao = SubmitField("Registrar-se")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            return ValidationError("E-mail já cadastrado, Faça login para continuar.")

class FormPaciente(FlaskForm):
    nome = StringField("Nome do Paciente", validators=[DataRequired(), Length(min=2, max=100)])
    data_nascimento = DateField("Data de Nascimento", format='%Y-%m-%d', validators=[DataRequired()], render_kw={"placeholder": "AAAA-MM-DD"})
    cpf = StringField( "CPF", validators=[DataRequired(), Regexp(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message="CPF deve estar no formato XXX.XXX.XXX-XX")],render_kw={"placeholder": "000.000.000-00"})
    observacoes = TextAreaField( "Observações Médicas", validators=[Length(max=500)], render_kw={"placeholder": "Anotações importantes sobre o paciente"})
    botao_confirmacao = SubmitField("Cadastrar Paciente")

    def validate_cpf(self, cpf):
        paciente = Paciente.query.filter_by(cpf=cpf.data).first()
        if paciente:
            return ValidationError("CPF já cadastrado.")
        
class FormMedicamento(FlaskForm):
    nome = StringField("Nome do Medicamento", validators=[DataRequired(), Length(max=100)])
    observacoes = TextAreaField("Observações", validators=[Length(max=500)])
    botao_confirmacao = SubmitField("Adicionar Medicamento")

class FormConversao(FlaskForm):
    valor = FloatField("Valor a ser convertido", validators=[DataRequired()])
    unidade_origem = SelectField("De", choices=[("g", "Gramas"), ("mg", "Miligramas"), ("mcg", "Microgramas"), ("l", "Litros"), ("ml", "Mililitros")])
    unidade_destino = SelectField("Para", choices=[("g", "Gramas"), ("mg", "Miligramas"), ("mcg", "Microgramas"), ("l", "Litros"), ("ml", "Mililitros")])
    data_adm = DateField("Data de administração", format="%Y-%m-%d", validators=[DataRequired()])
    id_medicamento = SelectField("Medicamento", coerce=int, validators=[DataRequired()])
    lote = StringField("Lote do medicamento", validators=[DataRequired(), Length(max=50)])
    forma_adm = SelectField("Forma de administração", choices=[("oral", "Oral"), ("sublingual", "Sublingual"),("retal", "Retal"),("intravenosa", "Intravenosa"),("intramuscular", "Intramuscular"),("subcutanea", "Subcutânea")])
    id_paciente = SelectField("Paciente", coerce=int, validators=[DataRequired()])
    botao_confirmacao = SubmitField("Converter e salvar")

