import os
import random
import uuid
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from .models import Anuncio
from .models import Doacao
from .models import Anunciante
from .models import Pet
from .models import Raca
from .models import Cidade
from .models import Comentario
from .models import Favorito
from .models import Notificacao
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import secrets
import string
import datetime

def politica_privacidade(request):
    return render(request, 'privacy.html')

def explorar(request):
    if not request.session.get('user_data'):
        return redirect('sign_in')
    else:
        tipo = 2
        personalizado = 0
        sexo = 2
        idadeMax = 25
        pesoMax = 100
        cidade_id = -1
        raca_id = -1
        user = request.session.get('user_data')
        anunciante = Anunciante.objects.filter(email = user.get('email')).first()

        if anunciante:
            if request.method == "POST":
                _firstTime = request.POST.get('firstTime')

                if(_firstTime):
                    anunciante.firstTime = _firstTime
                anunciante.save()

            elif request.method == "GET":
                tipo = int(request.GET.get('tipo', 2))#garantir que seja um numero inteiro para nao haver problemas na chamada do template
                personalizado = int(request.GET.get('personalizado', 0))
                if int(request.GET.get('personalizado', 0)) == 1:
                    sexo = int(request.GET.get('sexo', 2))
                    cidade_id = int(request.GET.get('cidade', -1))
                    raca_id = int(request.GET.get('raca', -1))
                    idadeMax = int(request.GET.get('idade', 25))
                    pesoMax = int(request.GET.get('peso', 100))

            
            filtros = {
                "pet__idade__lte": idadeMax,   # Sempre incluído
                "pet__peso__lte": pesoMax,     # Sempre incluído
            }

            # Adiciona os filtros conforme os critérios
            if tipo != 2:
                filtros["pet__tipo"] = tipo

            if sexo != 2:
                filtros["pet__sexo"] = sexo

            if cidade_id > -1:
                filtros["anunciante__cidade__id"] = cidade_id
            
            if raca_id > -1:
                filtros["pet__raca__id"] = raca_id

            anuncios = Anuncio.objects.select_related('pet').values('id','status','pet__fotoDestaque','tipo', 'pet__nome', 'pet__raca__racas', 'pet__sexo').filter(**filtros)
                            
            context = {
                'ong': anunciante.isONG,
                'tipoFiltro' : tipo,
                'personalizado' : personalizado,
                'sexo': sexo,
                'idadeMax': idadeMax,
                'pesoMax' : pesoMax,
                'cidade_id' : cidade_id,
                'raca_id' : raca_id,
                'anuncios': anuncios,
                'cidades' : Cidade.objects.values(),
                'racas' : Raca.objects.values(),
                'first_time' : Anunciante.objects.filter(email = user.get('email')).first().firstTime
            }

            return render(request, 'explorar.html', context)
                
        else:#se nao existe um usuario ainda, é provavel que ainda não tenha completado o cadastro
            return redirect('cadastrar')

