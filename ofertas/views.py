# -*- coding: utf-8 -*-
from .models import Oferta, Usuario, Aluno, ProfessorRecrutador, Candidato
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template import Context
from django.db import IntegrityError
from django.forms import modelform_factory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OfertaSerializer
from .forms import FormularioAluno, FormularioProfessor, FormularioCriarOferta, FormularioMudancaAluno, \
    FormularioMudancaProfessor


def index(request):
    if request.user.is_authenticated():
        all_ofertas = Oferta.objects.all()
        if request.user.is_superuser:
            return render(request, 'ofertas/index.html',
                          {'all_ofertas': all_ofertas,
                           'user': request.user})
        return render(request, 'ofertas/index.html',
                      {'all_ofertas': all_ofertas,
                       'user': request.user,
                       'usuario': ObterUsuario(request)})
    return redirect('ofertas:login')

class CriarOferta(View):
    form_class = FormularioCriarOferta
    template_name = 'ofertas/formulario_criar_oferta.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'usuario': ObterUsuario(request)})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            bolsa = Oferta()

            bolsa.criador = request.user.id
            bolsa.titulo = form.cleaned_data['titulo']
            bolsa.descricao = form.cleaned_data['descricao']
            bolsa.imagem = form.cleaned_data['imagem']

            if bolsa.imagem == "":
                bolsa.imagem = 'https://upload.wikimedia.org/wikipedia/commons/7/7b/Minerva_UFRJ_Oficial.png'

            bolsa.save()

            return redirect('ofertas:detail',
                            oferta_id=bolsa.pk, )

        return render(request, self.template_name, {'form': form, 'usuario': ObterUsuario(request)})

def visualizarOferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    if request.user.is_authenticated and not request.user.is_superuser:
        e_candidato = False
        usuario = ObterUsuario(request)
        candidatos = Oferta.objects.get(id=oferta_id).candidato_set.all()
        if (usuario.e_aluno):
            # candidatos = Oferta.objects.get(id=oferta_id).candidato_set.all()
            for candidato in candidatos:
                candidato_holder = Usuario.objects.get(id=candidato.candidato_id)
                if (candidato_holder.username == usuario.username):
                    e_candidato = True
        return render(request, 'ofertas/visualizarOferta.html',
                      {'oferta': oferta,
                       'criador': ProfessorRecrutador.objects.get(id=oferta.criador),
                       'usuario': ObterUsuario(request),
                       'e_candidato': e_candidato})
    else:
        return render(request, 'ofertas/visualizarOferta.html',
                      {'oferta': oferta,
                       'criador': ProfessorRecrutador.objects.get(id=oferta.criador)})

def MinhasOfertas(request):
    all_ofertas = Oferta.objects.filter(criador=request.user.id)
    return render(request, 'ofertas/index.html',
                  {'all_ofertas': all_ofertas,
                   'minha': True,
                   'usuario': ObterUsuario(request)})


def DeletarOferta(request, oferta_id):
    oferta = Oferta.objects.get(id=oferta_id)
    usuario = ObterUsuario(request)
    if (oferta.criador == request.user.username or request.user.is_superuser or oferta.criador == usuario.username):
        oferta.delete()
    return redirect('ofertas:index')




