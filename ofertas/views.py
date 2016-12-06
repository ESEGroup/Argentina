from .models import Oferta, Usuario, Aluno, ProfessorRecrutador, Candidato
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .forms import FormularioAluno, FormularioProfessor, FormularioCriarOferta


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

def MinhasOfertas(request):
    all_ofertas = Oferta.objects.filter(criador=request.user.username)
    return render(request, 'ofertas/index.html',
                      {'all_ofertas': all_ofertas,
                        'minha': True,
                       'usuario':ObterUsuario(request)})

def DeletarOferta(request, oferta_id):
    oferta = Oferta.objects.get(id=oferta_id)
    if(oferta.criador == request.user.username or request.user.is_superuser):
        oferta.delete()
    return redirect('ofertas:index')

class RegistroAluno(View):
    form_class = FormularioAluno
    template_name = 'ofertas/formulario_registro.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

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
    template_name = 'ofertas/formulario_registro.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

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

class CriarOferta(View):
    form_class = FormularioCriarOferta
    template_name = 'ofertas/formulario_criar_oferta.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'usuario':ObterUsuario(request)})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            bolsa = Oferta()

            bolsa.criador = request.user.id
            bolsa.titulo = form.cleaned_data['titulo']
            bolsa.descricao = form.cleaned_data['descricao']
            bolsa.imagem = form.cleaned_data['imagem']

            bolsa.save()

            return redirect('ofertas:detail',
                            oferta_id=bolsa.pk,)

        return render(request, self.template_name, {'form': form, 'usuario':ObterUsuario(request)})


def visualizarOferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    e_candidato = False
    usuario = ObterUsuario(request)
    if (usuario.e_aluno):
        candidatos = Oferta.objects.get(id=oferta_id).candidato_set.all()
        for candidato in candidatos:
            if ((candidato.candidato_id == usuario.id) or (candidato.candidato_id == request.user.id)):
                e_candidato = True
    return render(request, 'ofertas/visualizarOferta.html',
                  {'oferta': oferta,
                   'criador': ProfessorRecrutador.objects.get(id=oferta.criador),
                   'usuario' : ObterUsuario(request),
                   'e_candidato': e_candidato})


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
            if (not(counter % 2) and (counter > 1)):
                professores += [professoresDoubled[counter]]
            counter += 1

    return render(request, 'ofertas/professores.html',
                  {'professores': professores,
                   'usuario': ObterUsuario(request)})

def ValidarProfessor(request, oferta_id):
    professorObj1 = ProfessorRecrutador.objects.get(id=oferta_id)
    id2 = int(oferta_id) + 1
    professorObj2 = ProfessorRecrutador.objects.get(id=id2)
    if(professorObj1.esta_validado or professorObj2.esta_validado):
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

def ObterUsuario(request):
    try:
        return Aluno.objects.get(identificador=request.user.username)
    except(ObjectDoesNotExist):
        try:
            return ProfessorRecrutador.objects.get(identificador=request.user.username)
        except(ObjectDoesNotExist):
            return request.user