def anuncio(request):
    user = request.session.get('user_data')
    _usuario = ''
    if user:
        _usuario = Anunciante.objects.filter(email = user.get('email')).first()
    anuncio_id = request.GET.get('id') or request.POST.get('id')
    _anuncio = Anuncio.objects.filter(id = anuncio_id).first()

    if _anuncio:
        #pet = Pet.objects.filter(dono = anuncio.anunciante).first()
        pet = Pet.objects.filter(id = _anuncio.pet.id).first()
        
        #atualizacao?
        if request.method == "POST":
            #atualizando informacoes do pet
            _fotoDestaque = request.FILES.get('foto_destaque')
            _foto1 = request.FILES.get('foto_1')
            _foto2 = request.FILES.get('foto_2')
            _foto3 = request.FILES.get('foto_3')
            _foto4 = request.FILES.get('foto_4')
            _deleting_foto1 = request.POST.get('delete_foto_1')
            _deleting_foto2 = request.POST.get('delete_foto_2')
            _deleting_foto3 = request.POST.get('delete_foto_3')
            _deleting_foto4 = request.POST.get('delete_foto_4')
            _texto = request.POST.get('texto')
            _peso = request.POST.get('peso')
            _idade = request.POST.get('idade')
            _bairro = request.POST.get('bairro')
            _cidade = request.POST.get('cidade')
            _castrado = request.POST.get('castrado')

            #atualizar dados do pet
            if(_fotoDestaque):
                if pet.fotoDestaque :
                    excluirFoto(pet.fotoDestaque)
                pet.fotoDestaque = "uploads/" + str(salvarFoto(_fotoDestaque))

            if(_foto1):
                if pet.foto1:
                    excluirFoto(pet.foto1)
                pet.foto1 = "uploads/" + str(salvarFoto(_foto1))
            elif _deleting_foto1 == '1':
                if pet.foto1:
                    excluirFoto(pet.foto1)
                pet.foto1 = ''

            if(_foto2):
                if pet.foto2:
                    excluirFoto(pet.foto2)
                pet.foto2 = "uploads/" + str(salvarFoto(_foto2))
            elif _deleting_foto2 == '1':
                if pet.foto2:
                    excluirFoto(pet.foto2)
                pet.foto2 = ''

            if(_foto3):
                if pet.foto3:
                    excluirFoto(pet.foto3)
                pet.foto3 = "uploads/" + str(salvarFoto(_foto3))
            elif _deleting_foto3 == '1':
                if pet.foto3:
                    excluirFoto(pet.foto3)
                pet.foto3 = ''

            if(_foto4):
                if pet.foto4:
                    excluirFoto(pet.foto4)
                pet.foto4 = "uploads/" + str(salvarFoto(_foto4))
            elif _deleting_foto4 == '1':
                if pet.foto4:
                    excluirFoto(pet.foto4)
                pet.foto4 = ''

            if(_peso):
                pet.peso = int(_peso)
            if(_idade):
                pet.idade = int(_idade)
            if(_castrado):
                if _castrado == "Sim":
                    pet.castrado = True
                else:
                    pet.castrado = False

            pet.save()

            #atualizar dados do anuncio
            if(_texto):
                _anuncio.texto = _texto
            _anuncio.save()

            #atualizar dados do usuario
            if(_usuario == _anuncio.anunciante):
                if(_bairro):
                    _usuario.bairro = _bairro
                if(_cidade):
                    _usuario.cidade = Cidade.objects.filter(cidades = _cidade).first()
                _usuario.save()

            return redirect( reverse('anuncio') + '?id=' + str(anuncio_id))
        
        elif request.method == "GET":
            if request.GET.get('atualizar'):
                return redirect( reverse('meuperfil') + '?opcao=1')
            
            #exclusao?
            if request.GET.get('excluir') and _usuario == _anuncio.anunciante:
                if pet.fotoDestaque:
                    excluirFoto(pet.fotoDestaque)
                if pet.foto1:
                    excluirFoto(pet.foto1)
                if pet.foto2:
                    excluirFoto(pet.foto2)
                if pet.foto3:
                    excluirFoto(pet.foto3)
                if pet.foto4:
                    excluirFoto(pet.foto4)
                pet.delete()#deletar o pet deleta automaticamente o anuncio tambem
                return redirect( reverse('meuperfil') + '?opcao=1')
            
            #adocao?
            if request.GET.get('adotar') and _usuario:
                if not Doacao.objects.filter(adotante = _usuario, anuncio = _anuncio).exists():#verificar se ja existe uma notificacao nesse sentido
                    nova_adocao = Doacao(adotante = _usuario, anuncio = _anuncio, status = 0)
                    nova_adocao.save()

                    #criar notificacao para o dono do anuncio de que alguem esta interessado
                    n = Notificacao(tipo = 1, usuario = _anuncio.anunciante, doacao = nova_adocao, dataNotificacao = datetime.datetime.now())
                    n.save()

                return redirect( reverse('anuncio') + '?id=' + str(anuncio_id))
                    
            
            #desativacao?
            if request.GET.get('desativar') and _usuario == _anuncio.anunciante:
                _anuncio.status = int(request.GET.get('desativar')) 
                _anuncio.save()
                return redirect( reverse('anuncio') + '?id=' + str(anuncio_id))
            
            #conclusao?
            if request.GET.get('concluir') and _usuario == _anuncio.anunciante:
                _anuncio.status = 2
                _anuncio.save()
                doacoes = Doacao.objects.filter(anuncio = _anuncio)
                adotante = Anunciante.objects.filter(id = request.GET.get('id_adotante')).first()
                for d in doacoes:
                    if d.adotante == adotante:
                        d.status = 1
                        d.dataDoacao = datetime.datetime.now()
                    else:
                        d.status = 2 #doacao falhou para os nao escolhidos
                    d.save()
                #notifica o adotante da doação concluida
                n = Notificacao(tipo = 2, usuario = adotante, anuncio = _anuncio, dataNotificacao = datetime.datetime.now())
                n.save()
                return redirect( reverse('anuncio') + '?id=' + str(anuncio_id))
            
            #comentario?
            if request.GET.get('comentar'):
                novo_comentario = request.GET.get('comentario')
                data_comentario = datetime.datetime.now()
                
                c = Comentario(texto = novo_comentario, anuncio = _anuncio, usuario = _usuario, dataComentario = data_comentario )
                c.save()

                #cria uma notificacao para o dono do anuncio
                n = Notificacao(tipo = 0, usuario = _anuncio.anunciante, anuncio = _anuncio, dataNotificacao = datetime.datetime.now())
                n.save()
                
                return redirect( reverse('anuncio') + '?id=' + str(anuncio_id))
            
            #favoritando?
            if request.GET.get('favoritar'):
                favoritar = request.GET.get('favoritar')
                if favoritar == '1':
                    #verificar se usuario já favoritou
                    if not Favorito.objects.filter(anuncio = _anuncio, usuario = _usuario):
                        f = Favorito(anuncio = _anuncio, usuario = _usuario)
                        f.save()
                elif favoritar == '2':
                    Favorito.objects.filter(anuncio = _anuncio, usuario = _usuario).delete()

                return redirect( reverse('anuncio') + '?id=' + str(anuncio_id))
            
            #abrindo notificacao?
            if request.GET.get('notificacao_id'):
                notificacao_id = request.GET.get('notificacao_id')
                notificacao = Notificacao.objects.filter(id = notificacao_id).first()
                
                #so abre notificacoes do proprio usuario
                if notificacao.usuario == _usuario:
                    notificacao.aberta = True
                    notificacao.save()
            
            modoEdicao = False
            ong = False
            isAdotante = False
            interessados = ''
            doacaoEscolhida = ''

            if _usuario:
                modoEdicao = (_usuario == _anuncio.anunciante)#ativa modo de edicao se usuario for dono do anuncio
                ong = _usuario.isONG
                if Doacao.objects.filter(anuncio = _anuncio).first():
                    isAdotante = Doacao.objects.filter(adotante = _usuario).first()
                interessados = Doacao.objects.filter(anuncio = _anuncio)
            
            #verificar se ja foi doado
            if _anuncio.status == 2:
                doacaoEscolhida = Doacao.objects.filter(anuncio = _anuncio, status = 1).first()

            usuario_favoritou = False
            if(_usuario):
                usuario_favoritou = Favorito.objects.filter(anuncio = _anuncio, usuario = _usuario)
 
            context = {
                'ong': ong,
                'pet': pet,
                'usuario_min': user,
                'usuario_full': _usuario,
                'anuncio' : _anuncio,
                'comentarios': Comentario.objects.filter(anuncio = _anuncio),
                'quant_favoritos' :  Favorito.objects.filter(anuncio = _anuncio).count,
                'usuario_favoritou' : usuario_favoritou,
                'interessados' : interessados,
                'doacao_escolhida' : doacaoEscolhida,
                'edit_mode' : modoEdicao,
                'cidades' : Cidade.objects.all().values(),
                'naoLogado' : not _usuario,
                'isAdotante' : isAdotante
            }

            return render(request, 'anuncio.html', context)
    else:
        return HttpResponse(status = 403)
    
        
