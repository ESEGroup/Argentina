# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Usuario(User):
    nome = models.CharField(max_length=256)
    telefone = models.CharField(max_length=256)
    nascimento = models.CharField(max_length=256)
    e_aluno = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class ProfessorRecrutador(Usuario):
    departamento = models.CharField(max_length=256)
    admDepartamento = models.BooleanField(default=False)
    identificador = models.CharField(max_length=1024)
    esta_validado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome + ' - ' + self.departamento


class Aluno(Usuario):
    user_id = models.CharField(max_length=1024)
    estadoCivil = models.CharField(max_length=256)
    curso = models.CharField(max_length=256)
    periodo = models.CharField(max_length=2)
    CRA = models.CharField(max_length=7)
    objetivo = models.CharField(max_length=256)
    formacao = models.CharField(max_length=256)
    experiencia = models.CharField(max_length=1024)
    habilidade = models.CharField(max_length=1024)
    identificador = models.CharField(max_length=1024)

    def __str__(self):
        return self.nome + ' - ' + self.curso

class Oferta(models.Model):
    criador = models.CharField(max_length=250)
    titulo = models.CharField(max_length=500)
    descricao = models.CharField(max_length=100)
    imagem = models.CharField(max_length=10000)

    def __str__(self):
        return self.titulo + ' - ' + self.criador


class Candidato(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    curso = models.CharField(max_length=100)
    candidato_id = models.CharField(max_length=200)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.nome