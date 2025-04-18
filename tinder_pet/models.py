from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Raca(models.Model):
    tipo = models.SmallIntegerField(default=0)#0 - cachorro , 1 - gato, 2 - outros
    racas = models.CharField(max_length=30)

class Cidade(models.Model):
    cidades = models.CharField(max_length=40)

class Doacao(models.Model):
    adotante = models.ForeignKey("Anunciante", on_delete=models.CASCADE)
    anuncio = models.ForeignKey("Anuncio", on_delete=models.CASCADE)
    dataDoacao = models.DateField(null=True)
    status = models.SmallIntegerField()#0 ativo - estao em contato, 1 bem sucedida, 2 - fracassou


class Anunciante(models.Model):
    nome = models.CharField(max_length=120, null=True)
    senha = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, unique=True)
    telefone = models.CharField(max_length=15, null=True)
    whatsapp = models.CharField(max_length=15, null=True)
    bairro = models.CharField(max_length=50, null=True)
    cidade = models.ForeignKey("Cidade", on_delete=models.PROTECT, null=True)
    loginGoogle = models.BooleanField(default=False)
    firstTime = models.BooleanField(default=True)
    emailConfirmado = models.BooleanField(default=False)
    token = models.CharField(max_length=30, null=True)
    #abaixo os dados para a pagina da ong
    isONG = models.BooleanField(default=False)
    nomeONG = models.CharField(max_length=120, null=True)
    cnpj = models.CharField(max_length=20, null=True)
    fotoPerfil = models.URLField(null=True)
    fotoCapa = models.URLField(null=True)
    sobre = models.TextField(null=True)
    chavePIX = models.CharField(max_length=50, null=True)
    endereço = models.CharField(max_length=255, null=True)
    instagram = models.URLField(null=True)
    facebook = models.URLField(null=True)
    twitter = models.URLField(null=True)
    site = models.URLField(null=True)

    def __str__(self):
        return self.nome

    def setar_senha(self, senha_raw):
        self.senha = make_password(senha_raw)

    def checkar_senha(self, senha_raw):
        return check_password(senha_raw, self.senha)

class Pet(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.SmallIntegerField(default=0)#0 - cachorro , 1 - gato, 2 - outros
    sexo = models.SmallIntegerField(null=True)#0 - macho, 1 - femea
    raca = models.ForeignKey("Raca", on_delete=models.PROTECT)
    peso = models.SmallIntegerField()
    idade = models.SmallIntegerField()
    castrado = models.BooleanField(default=False)
    dono = models.ForeignKey("Anunciante", on_delete=models.CASCADE)
    fotoDestaque = models.URLField(null=True)
    foto1 = models.URLField(null=True)
    foto2 = models.URLField(null=True)
    foto3 = models.URLField(null=True)
    foto4 = models.URLField(null=True)

class Anuncio(models.Model):
    #titulo = models.TextField(max_length=150, null=True)
    texto = models.TextField()
    tipo = models.SmallIntegerField(null=True)#0-doacao, 1-cruzamento
    anunciante = models.ForeignKey("Anunciante", on_delete=models.CASCADE)
    pet = models.ForeignKey("Pet", on_delete=models.CASCADE)
    status = models.SmallIntegerField()#0-ativo, 1-desativado, 2-concluido
    dataPublicacao = models.DateField(null=True)

class Comentario(models.Model):
    texto = models.TextField()
    anuncio = models.ForeignKey("Anuncio", on_delete=models.CASCADE)
    usuario = models.ForeignKey("Anunciante", on_delete=models.CASCADE)
    dataComentario = models.DateField()

class Favorito(models.Model):
    #favorita o anuncio e nao o pet
    anuncio = models.ForeignKey("Anuncio", on_delete=models.CASCADE)
    usuario = models.ForeignKey("Anunciante", on_delete=models.CASCADE)
    
class Notificacao(models.Model):
    tipo = models.SmallIntegerField(null=True)#0-novo comentário, 1-novo interessado, 2-doacao confirmada
    usuario = models.ForeignKey("Anunciante", null=True, on_delete=models.CASCADE)# apessoa a quem o anuncio ira se destinar
    anuncio = models.ForeignKey("Anuncio", null=True, on_delete=models.CASCADE)
    doacao = models.ForeignKey("Doacao", null=True, on_delete=models.CASCADE)
    aberta = models.BooleanField(default=False)
    dataNotificacao = models.DateTimeField(null=True)