def apoiar(request):
    if not request.session.get('user_data'):
        return redirect('sign_in')
    else:
        user = request.session.get('user_data')
        usuario = Anunciante.objects.filter(email=user.get('email')).first()

        if usuario:
            context = {
                'ong': usuario.isONG,
                'ongs': Anunciante.objects.filter(isONG = True)
            }
            return render(request, 'apoiar.html', context)
        else:
            return redirect('cadastrar')

def ong(request):
    user = request.session.get('user_data')
    usuario = ''
    _anuncios = ''
    _anunciante = ''

    if user:#logado   
        usuario = Anunciante.objects.filter(email = user.get('email')).first()
        if request.method == "GET":
            _anunciante = Anunciante.objects.filter(id = request.GET.get('id')).first()
        else:
            _anunciante = Anunciante.objects.filter(id = request.POST.get('id')).first()
        _anuncios = Anuncio.objects.filter(anunciante = _anunciante)
        if _anunciante:
            if _anunciante.isONG:
                if request.method == 'POST':
                    _ong_nome = request.POST.get('ong-nome')
                    _ong_foto_perfil = request.FILES.get('ong-foto-perfil')
                    _ong_foto_capa = request.FILES.get('ong-foto-capa')
                    _ong_desc = request.POST.get('ong-desc')
                    _ong_pix = request.POST.get('ong-pix')
                    _ong_contato = request.POST.get('ong-contato')
                    _ong_cnpj = request.POST.get('ong-cnpj')
                    _ong_endereco = request.POST.get('ong-endereco')
                    _ong_instagram = request.POST.get('ong-instagram')
                    _ong_facebook = request.POST.get('ong-facebook')
                    _ong_twitter = request.POST.get('ong-twitter')
                    _ong_site = request.POST.get('ong-site')
                    
                    if _ong_foto_perfil:
                        _anunciante.fotoPerfil = "uploads/" + str(salvarFoto(_ong_foto_perfil))
                    if _ong_foto_capa:
                        _anunciante.fotoCapa = "uploads/" + str(salvarFoto(_ong_foto_capa))

                    if _ong_nome:
                        _anunciante.nomeONG = _ong_nome
                    if _ong_desc:
                        _anunciante.sobre = _ong_desc
                    if _ong_pix:
                        _anunciante.chavePIX = _ong_pix
                    if _ong_contato:
                        _anunciante.telefone = _ong_contato
                    if _ong_cnpj:
                        _anunciante.cnpj = _ong_cnpj
                    if _ong_endereco:
                        _anunciante.cnpj = _ong_endereco
                    if _ong_instagram:
                        _anunciante.instagram = _ong_instagram
                    if _ong_facebook: 
                        _anunciante.facebook = _ong_facebook
                    if _ong_twitter:
                        _anunciante.twitter = _ong_twitter
                    if _ong_site:
                        _anunciante.site = _ong_site

                    _anunciante.save()
                    return redirect( reverse('ong') + '?id=' + str(request.POST.get('id')))
                else:#GET
                    isONG = False
                    if(usuario):
                        isONG = usuario.isONG
                    context = {
                        'id': request.GET.get('id'),
                        'ong': isONG,
                        'pagina_propria': (usuario == _anunciante),
                        'dados': _anunciante,
                        'anuncios' : _anuncios
                    }
                    return render(request, 'ong.html', context)
                    #return redirect( reverse('ong') + '?id=' + str(ong_id))
            else:
                return HttpResponse(status = 404)#usuario não é uma ONG
        else:
            return HttpResponse(status = 404)#usuario não existe
        
    else:#nao logado
        _anunciante = Anunciante.objects.filter(id = request.GET.get('id')).first()
        _anuncios = Anuncio.objects.filter(anunciante = _anunciante)
        context = {
            'id': request.GET.get('id'),
            'ong': False,
            'pagina_propria': False,
            'dados': _anunciante,
            'anuncios' : _anuncios
        }
        return render(request, 'ong.html', context)
    

