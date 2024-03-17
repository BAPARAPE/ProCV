     
from django.db import models
from django.conf import settings
from django.contrib.auth.models import  AbstractUser

class User(AbstractUser):
    pass

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class InfoPerso(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nomcv = models.CharField(max_length=100)
    prenomcv = models.CharField(max_length=100)
    emailcv = models.EmailField(max_length=100)
    numero = models.CharField(max_length=30)
    adresse = models.CharField(max_length=80)
    profil = models.CharField(max_length=200)
    competence = models.CharField(max_length=150)
    interet = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nomcv} {self.prenomcv}"

class Experience(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poste = models.CharField(max_length=100,null=True)
    societe = models.CharField(max_length=50,null=True) 
    adresse_exp = models.CharField(max_length=80,null=True)
    date_debut = models.DateField(null=True)
    date_fin = models.DateField(null=True, blank=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f"{self.poste} chez {self.societe}"

class Formation(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    diplome = models.CharField(max_length=100,null=True)
    etablissement = models.CharField(max_length=100,null=True)
    adresse_formation = models.CharField(max_length=80,null=True)
    date_debut_formation = models.DateField(null=True)
    date_fin_formation = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.diplome} à {self.etablissement}"

class Langue(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    anglais = models.CharField(max_length=50)
    francais = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.anglais}: {self.francais}"
     