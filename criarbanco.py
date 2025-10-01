from sam import database, app
from sam.models import Usuario, Paciente, Medicamento, Historico

with app.app_context():
    database.create_all()