def anunciar(request):
    if not request.session.get('user_data'):
        return redirect('sign_in')
    else:
        user = request.session.get('user_data')
        usuario = Anunciante.objects.filter(email=user.get('email')).first()

        if usuario:
            if request.method == "POST":
                #_tipoAnuncio = request.POST.get("anuncio_tipo")
                #_titulo = request.POST.get("titulo")
                _desc = request.POST.get("desc")#anuncio
                _nome = request.POST.get("nome_pet")
                _tipo = int(request.POST.get("pet_tipo"))
                _sexo = int(request.POST.get("pet_sexo"))
                _idRacaCachorro = 0
                if request.POST.get("raca_pet_id_cachorro"):
                    _idRacaCachorro = int(request.POST.get("raca_pet_id_cachorro"))
                _idRacaGato = 0
                if request.POST.get("raca_pet_id_gato"):
                    _idRacaGato = int(request.POST.get("raca_pet_id_gato"))
                _idRaca = 0
                if(_tipo == 0):
                    _idRaca = _idRacaCachorro
                else:
                    _idRaca = _idRacaGato
                _peso = int( request.POST.get("peso_pet") )
                _idade = int( request.POST.get("idade_pet") )
                _fotoDestaque = request.FILES.get('foto_destaque')
                _foto1 = request.FILES.get('foto_1')
                _foto2 = request.FILES.get('foto_2')
                _foto3 = request.FILES.get('foto_3')
                _foto4 = request.FILES.get('foto_4')

                _arquivo_fotoDestaque = "uploads/" + str(salvarFoto(_fotoDestaque))
                _arquivo_foto_1 = ""
                if _foto1:
                    _arquivo_foto_1 = "uploads/" + str(salvarFoto(_foto1))
                _arquivo_foto_2 = ""
                if _foto2:
                    _arquivo_foto_2 = "uploads/" + str(salvarFoto(_foto2))
                _arquivo_foto_3 = ""
                if _foto3:
                    _arquivo_foto_3 = "uploads/" + str(salvarFoto(_foto3))
                _arquivo_foto_4 = ""
                if _foto4:
                    _arquivo_foto_4 = "uploads/" + str(salvarFoto(_foto4))
                    
                novo_pet = Pet(nome = _nome, tipo = _tipo, sexo = _sexo, raca = Raca.objects.filter(id = _idRaca).first(), peso = _peso, idade = _idade,
                            dono = usuario , fotoDestaque = _arquivo_fotoDestaque, foto1 = _arquivo_foto_1,
                            foto2 = _arquivo_foto_2, foto3 = _arquivo_foto_3, foto4 = _arquivo_foto_4)
                novo_pet.save()

                novo_anuncio = Anuncio(texto = _desc, status = 0, dataPublicacao = datetime.datetime.now(),
                                    tipo = 0, anunciante_id = Anunciante.objects.filter(email = user.get("email")).first().id,
                                    pet_id = novo_pet.id )
                novo_anuncio.save()
                return redirect( reverse('anuncio') + '?id=' + str(novo_anuncio.id))
            else:
                user = request.session.get('user_data')
                usuario = Anunciante.objects.filter(email = user.get('email')).first()
                context = {
                    'usuario' : usuario,
                    'ong': usuario.isONG,
                    'pets' : Pet.objects.filter(dono = usuario).values(),
                    'racas' : Raca.objects.all().values() 
                }

                return render(request, 'anunciar.html', context)
            
        else:#nao terminou o cadastro
            return redirect('cadastrar')

    
