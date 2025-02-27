from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Raca(models.Model):
    tipo = models.SmallIntegerField(default=0)#0 - cachorro , 1 - gato, 2 - outros
    racas = models.CharField(max_length=30)

class Cidade(models.Model):
    cidades = models.CharField(max_length=40)

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
    querAdotar = models.BooleanField(default=False)

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
    status = models.SmallIntegerField()#0-ativo, 1-doado
    dataPublicacao = models.DateField(null=True)
    

