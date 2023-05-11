from django import template

from cadastrar.models import Categorias, Titular

register = template.Library()


@register.filter(name='verifica_titular')
def verifica_titular(value, arg1):
    nome_r = value.title()
    categoria_r = arg1.title()
    categ_id = Categorias.objects.filter(nome=categoria_r).first()
    if categ_id:
        nome_t = Titular.objects.filter(
            nome=nome_r, categoria_id=categ_id.id).first()
        nome_t = nome_t.id if nome_t else -1
    else:
        nome_t = -1

    return nome_t


@register.filter(name='adiciona_categoria')
def adiciona_categoria(value):
    categ_esc = Categorias.objects.get(id=value)
    categ_esc = categ_esc.nome if categ_esc else "Colaborador"
    return categ_esc


@register.filter(name='retorna_id')
def retorna_id(categoria, nome):
    categoria_id = Categorias.objects.filter(nome=categoria).first()
    tit_id = Titular.objects.filter(nome=nome, categoria=categoria_id).first()
    if (tit_id):
        return tit_id.id
    else:
        return ''


@register.filter(name='gera_categoria')
def gera_categoria(value):
    if isinstance(value, int):
        try:
            value = int(value)
            categ_esc = Categorias.objects.get(id=value)
            return categ_esc.nome
        except:
            return '---'
    else:
        return '---'