#def novopet(request):
#    if not request.session.get('user_data'):
#        return redirect('sign_in')
#    else:
#        if request.method == "POST":
#            _nome = request.POST.get("nome_pet")
#            _tipo = int(request.POST.get("pet_tipo"))
#            _sexo = int(request.POST.get("pet_sexo"))
#            _idRacaCachorro = 0
#            if request.POST.get("raca_pet_id_cachorro"):
#                _idRacaCachorro = int(request.POST.get("raca_pet_id_cachorro"))
#            _idRacaGato = 0
#            if request.POST.get("raca_pet_id_gato"):
#                _idRacaGato = int(request.POST.get("raca_pet_id_gato"))
#            _idRaca = 0
#            if(_tipo == 0):
#                _idRaca = _idRacaCachorro
#            else:
#                _idRaca = _idRacaGato
#            _peso = int( request.POST.get("peso_pet") )
#            _idade = int( request.POST.get("idade_pet") )
#            user = request.session.get('user_data')
#            #_idDono = Anunciante.objects.get(email = user.get('email')).id
#            _idDono = Anunciante.objects.filter(email=user.get('email')).first()
#            _fotoDestaque = request.FILES.get('foto_destaque')
#            _foto1 = request.FILES.get('foto_1')
#            _foto2 = request.FILES.get('foto_2')
#            _foto3 = request.FILES.get('foto_3')
#            _foto4 = request.FILES.get('foto_4')
#
#            _arquivo_fotoDestaque = "uploads/" + str(salvarFoto(_fotoDestaque))
#            _arquivo_foto_1 = ""
#            if _foto1:
#                _arquivo_foto_1 = "uploads/" + str(salvarFoto(_foto1))
#            _arquivo_foto_2 = ""
#            if _foto2:
#                _arquivo_foto_2 = "uploads/" + str(salvarFoto(_foto2))
#            _arquivo_foto_3 = ""
#            if _foto3:
#                _arquivo_foto_3 = "uploads/" + str(salvarFoto(_foto3))
#            _arquivo_foto_4 = ""
#            if _foto4:
#                _arquivo_foto_4 = "uploads/" + str(salvarFoto(_foto4))
#                
#            novo_pet = Pet(nome = _nome, tipo = _tipo, sexo = _sexo, raca = Raca.objects.filter(id = _idRaca).first(), peso = _peso, idade = _idade,
#                           dono = _idDono , fotoDestaque = _arquivo_fotoDestaque, foto1 = _arquivo_foto_1,
#                           foto2 = _arquivo_foto_2, foto3 = _arquivo_foto_3, foto4 = _arquivo_foto_4)
#            novo_pet.save()
#            return redirect('anunciar')
#
#        data = Raca.objects.all().values()
#        return render(request, 'novo-pet.html', {'racas' : data})

