from django.db import models

class Oferta(models.Model):
    criador = models.CharField(max_length=250)
    titulo = models.CharField(max_length=500)
    descricao = models.CharField(max_length=100)
    imagem = models.CharField(max_length=1000)

    def __str__(self):
        return self.titulo + ' - ' + self.criador

class Candidato(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100)
    nome = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    class Usuario(models.Model):
        nome = models.CharField(max_length=256)
        email = models.CharField(max_length=256)
        telefone = models.CharField(max_length=256)
        nascimento = models.CharField(max_length=256)

        def __str__(self):
            return self.nome

    class ProfessorRecrutador(Usuario):
        departamento = models.CharField(max_length=256)
        admDepartamento = models.BooleanField(default=false)

        def __str__(self):
            return self.nome + ' - ' + self.departamento
