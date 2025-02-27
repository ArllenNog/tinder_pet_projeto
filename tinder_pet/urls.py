from django.urls import path
from . import views

urlpatterns = [
    path('', views.explorar, name='explorar'),
    path('anuncio', views.anuncio, name='anuncio'),
    path('anunciar', views.anunciar, name='anunciar'),
    path('meuperfil', views.meuperfil, name='meuperfil'),
    path('entrar', views.sign_in, name='sign_in'),
    path('sair', views.sign_out, name='sign_out'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver')
    #path('novo-pet', views.novopet, name='novo-pet')
]