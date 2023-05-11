import os

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode

from cadastrar.decorators import has_permission_decorator
from utils.crypto import encrypt_number
from utils.email import send_styled_email

from .models import AprovUser, Users

User = get_user_model()


@has_permission_decorator('listar_disparador')
def listar_disparador(request):
    if request.method == "GET":
        # Obtenha o número da página atual para cada tabela
        page_disparador = request.GET.get('page_disparador', '1')

        # Limite de exibições de arquivos por página
        limite_titular = '10'

        disparadores_all = Users.objects.filter(
            cargo="D").order_by('first_name')

        # Crie os paginadores para cada tabela
        paginator_disparador = Paginator(disparadores_all, limite_titular)

        # Obtenha os objetos paginados para a página atual
        disparadores = paginator_disparador.get_page(page_disparador)

        return render(request, 'listar_disparador.html', {'disparadores': disparadores})


@has_permission_decorator('cadastrar_disparador')
def cadastrar_disparador(request):
    if request.method == "GET":
        return render(request, 'cadastrar_disparador.html')
    if request.method == "POST":
        usuario = request.POST.get('usuario', '')
        nome = request.POST.get('nome', '')
        sobrenome = request.POST.get('sobrenome', '')
        email = request.POST.get('email', '')
        senha = request.POST.get('senha', '')
        senha2 = request.POST.get('senha2', '')
        telregdisp = request.POST.get('telregdisp', '')
        dddregdisp = request.POST.get('dddregdisp', '')

    if senha != senha2:
        messages.add_message(request, messages.ERROR,
                             "Senhas não conferem")
        return redirect(reverse('cadastrar_disparador'))

    if Users.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.ERROR,
                             "Usuario já existe")
        return redirect(reverse('cadastrar_disparador'))

    if Users.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR,
                             "Email já existe")
        return redirect(reverse('cadastrar_disparador'))

    if usuario == '' or email == '' or senha == '':
        if usuario == '':
            messages.add_message(request, messages.ERROR,
                                 "Usuário não pode estar vazio")
        elif email == '':
            messages.add_message(request, messages.ERROR,
                                 "Email não pode estar vazio")
        elif senha == '':
            messages.add_message(request, messages.ERROR,
                                 "Senha não pode estar vazio")
        return redirect(reverse('cadastrar_disparador'))

    if usuario == '' or email == '' or senha == '' or nome == '' or sobrenome == '' or telregdisp == '' or dddregdisp == '':

        if usuario == '':
            messages.add_message(request, messages.ERROR,
                                 "Usuário não pode estar vazio")
        elif email == '':
            messages.add_message(request, messages.ERROR,
                                 "Email não pode estar vazio")
        elif senha == '':
            messages.add_message(request, messages.ERROR,
                                 "Senha não pode estar vazio")
        elif nome == '':
            messages.add_message(request, messages.ERROR,
                                 "Nome não pode estar vazio")
        elif sobrenome == '':
            messages.add_message(request, messages.ERROR,
                                 "Sobrenome não pode estar vazio")
        elif telregdisp == '' or len(telregdisp) < 8:
            messages.add_message(request, messages.ERROR,
                                 "Telefone não pode estar vazio e nem ser menor que 8 digitos")
        elif dddregdisp == '' or len(dddregdisp) < 2:
            messages.add_message(request, messages.ERROR,
                                 "DDD não pode estar vazio e nem ser menor que 2 digitos")
        return redirect(reverse('cadastrar_disparador_ext'))

    user = Users.objects.create_user(
        first_name=nome, last_name=sobrenome, username=usuario, email=email, password=senha, cargo="D", telfnumber=telregdisp, ddd=dddregdisp)

    messages.add_message(request, messages.SUCCESS,
                         "Disparador criado com sucesso!!")
    return redirect(reverse('cadastrar_disparador'))


def authenticate_username_or_email(username, password):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

    if user.check_password(password):
        return user


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return render(request, 'login.html')
    elif request.method == "POST":
        username_or_email = request.POST.get('usuario')
        senha = request.POST.get('senha')

    user = authenticate_username_or_email(username_or_email, senha)

    if not user:
        messages.add_message(request, messages.ERROR,
                             "O usuário e/ou a senha estão incorretos")
        return redirect(reverse('login'))

    auth.login(request, user)
    return redirect(reverse('home'))


def logout(request):
    request.session.flush()
    return redirect(reverse('login'))


@has_permission_decorator('cadastrar_disparador')
def exluir_disparador(request, id):
    disparador = get_object_or_404(Users, id=id)
    disparador.delete()
    messages.add_message(request, messages.SUCCESS,
                         "Disparador excluido com sucesso!")
    return redirect(reverse('listar_disparador'))


@has_permission_decorator('cadastrar_disparador')
def editar_disparador(request, id):

    disparador = get_object_or_404(Users, id=id)

    if request.method == 'POST':

        if (request.POST.get('dispNome')) != (disparador.first_name):
            disparador.first_name = request.POST.get('dispNome')

        if (request.POST.get('dispSobrenome')) != (disparador.last_name):
            disparador.last_name = request.POST.get('dispSobrenome')

        if (request.POST.get('dispUsuario')) != (disparador.username):
            disparador.username = request.POST.get('dispUsuario')

        if (request.POST.get('dispEmail')) != (disparador.email):
            disparador.email = request.POST.get('dispEmail')
        try:
            disparador.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Edição realizada com sucesso!!")
        except:
            messages.add_message(request, messages.ERROR,
                                 "Falha durante a edição")

    return redirect(reverse('listar_disparador'))


