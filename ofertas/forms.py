# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django import forms
from .models import Aluno, ProfessorRecrutador, Oferta


class FormularioAluno(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Aluno
        fields = ['username',
                  'password',
                  'email',
                  'nome',
                  'telefone',
                  'nascimento',
                  'estadoCivil',
                  'curso',
                  'periodo',
                  'CRA',
                  'objetivo',
                  'formacao',
                  'experiencia',
                  'habilidade']

class FormularioMudancaAluno(forms.ModelForm):

    class Meta:
        model = Aluno
        fields = ['email',
                  'nome',
                  'telefone',
                  'nascimento',
                  'estadoCivil',
                  'curso',
                  'periodo',
                  'CRA',
                  'objetivo',
                  'formacao',
                  'experiencia',
                  'habilidade']

class FormularioProfessor(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ProfessorRecrutador
        fields = ['username',
                  'password',
                  'nome',
                  'email',
                  'telefone',
                  'nascimento',
                  'departamento']

class FormularioMudancaProfessor(forms.ModelForm):

    class Meta:
        model = ProfessorRecrutador
        fields = ['nome',
                  'email',
                  'telefone',
                  'nascimento',
                  'departamento']


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']


class FormularioCriarOferta(forms.ModelForm):
    imagem = forms.CharField(required=False)

    class Meta:
        model = Oferta
        fields = ['titulo',
                  'descricao',
                  'imagem']
