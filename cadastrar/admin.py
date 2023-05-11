from django.contrib import admin

from .models import (AjudaManager, Assessor, Categorias, RegistroDisparo,
                     Titular, Viatura)

admin.site.register(Categorias)
admin.site.register(Titular)
admin.site.register(Viatura)
admin.site.register(Assessor)
admin.site.register(RegistroDisparo)
admin.site.register(AjudaManager)