def salvarFoto(foto):
    # Caminho para o diretório 'static' dentro do app 'tinder_pet'
    pasta_static = os.path.join(settings.BASE_DIR, 'tinder_pet', 'static', 'uploads')  # Ajuste para a pasta do seu app
    
    # Cria a pasta se não existir
    os.makedirs(pasta_static, exist_ok=True)
    
    # Gera um nome único para o arquivo
    nome_arquivo = f"{uuid.uuid4().hex}{os.path.splitext(foto.name)[1]}"  # Ex: 'f3d74b9b6f8c4d5c.png'
    
    # Caminho completo para salvar o arquivo
    caminho_arquivo = os.path.join(pasta_static, nome_arquivo)
    
    # Salva o arquivo
    with open(caminho_arquivo, 'wb+') as f:
        for chunk in foto.chunks():
            f.write(chunk)
    
    return nome_arquivo

def excluirFoto(file_path):
    caminho_arquivo = os.path.join(settings.BASE_DIR, 'tinder_pet', 'static', file_path)
    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)

def meuperfil(request):
    if not request.session.get('user_data'):
        return redirect('sign_in')
    else:
        user = request.session.get('user_data')
        opcao = '0'
        _usuario = Anunciante.objects.filter(email = user.get('email')).first()
        _email_enviado = False

        if _usuario:
            if request.method == "POST":
                _nome = request.POST.get('nome')
                _senha = request.POST.get('senha')
                _bairro = request.POST.get('bairro')
                _cidade = request.POST.get('cidade')
                _telefone = request.POST.get('telefone')
                _whatsapp = request.POST.get('whatsapp')
                _confirmar_email = request.POST.get('confirmar_email')

                if(_nome):
                    _usuario.nome = _nome
                if(_senha):
                    _usuario.setar_senha(_senha)
                if(_bairro):
                    _usuario.bairro = _bairro
                if(_cidade):
                    _usuario.cidade =  Cidade.objects.filter(cidades = _cidade).first()
                if(_telefone):
                    _usuario.telefone = _telefone
                if(_whatsapp):
                    _usuario.whatsapp = _whatsapp
                if(_confirmar_email):
                    #gerar token de usuario e enviar email
                    _usuario.token = gerar_token()
                    _email_enviado = True
                _usuario.save()
            else:
                if request.GET.get('opcao'):
                    opcao = request.GET.get('opcao')

            user = request.session.get('user_data')
            user_pets = Pet.objects.filter(dono = _usuario)
            user_anuncios = Anuncio.objects.select_related('pet').values('id','status','pet__nome').filter(anunciante = _usuario)
            user_adocoes = Doacao.objects.filter(adotante = _usuario)
            user_favoritos = Favorito.objects.filter(usuario = _usuario)
            user_notificacoes = Notificacao.objects.filter(usuario = _usuario).order_by('-dataNotificacao')
            context = {
                'ong': _usuario.isONG,
                'user_data' : _usuario, 
                'user_pets' : user_pets, 
                'user_anuncios': user_anuncios,
                'user_adocoes' : user_adocoes,
                'user_favoritos' : user_favoritos,
                'user_notificacoes': user_notificacoes,
                'opcao': opcao,
                'email_enviado' : _email_enviado,
                'cidades': Cidade.objects.all().values()
            }
            return render(request, 'meuperfil.html', context)
        else:
            return redirect('cadastrar')
    
