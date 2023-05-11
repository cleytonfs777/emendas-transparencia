from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    choices_cargo = (('A', 'Administrador'),
                     ('D', 'Disparador'))
    cargo = models.CharField(max_length=1, choices=choices_cargo)
    ddd = models.CharField(max_length=2, null=True, blank=True)
    telfnumber = models.CharField(max_length=20, null=True, blank=True)


class AprovUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=300)
    cargo = models.CharField(max_length=1, default="D")
    ddd = models.CharField(max_length=2, null=True, blank=True)
    telfnumber = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username
