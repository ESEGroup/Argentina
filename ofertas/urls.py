from django.conf.urls import url
from . import views

app_name = 'ofertas'

urlpatterns = [
    # /ofertas/
    url(r'^$', views.index, name='index'),

    # /ofertas/71/ (oferta ID)
    url(r'^(?P<oferta_id>[0-9]+)/?$', views.detail, name='detail'),

    # /ofertas/71/favorite/ (oferta ID)
    url(r'^(?P<oferta_id>[0-9]+)/favorite/?$', views.favorite, name='favorite'),
]