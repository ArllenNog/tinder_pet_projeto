import os
import uuid
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from .models import Anuncio
from .models import Anunciante
from .models import Pet
from .models import Raca
from .models import Cidade
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import secrets
import string
import datetime


def explorar(request):
    
    if not request.session.get('user_data'):
        return redirect('sign_in')
    else:
        tipo = 0
        user = request.session.get('user_data')

        if request.method == "POST":
            anunciante = Anunciante.objects.filter(email = user.get('email')).first()
            _firstTime = request.POST.get('firstTime')
            _querAdotar = request.POST.get('querAdotar')
            if(_firstTime):
                anunciante.firstTime = _firstTime
            if(_querAdotar):
                anunciante.querAdotar = _querAdotar
            anunciante.save()
        elif request.method == "GET":
            tipo = int(request.GET.get('tipo', 2))#garantir que seja um numero inteiro para nao haver problemas na chamada do template
        

        if tipo != 2:
            anuncios = Anuncio.objects.select_related('pet').values('id','status','pet__fotoDestaque','tipo', 'pet__nome', 'pet__raca__racas', 'pet__sexo').filter(pet__tipo=tipo)
        else:
            anuncios = Anuncio.objects.select_related('pet').values('id','status','pet__fotoDestaque','tipo', 'pet__nome', 'pet__raca__racas', 'pet__sexo')
            
        context = {
            'tipoFiltro' : tipo,
            'anuncios': anuncios,
            'first_time' : Anunciante.objects.filter(email = user.get('email')).first().firstTime
        }

        #verificar se ja completou cadastro
        if Anunciante.objects.filter(email=user.get('email')).exists():
            return render(request, 'explorar.html', context)
        else:
            return redirect('cadastrar')

def anuncio(request):
    if not request.session.get('user_data'):
        return redirect('sign_in')
    else:
        user = request.session.get('user_data')
        anunciante = Anunciante.objects.filter(email = user.get('email')).first()
        anuncio_id = request.GET.get('id') or request.POST.get('id') 
        anuncio_obj = Anuncio.objects.filter(id = anuncio_id).first()
        pet = Pet.objects.filter(id = anuncio_obj.pet_id).first() 

        #atualizacao?
        if request.method == "GET":
            if request.GET.get('atualizar'):
                return redirect( reverse('meuperfil') + '?opcao=1')
            
            #exclusao?
            if request.GET.get('excluir'):
                #deletar o pet deleta automaticamente o anuncio tambem
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
                pet.delete()
                return redirect( reverse('meuperfil') + '?opcao=1')
            
            #conclusao?
            if request.GET.get('concluido'):
                anuncio_obj.status = int(request.GET.get('concluido')) 
                anuncio_obj.save()
                return redirect( reverse('anuncio') + '?id=' + str(anuncio_id))
            
        elif request.method == "POST":
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
            pet.save()

            #atualizar dados do anuncio
            if(_texto):
                anuncio_obj.texto = _texto
            anuncio_obj.save()

            #atualizar dados do usuario
            if(_bairro):
                anunciante.bairro = _bairro
            if(_cidade):
                anunciante.cidade = Cidade.objects.filter(cidades = _cidade).first()
            anunciante.save()

            return redirect( reverse('anuncio') + '?id=' + str(anuncio_id))

        modoEdicao = False
        anuncioProprio = (pet.dono == Anunciante.objects.filter(email = user.get('email')).first())

        if( anuncioProprio ):#a pessoa logada é dona do anuncio
            modoEdicao = True

        anuncio = Anuncio.objects.select_related('pet').values('id','status','pet__nome', 'texto','pet__raca__racas','pet__peso', 'pet__idade','pet__sexo','pet__fotoDestaque','tipo', 'anunciante__telefone','anunciante__bairro', 'anunciante__cidade__cidades', 'pet__foto1', 'pet__foto2', 'pet__foto3', 'pet__foto4').filter(id=anuncio_obj.id)
        context = {
            'pet':pet, 'anuncio' : anuncio, 'edit_mode' : modoEdicao, 'cidades' : Cidade.objects.all().values(), 'anuncio_proprio' : anuncioProprio
        }
        return render(request, 'anuncio.html', context)