class RegistroAluno(View):
    form_class = FormularioAluno
    form_class_mudanca = FormularioMudancaAluno
    template_name = 'ofertas/formulario_registro.html'

    def get(self, request):
        if request.user.is_authenticated:
            usuario = ObterUsuario(request)
            form = self.form_class_mudanca(initial={'nome': usuario.nome,
                                                    'CRA': usuario.CRA,
                                                    'username': request.user.username,
                                                    'email': request.user.email,
                                                    'curso': usuario.curso,
                                                    'estadoCivil': usuario.estadoCivil,
                                                    'experiencia': usuario.experiencia,
                                                    'formacao': usuario.formacao,
                                                    'habilidade': usuario.habilidade,
                                                    'nascimento': usuario.nascimento,
                                                    'objetivo': usuario.objetivo,
                                                    'periodo': usuario.periodo,
                                                    'telefone': usuario.telefone})

        else:
            form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid() or request.user.is_authenticated:

            if (request.user.is_authenticated):
                aluno = ObterUsuario(request)
                nome = form.cleaned_data['nome']
                email = form.cleaned_data['email']
                CRA = form.cleaned_data['CRA']
                curso = form.cleaned_data['curso']
                estadoCivil = form.cleaned_data['estadoCivil']
                experiencia = form.cleaned_data['experiencia']
                formacao = form.cleaned_data['formacao']
                habilidade = form.cleaned_data['habilidade']
                nascimento = form.cleaned_data['nascimento']
                objetivo = form.cleaned_data['objetivo']
                periodo = form.cleaned_data['periodo']
                telefone = form.cleaned_data['telefone']
                if (nome != ''):
                    aluno.nome = nome
                if (email != ''):
                    request.user.email = email
                    request.user.save()
                if (CRA != ''):
                    aluno.CRA = CRA
                if (curso != ''):
                    aluno.curso = curso
                if (estadoCivil != ''):
                    aluno.estadoCivil = estadoCivil
                if (experiencia != ''):
                    aluno.experiencia = experiencia
                if (formacao != ''):
                    aluno.formacao = formacao
                if (habilidade != ''):
                    aluno.habilidade = habilidade
                if (nascimento != ''):
                    aluno.nascimento = nascimento
                if (objetivo != ''):
                    aluno.objetivo = objetivo
                if (periodo != ''):
                    aluno.periodo = periodo
                if (telefone != ''):
                    aluno.telefone = telefone
                aluno.save()
                return redirect('ofertas:perfil')
            else:
                aluno = Aluno()

                user = form.save(commit=False)

                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                aluno.nome = form.cleaned_data['nome']
                aluno.CRA = form.cleaned_data['CRA']
                aluno.curso = form.cleaned_data['curso']
                aluno.estadoCivil = form.cleaned_data['estadoCivil']
                aluno.experiencia = form.cleaned_data['experiencia']
                aluno.formacao = form.cleaned_data['formacao']
                aluno.habilidade = form.cleaned_data['habilidade']
                aluno.nascimento = form.cleaned_data['nascimento']
                aluno.objetivo = form.cleaned_data['objetivo']
                aluno.periodo = form.cleaned_data['periodo']
                aluno.telefone = form.cleaned_data['telefone']
                aluno.identificador = username
                aluno.e_aluno = True

                user.set_password(password)

                user.save()

                aluno.username = user.id

                aluno.save()

                user = authenticate(username=username, password=password)

                if user is not None:

                    if user.is_active:
                        login(request, user)
                        return redirect('ofertas:index')

        return render(request, self.template_name, {'form': form})


class RegistroProfessor(View):
    form_class = FormularioProfessor
    form_class_mudanca = FormularioMudancaProfessor
    template_name = 'ofertas/formulario_registro.html'

    def get(self, request):
        if request.user.is_authenticated:
            usuario = ObterUsuario(request)
            form = self.form_class_mudanca(initial={'nome': usuario.nome,
                                                    'email': request.user.email,
                                                    'nascimento': usuario.nascimento,
                                                    'telefone': usuario.telefone,
                                                    'departamento': usuario.departamento})

        else:
            form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid() or request.user.is_authenticated:

            if (request.user.is_authenticated):
                professor = ObterUsuario(request)
                nome = form.cleaned_data['nome']
                email = form.cleaned_data['email']
                nascimento = form.cleaned_data['nascimento']
                telefone = form.cleaned_data['telefone']
                departamento = form.cleaned_data['departamento']
                professor.nome = nome
                request.user.email = email
                professor.nascimento = nascimento
                professor.telefone = telefone
                professor.departamento = departamento
                professor.save()
                request.user.save()
                return redirect('ofertas:perfil')

            professor = ProfessorRecrutador()

            user = form.save(commit=False)

            professor.nome = form.cleaned_data['nome']
            professor.nascimento = form.cleaned_data['nascimento']
            professor.departamento = form.cleaned_data['departamento']
            professor.admDepartamento = False
            professor.telefone = form.cleaned_data['telefone']
            professor.esta_validado = False
            professor.identificador = form.cleaned_data['username']
            professor.e_aluno = False

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)

            user.save()

            professor.username = user.id

            professor.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('ofertas:index')

        return render(request, self.template_name, {'form': form})


def AlterarPerfil(request):
    if (ObterUsuario(request).e_aluno):
        return redirect('ofertas:registroaluno')
    elif (not ObterUsuario(request).e_aluno):
        return redirect('ofertas:registroprofessor')


