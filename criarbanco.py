from sam import database, app
from sam.models import Usuario, Paciente, Medicamento, Calculadora

with app.app_context():
    database.create_all()