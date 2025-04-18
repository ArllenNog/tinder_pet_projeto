from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.explorar, name='explorar'),
    path('anuncio', views.anuncio, name='anuncio'),
    path('anunciar', views.anunciar, name='anunciar'),
    path('apoiar', views.apoiar, name='apoiar'),
    path('ong', views.ong, name='ong'),
    path('meuperfil', views.meuperfil, name='meuperfil'),
    path('entrar', views.sign_in, name='sign_in'),
    path('sair', views.sign_out, name='sign_out'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('politica-de-privacidade', views.politica_privacidade, name='politica-privacidade')
    #path('novo-pet', views.novopet, name='novo-pet')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)