def anunciar(request):
    if not request.session.get('user_data'):
        return redirect('sign_in')
    else:
        if request.method == "POST":
            user = request.session.get('user_data')
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
            user = request.session.get('user_data')
            #_idDono = Anunciante.objects.get(email = user.get('email')).id
            _idDono = Anunciante.objects.filter(email=user.get('email')).first()
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
                           dono = _idDono , fotoDestaque = _arquivo_fotoDestaque, foto1 = _arquivo_foto_1,
                           foto2 = _arquivo_foto_2, foto3 = _arquivo_foto_3, foto4 = _arquivo_foto_4)
            novo_pet.save()

            novo_anuncio = Anuncio(texto = _desc, status = 0, dataPublicacao = datetime.datetime.now(),
                                   tipo = 0, anunciante_id = Anunciante.objects.filter(email = user.get("email")).first().id,
                                   pet_id = novo_pet.id )
            novo_anuncio.save()
            return redirect( reverse('anuncio') + '?id=' + str(novo_anuncio.id))

        user = request.session.get('user_data')
        _dono = Anunciante.objects.filter(email = user.get('email')).first()
        context = { 'pets' : Pet.objects.filter(dono = _dono).values(), 'racas' : Raca.objects.all().values() }
        return render(request, 'anunciar.html', context)
    
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
        if request.method == "POST":
            user = request.session.get('user_data')
            _nome = request.POST.get('nome')
            _senha = request.POST.get('senha')
            _bairro = request.POST.get('bairro')
            _cidade = request.POST.get('cidade')
            _telefone = request.POST.get('telefone')
            _whatsapp = request.POST.get('whatsapp')
            anunciante = Anunciante.objects.filter(email = user.get('email')).first()
            if(_nome):
                anunciante.nome = _nome
            if(_senha):
                anunciante.setar_senha(_senha)
            if(_bairro):
                anunciante.bairro = _bairro
            if(_cidade):
                anunciante.cidade =  Cidade.objects.filter(cidades = _cidade).first()
            if(_telefone):
                anunciante.telefone = _telefone
            if(_whatsapp):
                anunciante.whatsapp = _whatsapp
            anunciante.save()

        opcao = '0'
        if request.GET.get('opcao'):
            opcao = request.GET.get('opcao')

        user = request.session.get('user_data')
        user_data = Anunciante.objects.filter(email = user.get('email')).first()
        user_pets = Pet.objects.filter(dono_id = user_data.id)
        user_anuncios = Anuncio.objects.select_related('pet').values('id','status','pet__nome').filter(anunciante_id = user_data.id)
        context = {
            'user_data' : user_data, 'user_pets' : user_pets, 'user_anuncios': user_anuncios, 'opcao': opcao, 'cidades': Cidade.objects.all().values()
        }
        return render(request, 'meuperfil.html', context)
    
def cadastrar(request):
    if request.method == "POST":
        #processar requisicao
        _nome = ""
        _email = ""
        _senha = ""
        _loginGoogle = False

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

        _telefone = request.POST.get("telefone")
        _whatsapp = request.POST.get("whatsapp")
        _bairro = request.POST.get("bairro")
        _idCidade = int( request.POST.get("cidade") )

        anunciante = Anunciante(nome=_nome , email=_email, telefone=_telefone, whatsapp=_whatsapp, bairro=_bairro,
                                cidade= Cidade.objects.filter(id = _idCidade).first() , loginGoogle=_loginGoogle)

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
                return redirect('explorar')
            else:   
                return render(request, 'entrar.html', {'erro': 'Senha incorreta'})
        else:
            return render(request, 'entrar.html', {'erro': 'Usuário não existe'})


    if not request.session.get('user_data'):
        return render(request, 'entrar.html')
    else:
        usuario = request.session.get('user_data')
        #se usuario iniciou o processo de login, mas não completou o cadastro
        if not Anunciante.objects.filter(email=usuario.get('email')).exists():
            return redirect('cadastrar')
        else:
            return redirect('explorar')


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print('Inside')
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data
    email = user_data.get('email')
    usuarioExiste = Anunciante.objects.filter(email=email).first()
    if(usuarioExiste):
        return redirect('explorar')
    else:
        return redirect('cadastrar')


def sign_out(request):
    del request.session['user_data']
    return redirect('sign_in')

