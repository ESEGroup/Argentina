from django.test import TestCase
from ofertas.models import ProfessorRecrutador

# Create your tests here.

class ProfessorRecrutadorTestCase(TestCase):
    def setUp(self):
        ProfessorRecrutador.objects.create(nome="Travassos",
                                           username="travassos",
                                           email="travassos@",
                                           password="trav",
                                           telefone = "999999999",
                                           nascimento = "456456",
                                           e_aluno = False,
                                           departamento = "Software",
                                           admDepartamento = False,
                                           identificador = "46545665",
                                           esta_validado = False)
        ProfessorRecrutador.objects.create(nome="Hilmer",
                                           username="hilmer",
                                           email="hilmer@",
                                           password="hilm",
                                           telefone="222222222",
                                           nascimento="456456",
                                           e_aluno=False,
                                           departamento="Engenharia",
                                           admDepartamento=False,
                                           identificador="46545665",
                                           esta_validado=False)

    def test_professores(self):
        travassos = ProfessorRecrutador.objects.get(nome="Travassos")
        hilmer = ProfessorRecrutador.objects.get(nome="Hilmer")
        self.assertEqual(travassos.__str__(), 'Travassos - Software')
        self.assertEqual(hilmer.__str__(), 'Hilmer - Engenharia')
