from sam import database, app
from sam.models import Paciente, Medicamento

with app.app_context():
    #Pacientes
    pacientes = [
        Paciente(nome="João Silva", cpf="123.456.789-00"),
        Paciente(nome="Maria Oliveira", cpf="987.654.321-00"),
        Paciente(nome="Carlos Souza", cpf="111.222.333-44"),
        Paciente(nome="Ana Pereira", cpf="555.666.777-88"),
        Paciente(nome="Rafael Lima", cpf="999.888.777-66"),
    ]
    database.session.add_all(pacientes)

    #Medicamentos
    medicamentos = [
        Medicamento(nome="Paracetamol"),
        Medicamento(nome="Ibuprofeno"),
        Medicamento(nome="Amoxicilina"),
        Medicamento(nome="Dipirona"),
        Medicamento(nome="Omeprazol"),
    ]
    database.session.add_all(medicamentos)

    database.session.commit()

    print("Dados inseridos com sucesso!")