def favorite(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    try:
        selected_candidato = oferta.candidato_set.get(pk=request.POST['candidato'])
    except (KeyError, Candidato.DoesNotExist):
        return render(request, 'ofertas/visualizarOferta.html', {
            'oferta': oferta,
            'error_message': 'Voce nao selecionou um candidato.'
        })
    else:
        selected_candidato.is_favorite = True
        selected_candidato.save()
        return render(request, 'ofertas/visualizarOferta.html', {'oferta': oferta})


def Professores(request):
    professoresDoubled = ProfessorRecrutador.objects.filter(admDepartamento=False)
    professores = professoresDoubled
    if (request.user.is_superuser):
        professoresDoubled = ProfessorRecrutador.objects.all()
    if (professoresDoubled.count() > 0):
        professores = [professoresDoubled[0]]
        counter = 0
        for professor in professoresDoubled:
            if (not (counter % 2) and (counter > 1)):
                professores += [professoresDoubled[counter]]
            counter += 1

    return render(request, 'ofertas/professores.html',
                  {'professores': professores,
                   'usuario': ObterUsuario(request)})


def ValidarProfessor(request, oferta_id):
    professorObj1 = ProfessorRecrutador.objects.get(id=oferta_id)
    id2 = int(oferta_id) + 1
    professorObj2 = ProfessorRecrutador.objects.get(id=id2)
    if (professorObj1.esta_validado or professorObj2.esta_validado):
        professorObj1.esta_validado = False
        professorObj1.admDepartamento = False
    else:
        professorObj1.esta_validado = True
    professorObj2.esta_validado = professorObj1.esta_validado
    professorObj1.save()
    professorObj2.save()
    return redirect('ofertas:professores')


def ValidarAdmDepartamento(request, professor_id):
    professorObj1 = ProfessorRecrutador.objects.get(id=professor_id)
    id2 = int(professor_id) + 1
    professorObj2 = ProfessorRecrutador.objects.get(id=id2)
    if (professorObj1.admDepartamento or professorObj2.admDepartamento):
        professorObj1.admDepartamento = False
    else:
        professorObj1.admDepartamento = True
    professorObj2.admDepartamento = professorObj1.admDepartamento
    professorObj1.save()
    professorObj2.save()
    return redirect('ofertas:professores')


def Candidatar(request, oferta_id):
    candidatos = Oferta.objects.get(id=oferta_id).candidato_set.all()
    usuario = ObterUsuario(request)
    try:
        candidatos.get(candidato_id=usuario.id).delete()
    except(ObjectDoesNotExist):
        try:
            candidatos.get(candidato_id=request.user.id).delete()
        except(ObjectDoesNotExist):
            candidato = Candidato(oferta=Oferta.objects.get(id=oferta_id),
                                  candidato_id=usuario.id,
                                  nome=Usuario.objects.get(id=usuario.id).nome,
                                  curso=usuario.curso,
                                  is_favorite=False)
            candidato.save()
            EnviarEmail(request, usuario, ProfessorRecrutador.objects.get(id=Oferta.objects.get(id=oferta_id).criador),
                        oferta=Oferta.objects.get(id=oferta_id))

    return redirect('ofertas:detail',
                    oferta_id=oferta_id)


def Perfil(request):
    if (request.user.is_superuser):
        usuario = request.user
    else:
        usuario = ObterUsuario(request)
    return render(request,
                  'ofertas/perfil.html',
                  {'usuario': usuario})


def Anonimo(request):
    all_ofertas = Oferta.objects.all()
    return render(request, 'ofertas/index.html',
                  {'all_ofertas': all_ofertas,
                   'e_convidado': True})


def ObterUsuario(request):
    try:
        return Aluno.objects.get(identificador=request.user.username)
        # return get_object_or_404(Aluno, identificador=request.user.username)
    except(ObjectDoesNotExist):
        try:
            return ProfessorRecrutador.objects.get(identificador=request.user.username)
        except(ObjectDoesNotExist):
            try:
                return request.user
            except(ObjectDoesNotExist):
                return None


class OfertasLista(APIView):
    # Lista todas as Ofertas
    def get(self, request):
        ofertas = Oferta.objects.all()
        serializer = OfertaSerializer(ofertas, many=True)
        return Response(serializer.data)


def EnviarEmail(request, remetente, destinatario, oferta):
    msg = EmailMessage(
        'Bolsa: ' + oferta.titulo,
        remetente.nome + ' Candidatou-se a ' + oferta.titulo + '<br>' +
        'Dados: <br>' +
        'Nome: ' + remetente.nome + '<br>' +
        'Email: ' + request.user.email + '<br>' +
        'Telefone: ' + remetente.telefone + '<br>' +
        'Nascimento: ' + remetente.nascimento + '<br>' +
        'Estado Civil: ' + remetente.estadoCivil + '<br>' +
        'Curso: ' + remetente.curso + '<br>' +
        'Período: ' + remetente.periodo + '<br>' +
        'CRA: ' + remetente.CRA + '<br>' +
        'Objetivo: ' + remetente.objetivo + '<br>' +
        'Formação: ' + remetente.formacao + '<br>' +
        'Experiência: ' + remetente.experiencia + '<br>' +
        'Habilidade: ' + remetente.habilidade + '<br>',
        request.user.email,
        [destinatario.email]
    )

    msg.content_subtype = "html"
    msg.send()

def BuscarOferta(request):
    try:
        all_ofertas = Oferta.objects.filter(titulo=request.GET.get('q'))
    except(ObjectDoesNotExist):
        all_ofertas = Oferta.objects.all
    return render(request, 'ofertas/index.html',
                      {'all_ofertas': all_ofertas ,
                       'user': request.user})