def cadastrar_disparador_ext(request):

    if request.method == "POST":

        usuario = request.POST.get('usuario', '')
        nome = request.POST.get('nome', '')
        sobrenome = request.POST.get('sobrenome', '')
        email = request.POST.get('email', '')
        senha = request.POST.get('senha', '')
        senha2 = request.POST.get('senha2', '')
        teldisp = request.POST.get('teldisp', '')
        ddddisp = request.POST.get('ddddisp', '')

        if senha != senha2:
            messages.add_message(request, messages.ERROR,
                                 "Senhas não conferem")
            return redirect(reverse('cadastrar_disparador_ext'))

        if Users.objects.filter(username=usuario).exists():
            messages.add_message(request, messages.ERROR,
                                 "Usuario já existe")
            return redirect(reverse('cadastrar_disparador_ext'))

        if Users.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 "Email já existe")
            return redirect(reverse('cadastrar_disparador_ext'))

        if usuario == '' or email == '' or senha == '' or nome == '' or sobrenome == '' or teldisp == '' or ddddisp == '':
            if usuario == '':
                messages.add_message(request, messages.ERROR,
                                     "Usuário não pode estar vazio")
            elif email == '':
                messages.add_message(request, messages.ERROR,
                                     "Email não pode estar vazio")
            elif senha == '':
                messages.add_message(request, messages.ERROR,
                                     "Senha não pode estar vazio")
            elif nome == '':
                messages.add_message(request, messages.ERROR,
                                     "Nome não pode estar vazio")
            elif sobrenome == '':
                messages.add_message(request, messages.ERROR,
                                     "Sobrenome não pode estar vazio")
            elif teldisp == '' or len(teldisp) < 8:
                messages.add_message(request, messages.ERROR,
                                     "Telefone não pode estar vazio e nem ser menor que 8 digitos")
            elif ddddisp == '' or len(ddddisp) < 2:
                messages.add_message(request, messages.ERROR,
                                     "DDD não pode estar vazio e nem ser menor que 2 digitos")
            return redirect(reverse('cadastrar_disparador_ext'))
        senha = encrypt_number(senha)
        print(f"Senha Criptografada: {senha}")

        user = AprovUser(first_name=nome, last_name=sobrenome, username=usuario,
                         email=email, password=senha, cargo="D", telfnumber=teldisp, ddd=ddddisp)

        user.save()

        # Encaminha email para o usuario informando que o cadastro será analisado pela equipe de aprovação da Dai
        subject = 'Dai Cadastros | Disparadores'
        to = email
        text_content = 'Esta é a versão em texto simples do e-mail.'
        titulo = 'Seu cadastro em análise!! 👁'
        msg = f"Olá senhor {nome} {sobrenome}, seu cadastro foi encaminhado para a equipe de aprovação da Dai, em breve você receberá um email com a confirmação da aprovação ou não do seu cadastro."
        send_styled_email(subject, to, text_content,  titulo, msg)

        messages.add_message(request, messages.SUCCESS,
                             "Seu cadastro foi encaminhado com sucesso!! Em breve você receberá a confirmação por email")

        return render(request, 'login.html')

    return render(request, 'cadastrar_disparador_ext.html')


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = Users.objects.filter(email=email).first()

        if user:
            subject = "Redefinição de senha"
            to_email = email
            context = {
                "email": to_email,
                "domain": request.META["HTTP_HOST"],
                "site_name": "Seu Site",
                "uid": force_str(urlsafe_base64_encode(force_bytes(user.pk))),
                "user": user,
                "token": default_token_generator.make_token(user),
                "protocol": "https" if request.is_secure() else "http",
            }
            email_template_name = "password_reset_email.html"
            text_content = get_template(email_template_name).render(context)
            titulo = "Redefinição de senha"
            msg = "Clique no link abaixo para redefinir sua senha."
            send_styled_email(subject, to_email, text_content, titulo, msg)
            messages.success(
                request, "Um email foi enviado para você com instruções para redefinir sua senha.")
            return redirect("login")
        else:
            messages.error(
                request, "Não foi possível encontrar um usuário com este endereço de e-mail.")

    return render(request, "password_reset_form.html")


# # accounts/views.py
# class MyPasswordReset(auth.views.PasswordResetView):
#     '''
#     Requer
#     registration/password_reset_form.html
#     registration/password_reset_email.html
#     registration/password_reset_subject.txt  Opcional
#     '''
#     ...


# class MyPasswordResetDone(auth.views.PasswordResetDoneView):
#     '''
#     Requer
#     registration/password_reset_done.html
#     '''
#     ...


def password_reset_confirm(request, uidb64=None, token=None):
    friendly_password_requirements = [
        "A senha deve ter pelo menos 8 caracteres.",
        "A senha não deve ser muito semelhante a seus outros atributos pessoais.",
        "A senha não deve ser uma senha comum.",
        "A senha não deve consistir apenas em números."
    ]

    # ...
    context = {
        'uidb64': uidb64,
        'token': token,
        'regras': friendly_password_requirements,
    }
    return render(request, 'password_reset_confirm.html', context)
