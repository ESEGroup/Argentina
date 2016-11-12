from django.shortcuts import render, get_object_or_404
from .models import Oferta

def index(request):
    all_ofertas = Oferta.objects.all()
    return render(request, 'ofertas/index.html', {'all_ofertas': all_ofertas})


def detail(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    return render(request, 'ofertas/detail.html', {'oferta': oferta})

def favorite(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    try:
        selected_candidato = oferta.candidato_set.get(pk=request.POST['candidato'])
    except (KeyError, Candidato.DoesNotExist):
        return render(request, 'ofertas/detail.html', {
            'oferta': oferta,
            'error_message': 'Voce nao selecionou um candidato.'
        })
    else:
        selected_candidato.is_favorite = True
        selected_candidato.save()
        return render(request, 'ofertas/detail.html', {'oferta': oferta})