from django.conf.urls import url
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

app_name = 'ofertas'

urlpatterns = [

    url(r'^login/$', auth_views.login, {'template_name': 'ofertas/login.html'}, name='login'),

    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),


    # url(r'^login/$', views.logIn.as_view(), name='login'),

    # /ofertas/
    url(r'^$', views.index, name='index'),

    url(r'^criar/$', views.CriarOferta.as_view(), name='criarofertas'),

    url(r'^minhas/$', views.MinhasOfertas, name='minhasofertas'),

    url(r'^deletar/(?P<oferta_id>[0-9]+)$', views.DeletarOferta, name='deletar'),

    # /ofertas/71/ (oferta ID)
    url(r'^(?P<oferta_id>[0-9]+)/?$', views.visualizarOferta, name='detail'),

    # /ofertas/71/favorite/ (oferta ID)
    url(r'^(?P<oferta_id>[0-9]+)/favorite/?$', views.favorite, name='favorite'),

    url(r'^professores/$', views.Professores, name='professores'),

    url(r'^validar/(?P<oferta_id>[0-9]+)$', views.ValidarProfessor, name='validarProfessor'),

    url(r'^registroaluno/$', views.RegistroAluno.as_view(), name='registroaluno'),

    url(r'^registroprofessor/$', views.RegistroProfessor.as_view(), name='registroprofessor'),

    url(r'^admdepartamento/(?P<oferta_id>[0-9]+)$', views.AdmDepartamento, name='AdmDepartamento'),

    # url(r'^logout/$', views.logOut, name='logout'),

]