from django.db import models

from cadastrar.models import Titular


class RegTitular(models.Model):
    nome_cat = models.CharField(max_length=100, blank=True)
    nome_tit = models.CharField(max_length=100, blank=True)
    id_t = models.CharField(max_length=30, blank=True, default="")
    only_assec = models.BooleanField(default=False)
    ddd = models.CharField(max_length=2, null=True, blank=True)
    telfnumber = models.CharField(
        max_length=250, unique=True, null=True, blank=True)

    def __str__(self):
        return self.nome_tit


class RegAssessor(models.Model):
    nome_cat = models.CharField(max_length=100, blank=True)
    nome_ass = models.CharField(max_length=100, blank=True)
    id_a = models.CharField(max_length=50, blank=True, default="")
    nome_tit = models.CharField(max_length=100, blank=True)
    ddd = models.CharField(max_length=2, null=True, blank=True)
    telfnumber = models.CharField(
        max_length=300, unique=True, null=True, blank=True)

    def __str__(self):
        return self.nome_ass


class Imagem(models.Model):
    imagem = models.ImageField(upload_to='imagem_disparo/')