def cadastrar(request):
    if request.method == "POST":
        #processar requisicao
        _nome = ""
        _email = ""
        _senha = ""
        _loginGoogle = False
        _emailConfirmado = False

        if not request.session.get('user_data'):
            _nome = request.POST.get("nome")
            _email = request.POST.get("email")
            _senha = request.POST.get("senha")
        else:
            user_data = request.session.get('user_data')
            _nome = user_data.get("given_name")
            _email = user_data.get("email")
            _senha = gerar_senha()
            _loginGoogle = True
            _emailConfirmado = True
            

        _is_ong = False
        if request.POST.get("is_ong") == 'on':
            _is_ong = True
        _telefone = request.POST.get("telefone")
        _whatsapp = request.POST.get("whatsapp")
        _bairro = request.POST.get("bairro")
        _idCidade = int( request.POST.get("cidade") )

        anunciante = Anunciante(nome=_nome , email=_email, telefone=_telefone, whatsapp=_whatsapp, bairro=_bairro,
                                cidade= Cidade.objects.filter(id = _idCidade).first() , loginGoogle=_loginGoogle, emailConfirmado = _emailConfirmado, isONG = _is_ong)

        # Definindo a senha com hashing
        anunciante.setar_senha(_senha)

        if Anunciante.objects.filter(email=anunciante.email).exists():
            #nao pode fazer o cadastro usuario já existe
            return render(request, 'cadastrar.html', {'titulo':'Registre-se', 'erro':'Usuário já está cadastrado'})
        else:
            # Salvando o anunciante no banco de dados
            anunciante.save()  
            request.session['user_data'] = {'given_name' : _nome, 'email' : _email}
            return redirect('explorar')

    if request.session.get('user_data'):#o usuario ja tem um login
        usuario = request.session.get('user_data')
        #verificar se usuario nao completou cadastro
        if not Anunciante.objects.filter(email=usuario.get('email')).exists():
            data = {
                'nome' : usuario.get('given_name'),
                'email' : usuario.get('email'),
                'senha': gerar_senha(),
                'titulo' : 'Finalizar cadastro',
                'cidades': Cidade.objects.all().values(),
            }
            return render( request, 'cadastrar.html', data )
        else:#o usuario esta logado e acessou a pagina de cadastro
            return redirect('explorar')
    else:#o usuario nao tem cadastro
        data = {
            'titulo' : 'Registre-se',
            'cidades': Cidade.objects.all().values(),
        }
        return render(request, 'cadastrar.html', data)
        

def gerar_senha(tamanho=12):
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))

def gerar_token(tamanho=30):
    caracteres = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    token = ''.join(random.choices(caracteres, k=tamanho))
    return token

##GOOGLE SIGN IN
@csrf_exempt
def sign_in(request):
    if request.method == "POST":
        _email = request.POST.get("email")
        _senha = request.POST.get("password")

        #verificar se login existe
        if Anunciante.objects.filter(email=_email).exists():
            usuario = Anunciante.objects.get(email=_email)
            #ver se senha ta certa
            if Anunciante.checkar_senha(usuario, _senha):
                request.session['user_data'] = {'given_name' : usuario.nome, 'email' : usuario.email}
                #login por email
                return redirect('explorar')
            else:   
                return render(request, 'entrar.html', {'erro': 'Senha incorreta'})
        else:
            return render(request, 'entrar.html', {'erro': 'Usuário não existe'})
    else:
        if not request.session.get('user_data'):
            return render(request, 'entrar.html')
        else:
            usuario = request.session.get('user_data')
            #se usuario iniciou o processo de login, mas não completou o cadastro
            if not Anunciante.objects.filter(email=usuario.get('email')).exists():
                return redirect('cadastrar')
            else:
                #login pelo google
                return redirect('explorar')


@csrf_exempt
def auth_receiver(request):
    #print('Inside')
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID'] #requests.Request()
        )
    except ValueError:
        return HttpResponse(status=403)
    except Exception as e:
        return HttpResponse(f"Erro inesperado: {e}", status = 500)

    #(https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data
    email = user_data.get('email')

    if Anunciante.objects.filter(email=email).first():
        #salvar foto atual do google do usuario no banco de dados
        u = Anunciante.objects.filter(email = user_data.get('email')).first()
        #evitar salvar por cima da foto da ong definida manualmente
        if not u.isONG:
            u.fotoPerfil = user_data.get('picture')
            u.save()

        return redirect('explorar')
    else:
        return redirect('cadastrar')


def sign_out(request):
    del request.session['user_data']
    return redirect('sign_in')

