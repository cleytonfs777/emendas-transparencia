from django.contrib import admin

from .models import Imagem, RegAssessor, RegTitular


class RegTitularAdmin(admin.ModelAdmin):
    list_display = ('nome_cat', 'nome_tit', 'only_assec', 'id_t')


class RegAssessorAdmin(admin.ModelAdmin):
    list_display = ('nome_ass', 'nome_cat', 'nome_tit', 'id_a')


admin.site.register(RegTitular, RegTitularAdmin)

admin.site.register(RegAssessor, RegAssessorAdmin)

admin.site.register(Imagem)
