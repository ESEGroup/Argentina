from .models import Oferta, Usuario
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import FormularioAluno, FormularioProfessor


def index(request):
    if request.user.is_authenticated():
        all_ofertas = Oferta.objects.all()
        return render(request, 'ofertas/index.html', {'all_ofertas': all_ofertas, 'username': request.user.username})
    return redirect('ofertas:login')


class RegistroAluno(View):
    form_class = FormularioAluno
    template_name = 'ofertas/formulario_registro.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

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

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('ofertas:index')

        return render(request, self.template_name, {'form': form})


def criarOferta(request):
    return render(request)


def visualizarOferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    return render(request, 'ofertas/visualizarOferta.html', {'oferta': oferta})


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
