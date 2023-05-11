import asyncio
import json
import os
import sys
from ast import literal_eval
from datetime import datetime
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from dotenv import load_dotenv
from PIL import Image

from cadastrar.decorators import has_permission_decorator
from cadastrar.models import (Assessor, Categorias, RegistroDisparo, Titular,
                              Viatura)
from cadastrar.views import category_exists, userid_exists
from core import settings
from usuarios.models import AprovUser, Users
from utils.crypto import decrypt_number, encrypt_number
from utils.email import send_styled_email

from .models import Imagem, RegAssessor, RegTitular
from .telegram_utils import send_telegram_image, send_telegram_message

load_dotenv()  # take environment variables from .env.


async def send_telegram_content(tasks):
    for send_func, args in tasks:
        await send_func(*args)


def separar_itens(s):
    itens_separados = s.split(';')
    resultado = []

    for item in itens_separados:
        if item:
            resultado.append(item.split(','))

    return resultado


def who_is_assessor(id_tit):
    return Assessor.objects.filter(titular_id=id_tit)


def msg_simple_telegram(user_id_m, messages_send):

    chat_id = user_id_m  # Substitua pelo chat_id do usuário no Telegram, se necessário

    # Crie uma corrotina para executar as chamadas assíncronas
    async def send_messages():
        for message in messages_send:
            await send_telegram_message(chat_id, message)

    # Execute a corrotina
    asyncio.run(send_messages())


@login_required
def confirmar_disparo(request):

    status_ocorr = request.POST.get('status_ocorr', '')
    release = request.POST.get('release', '')
    deputoc2 = request.POST.get('deputoc2', '')
    imagens = request.FILES.getlist('imagens', '')
    if status_ocorr == '' or release == '' or deputoc2 == '[]' or deputoc2 == '' or imagens == '':
        if status_ocorr == '':
            messages.add_message(request, messages.ERROR,
                                 "Selecione o status da ocorrência")
        if release == '':
            messages.add_message(request, messages.ERROR,
                                 "O campo release não deve estar em branco")
        if deputoc2 == '[]' or deputoc2 == '':
            messages.add_message(request, messages.ERROR,
                                 "Deve ser selecionada pelo menos uma viatura")
        if imagens == '':
            messages.add_message(request, messages.ERROR,
                                 "Você deve selecionar pelo menos uma imagem")

        return redirect(reverse('enviar_disparo'))

    deputoc2 = json.loads(deputoc2)
    msg_g = []

    # cria a logo a ser inserida
    caminho = os.path.join(os.getcwd(), 'templates',
                           'static', 'disparo', 'img', 'logo.png')
    logo = Image.open(caminho)

    # variável que vai receber o nome das imagens

    for f in imagens:
        # Nome do arquivo
        name = f"{datetime.now()}.png"

        img_p = Image.open(f)
        img_p = img_p.convert('RGB')
        # img_p = img_p.resize((1080,1350))

        # coloca a imagem de logo na imagem
        logo_width, logo_height = logo.size
        img_width, img_height = img_p.size

        # calcula o novo tamanho da logo (10% da dimensão da imagem principal)
        new_logo_width = int(img_width * 0.2)
        new_logo_height = int(logo_height * (new_logo_width / logo_width))

        # redimensiona a logo
        resized_logo = logo.resize(
            (new_logo_width, new_logo_height), Image.ANTIALIAS)

        # calcula a posição da logo (canto inferior direito, com uma margem de 10 pixels)
        logo_position = (img_width - new_logo_width - 10,
                         img_height - new_logo_height - 10)

        # cola a logo redimensionada na imagem principal
        img_p.paste(resized_logo, logo_position, resized_logo)

        # draw = ImageDraw.Draw(img_p)
        # draw.text((20, 80), f"CBMMG {date.today()}", (255, 255, 255))
        output = BytesIO()
        img_p.save(output, format="PNG", quality=100)
        output.seek(0)
        img_final = InMemoryUploadedFile(
            output, 'ImageField', name, 'image/png', sys.getsizeof(output), None)

        img = Imagem(imagem=img_final)
        img.save()

    rec_image = Imagem.objects.all()
    rec_image_urls = [img.imagem.url for img in rec_image]

    for depdip in deputoc2:
        msg_t = []
        mensagem = {}
        viat = Viatura.objects.get(placa=depdip[0][0])
        titular = Titular.objects.get(nome=viat.titular)
        if (titular):
            # VERIFICA SE O TITULAR TEM ASSESSORES
            assessor_is = who_is_assessor(titular.id)
            print(f"assessor_is: {assessor_is}")
            # VERIFICA SE O TITULAR QUER RECEBER MENSAGENS
            print(f"Só o assessor recebe? {titular.only_assec}")

            andamento = "Está em andamento " if status_ocorr == "A" else "Houve "
            tempo = "há " if status_ocorr == "A" else "houve"

            vtr_emp = ""

            if len(depdip[0]) == 1:
                vtr_emp = f"da viatura {viat.tipo}, placa {viat.placa}, adquirida"
            else:
                for vt in range(0, len(depdip[0])):

                    viat = Viatura.objects.get(placa=depdip[0][vt])

                    if vt == len(depdip[0])-1:
                        vtr_emp += f" e da viatura {viat.tipo}, placa {viat.placa}, adquiridas "
                    elif vt == len(depdip[0])-2:
                        vtr_emp += f"da viatura {viat.tipo}, placa {viat.placa} "
                    else:
                        vtr_emp += f"da viatura {viat.tipo}, placa {viat.placa}, "

            # Se o assessor quiser receber será gerada mensagem para ele
            if not titular.only_assec:
                titCat = titular.categoria

                msgx = f"Senhor {titCat} {titular.nome}. {andamento} ocorrência de destaque atendida pelo CBMMG"
                msg = f"Caro Colaborador. {andamento} ocorrência de destaque atendida pelo CBMMG"
                msg2 = f"Nesta atuação {tempo} o empenho {vtr_emp} com recursos financeiros encaminhados pelo senhor, ocorrência essa em que o Corpo de Bombeiros Militar de Minas Gerais teve as seguintes atuações: "
                msg3 = release
                msg4 = "Mais uma vez o CBMMG agradece o indispensável empenho do senhor para que mais vidas e bens sejam salvos no estado de Minas Gerais"

                msg_t.append(msg)
                msg_t.append(msg2)
                msg_t.append(msg3)
                msg_t.append(msg4)

                mensagem = {
                    "usuar": titular.nome,
                    "msg_a": msg_t,
                    "placa": viat.placa,
                    "rec_image": rec_image_urls,
                    "ident_f": "T"
                }

                msg_g.append(mensagem)

                msg_t = []
                mensagem = {}

            if (assessor_is):
                for asses_l in assessor_is:
                    msgx = f"Senhor Assessor do {asses_l.titular.categoria} {asses_l.titular.nome}, {asses_l.nome_assessor}. {andamento} ocorrência de destaque atendida pelo CBMMG"
                    msg = f"Caro Assessor Colaborador. {andamento} ocorrência de destaque atendida pelo CBMMG"
                    msg2 = f"Nesta atuação {tempo} o empenho {vtr_emp} com recursos financeiros encaminhados pelo titular que o senhor assessora, ocorrência essa em que o Corpo de Bombeiros Militar de Minas Gerais teve as seguintes atuações: "
                    msg3 = release
                    msg4 = "Mais uma vez o CBMMG agradece o indispensável empenho do senhor para que mais vidas e bens sejam salvos no estado de Minas Gerais"

                    msg_t.append(msg)
                    msg_t.append(msg2)
                    msg_t.append(msg3)
                    msg_t.append(msg4)

                    mensagem = {
                        "usuar": asses_l.nome_assessor,
                        "tit_nome": titular.nome,
                        "tit_cargo": titular.categoria.nome,
                        "msg_a": msg_t,
                        "placa": viat.placa,
                        "rec_image": rec_image_urls,
                        "ident_f": "A"
                    }

                    msg_g.append(mensagem)

                    msg_t = []
                    mensagem = {}

    return render(request, 'confirmar.html', {'mensagem': msg_g})


@login_required
def enviar_disparo(request):

    if request.method == "GET":

        # apagar todas as imagens da pasta media
        media_folder = os.path.join(settings.MEDIA_ROOT, 'imagem_disparo')
        for file_name in os.listdir(media_folder):
            file_path = os.path.join(media_folder, file_name)
            os.remove(file_path)

        # apagar todos os objetos da classe Imagem no banco de dados
        Imagem.objects.all().delete()

        viaturas = Viatura.objects.all()
        selecionados = []
        return render(request, 'enviar_disparo.html', {'viaturas': viaturas})

    elif request.method == "POST":
        if 'mensagem' in request.POST:
            print(f"A mensagem é {request.POST.get('mensagem')}")
            TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
            try:
                # obter a string do input
                input_string = request.POST.get('mensagem')

                # analisar a string como uma lista de dicionários
                dados = literal_eval(input_string)

                def process_message(d, id_u_teleg, TOKEN):
                    tasks = []
                    # Enviar mensagem para o usuário do Telegram
                    print(f"Bot token: {TOKEN}")
                    for msg in d['msg_a']:
                        tasks.append(
                            (send_telegram_message, (id_u_teleg, msg)))

                    # Enviar imagens para o usuário do Telegram
                    for img in d['rec_image']:

                        img_p = os.path.join(
                            settings.BASE_DIR, settings.MEDIA_ROOT, 'imagem_disparo', img)
                        img_p = str(img_p)
                        img_t = str(settings.BASE_DIR)
                        image_p = img_t + img_p

                        tasks.append(
                            (send_telegram_image, (id_u_teleg, image_p)))

                    return tasks

                print(f"Todos os dados: {dados}")
                # Inicializar a lista de tarefas
                tasks = []

                # Controlar se o envio para o grupo já foi feito
                send_to_group_called = False

                for d in dados:
                    verif = True
                    if d['ident_f'] == 'T':
                        titular_targ = Titular.objects.get(nome=d['usuar'])
                        id_t_teleg = titular_targ.id_chat_d
                        verif = False if id_t_teleg == '' else True
                        if verif:
                            d['msg_a'][0] = d['msg_a'][0].replace(
                                "Caro Colaborador", f"Senhor {titular_targ.categoria} {titular_targ.nome}")
                            print("Usuário: ", d['usuar'])
                            print("Id User: ", id_t_teleg)
                            print("Mensagem: ", "\n".join(d['msg_a']))
                            # Registra a mensagem enviada na tabela RegistroDisparo
                            reg_disparo = RegistroDisparo(
                                disparador=request.user.username, titular=f"{titular_targ.categoria} {titular_targ.nome}", assessor=None, viatura=d['placa'])
                            reg_disparo.save()
                            tasks += process_message(d, id_t_teleg, TOKEN)
                            if not send_to_group_called:
                                tasks += process_message(
                                    d, os.getenv('TELEGRAM_GROUP_ID'), TOKEN)
                                send_to_group_called = True

                    elif d['ident_f'] == 'A':
                        assessor_targ = Assessor.objects.get(
                            nome_assessor=d['usuar'])
                        id_u_teleg = assessor_targ.id_chat_a
                        verif = False if id_u_teleg == '' else True
                        if verif:
                            d['msg_a'][0] = d['msg_a'][0].replace(
                                "Caro Assessor Colaborador", f"Senhor Assessor {assessor_targ.nome_assessor} do {assessor_targ.titular.categoria} {assessor_targ.titular.nome}")
                            print("Usuário: ", d['usuar'])
                            print("Id User: ", id_u_teleg)
                            print("Mensagem: ", "\n".join(d['msg_a']))
                            # Registra a mensagem enviada na tabela RegistroDisparo
                            reg_disparo = RegistroDisparo(
                                disparador=request.user.username, titular=f"{d['tit_cargo']} {d['tit_nome']}", assessor=assessor_targ.nome_assessor, viatura=d['placa'])
                            reg_disparo.save()
                            tasks += process_message(d, id_u_teleg, TOKEN)
                            if not send_to_group_called:
                                tasks += process_message(
                                    d, os.getenv('TELEGRAM_GROUP_ID'), TOKEN)
                                send_to_group_called = True

                asyncio.run(send_telegram_content(tasks))

                messages.add_message(
                    request, messages.SUCCESS, "Mensagem encaminhada com sucesso!!")
                return redirect(reverse('enviar_disparo'))
            except Exception as ex:
                print(ex)
                messages.add_message(
                    request, messages.ERROR, "Erro ao enviar mensagem")
                return redirect(reverse('enviar_disparo'))


@has_permission_decorator('cadastrar_recursos')
def add_authorization(request):

    # Obtenha o número da página atual para cada tabela
    page_titular_auth = request.GET.get('page_titular_auth', '1')
    page_assessor_auth = request.GET.get('page_assessor_auth', '1')
    page_disparador_auth = request.GET.get('page_disparador_auth', '1')

    # Limite de exibições de arquivos por página
    limite_titular_auth = '10'
    limite_assessor_auth = '10'
    limite_disparador_auth = '10'

    # Consulte todos os objetos
    titulares_all = RegTitular.objects.all().order_by('nome_tit')
    assessores_all = RegAssessor.objects.all().order_by('nome_ass')
    disparador_all = AprovUser.objects.all().order_by('first_name')
    titulares = Titular.objects.all()
    categorias = Categorias.objects.all().order_by('nome')

    # Desencriptar os dados telfnumber
    for assessores_a in assessores_all:
        if assessores_a.telfnumber != '':
            assessores_a.telfnumber = decrypt_number(assessores_a.telfnumber)
    for titulares_a in titulares_all:
        if titulares_a.telfnumber != '':
            titulares_a.telfnumber = decrypt_number(titulares_a.telfnumber)
    for titular in titulares:
        if titular.telfnumber != '':
            titular.telfnumber = decrypt_number(titular.telfnumber)

    # Crie os paginadores para cada tabela
    paginator_titular = Paginator(titulares_all, limite_titular_auth)
    paginator_assessor = Paginator(assessores_all, limite_assessor_auth)
    paginator_disparador = Paginator(disparador_all, limite_disparador_auth)

    # Obtenha os objetos paginados para a página atual
    titulares_auth = paginator_titular.get_page(page_titular_auth)
    assessores_auth = paginator_assessor.get_page(page_assessor_auth)
    disparadores_auth = paginator_disparador.get_page(page_disparador_auth)

    # Passe os objetos paginados para o contexto
    context = {
        'assessores_auth': assessores_auth,
        'titulares_auth': titulares_auth,
        'categorias': categorias,
        'titulares': titulares,
        'disparadores_auth': disparadores_auth
    }

    return render(request, 'autholist.html', context)


@has_permission_decorator('cadastrar_recursos')
def editautholist(request):
    # autholist = RegAssessor.objects.get(id=id)
    categorias = Categorias.objects.all().order_by('nome')
    return render(request, 'editautholist.html', {'categorias': categorias})


@has_permission_decorator('cadastrar_recursos')
def rec_authorization_tit(request):
    titularfinded = request.POST.get('titularfinded', '')
    catselect = request.POST.get('addcategtit', '')
    catinput = request.POST.get('lastaddtit', '')
    forregister = request.POST.get('auth_only_assec', False)
    is_checked = True if forregister else False
    authnamedtit = request.POST.get('authnamedtit', '')
    authuserchat = request.POST.get('authuserchat', '')
    authdddtit = request.POST.get('dddauttit', '')
    authteleftit = request.POST.get('telefauttit', '')
    authteleftit = encrypt_number(authteleftit)

    if titularfinded:
        titular = Titular.objects.get(id=titularfinded)

        if authdddtit != (titular.ddd):
            titular.ddd = authdddtit

        if authuserchat != (titular.id_chat_d):
            titular.id_chat_d = authuserchat

        if authteleftit != (titular.telfnumber):
            titular.telfnumber = authteleftit

        if is_checked != (titular.only_assec):
            titular.only_assec = is_checked

        try:
            titular.save()
            # Exclui da tabela de pendências
            regtitular = RegTitular.objects.get(id_t=authuserchat)
            regtitular.delete()
            # Envia uma msg no telegram informando que o cadastro foi relaizado

            chat_id = authuserchat  # Substitua pelo chat_id do usuário no Telegram, se necessário
            messages_send = ["Seu cadastro foi realizado com sucesso!!😃",
                             "A partir de agora o senhor está apto a receber todas as atualizações de ocorrências relacionadas ao senhor(a)"]

            # Crie uma corrotina para executar as chamadas assíncronas
            async def send_messages():
                for message in messages_send:
                    await send_telegram_message(chat_id, message)

            # Execute a corrotina
            asyncio.run(send_messages())

            # redireciona para a pagina de aprovações
            messages.add_message(request, messages.SUCCESS,
                                 "Mensagem encaminhada com sucesso!!")
            return redirect(reverse('add_authorization'))

        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR,
                                 "Falha durante a edição")

    elif catselect:
        # Verifica se a categoria informada já existe
        catidtit = Categorias.objects.get(nome=catselect)
        catselect = catidtit.id
        # Grava a categoria e o nome do titular na base de dados
        if userid_exists(authuserchat):
            msg = 'O id do usuário informado já está cadastrado no sistema'
            messages.add_message(request, messages.ERROR, msg)
            return redirect(reverse('add_authorization'))

        titular = Titular(categoria_id=catselect, nome=authnamedtit,
                          id_chat_d=authuserchat, only_assec=is_checked, ddd=authdddtit, telfnumber=authteleftit)
        titular.save()
        # Exclui da tabela de pendências
        regtitular = RegTitular.objects.get(id_t=authuserchat)
        regtitular.delete()
        # Envia uma msg no telegram informando que o cadastro foi relaizado

        chat_id = authuserchat  # Substitua pelo chat_id do usuário no Telegram, se necessário
        messages_send = ["Seu cadastro foi realizado com sucesso!!😃",
                         "A partir de agora o senhor está apto a receber todas as atualizações de ocorrências relacionadas ao senhor(a)"]

        # Crie uma corrotina para executar as chamadas assíncronas
        async def send_messages():
            for message in messages_send:
                await send_telegram_message(chat_id, message)

        # Execute a corrotina
        asyncio.run(send_messages())

        # redireciona para a pagina de aprovações
        messages.add_message(request, messages.SUCCESS,
                             "Mensagem encaminhada com sucesso!!")
        return redirect(reverse('add_authorization'))

    elif catinput:
        # Cadastra a categoria informada
        if category_exists(catinput):
            msg = "Erro ao cadastrar. Essa categoria já existe"
            messages.add_message(request, messages.ERROR, msg)
            return redirect(reverse('add_authorization'))

        categis = Categorias(nome=catinput)
        categis.save()
        catselect = categis.id
        # Grava a categoria e o nome do titular na base de dados
        if userid_exists(authuserchat):
            msg = 'O id do usuário informado já está cadastrado no sistema'
            messages.add_message(request, messages.ERROR, msg)
            return redirect(reverse('add_authorization'))

        titular = Titular(categoria_id=catselect, nome=authnamedtit,
                          id_chat_d=authuserchat, only_assec=is_checked, ddd=authdddtit, telfnumber=authteleftit)
        titular.save()
        # Exclui da tabela de pendências
        regtitular = RegTitular.objects.get(id_t=authuserchat)
        regtitular.delete()
        # Envia uma msg no telegram informando que o cadastro foi relaizado

        chat_id = authuserchat  # Substitua pelo chat_id do usuário no Telegram, se necessário
        messages_send = ["Seu cadastro foi realizado com sucesso!!😃",
                         "A partir de agora o senhor está apto a receber todas as atualizações de ocorrências relacionadas ao senhor"]

        # Crie uma corrotina para executar as chamadas assíncronas
        async def send_messages():
            for message in messages_send:
                await send_telegram_message(chat_id, message)

        # Execute a corrotina
        asyncio.run(send_messages())

        # redireciona para a pagina de aprovações
        messages.add_message(request, messages.SUCCESS,
                             "Mensagem encaminhada com sucesso!!")
        return redirect(reverse('add_authorization'))

    return redirect(reverse('add_authorization'))


@has_permission_decorator('cadastrar_recursos')
def rec_authorization_ass(request):

    assTitId = request.POST.get('authdepRep2', '')
    opcaoCat = request.POST.get('opcaoCat', '')
    lineCat = request.POST.get('athinlinecat', '')
    authassnametit = request.POST.get('authassnametit', '')
    authnameAss2 = request.POST.get('authnameAss2', '')
    authasschatid = request.POST.get('authasschatid', '')
    dddautass = request.POST.get('dddautass', '')
    telefautass = request.POST.get('telefautass', '')
    telefautass = encrypt_number(telefautass)

    if assTitId:
        # Grava o assesor e o Titular representado através de nome do Assessor e id do titular
        represent = Titular.objects.get(id=assTitId)

        if userid_exists(authasschatid):
            msg = 'O id do usuário informado já está cadastrado no sistema'
            messages.add_message(request, messages.ERROR, msg)
            return redirect(reverse('add_authorization'))

        assessor = Assessor(nome_assessor=authnameAss2,
                            id_chat_a=authasschatid, titular_id=represent.id, ddd=dddautass, telfnumber=telefautass)
        assessor.save()
        # Exclui Assessor da tabela de pendências
        regassessor = RegAssessor.objects.get(id_a=authasschatid)
        regassessor.delete()
        # Envia uma msg no telegram informando que o cadastro foi relaizado
        messages_send = ["Seu cadastro foi realizado com sucesso!!😃",
                         "A partir de agora o senhor está apto a receber todas as atualizações de ocorrências relacionadas ao senhor(a)"]
        msg_simple_telegram(authasschatid, messages_send)
        # redireciona para a pagina de aprovações
        messages.add_message(request, messages.SUCCESS,
                             "Mensagem encaminhada com sucesso!!")
        return redirect(reverse('add_authorization'))

    if opcaoCat:
        # Buscar a categoria pelo nome e retornar o id
        categis22 = Categorias.objects.get(nome=opcaoCat)
        # Usar o id da categoria e cadastrar o tilular

        titular3 = Titular(categoria_id=categis22.id,
                           nome=authassnametit, id_chat_d="", only_assec=True)
        titular3.save()
        titselect3 = titular3.id
        # Cadastrar o Assessor usando o id do titular
        represent3 = Titular.objects.get(id=titselect3)

        if userid_exists(authasschatid):
            msg = 'O id do usuário informado já está cadastrado no sistema'
            messages.add_message(request, messages.ERROR, msg)
            return redirect(reverse('add_authorization'))

        assessor = Assessor(nome_assessor=authnameAss2,
                            id_chat_a=authasschatid, titular_id=represent3.id, ddd=dddautass, telfnumber=telefautass)
        assessor.save()
        # Exclui Assessor da tabela de pendências
        regassessor = RegAssessor.objects.get(id_a=authasschatid)
        regassessor.delete()
        # Envia uma msg no telegram informando que o cadastro foi relaizado
        messages_send = ["Seu cadastro foi realizado com sucesso!!😃",
                         "A partir de agora o senhor está apto a receber todas as atualizações de ocorrências relacionadas ao senhor(a)"]
        msg_simple_telegram(authasschatid, messages_send)
        # redireciona para a pagina de aprovações
        messages.add_message(request, messages.SUCCESS,
                             "Mensagem encaminhada com sucesso!!")
        return redirect(reverse('add_authorization'))

    if lineCat:
        # Cadastra a categoria informada
        if category_exists(lineCat):
            msg = "Erro ao cadastrar categoria"
            messages.add_message(request, messages.ERROR, msg)
            return redirect(reverse('add_authorization'))
        categis2 = Categorias(nome=lineCat)
        categis2.save()
        catselect2 = categis2.id
        # Grava a categoria e o nome do titular na base de dados

        titular2 = Titular(categoria_id=catselect2,
                           nome=authassnametit, id_chat_d="", only_assec=True)
        titular2.save()
        titselect2 = titular2.id
        # Grava o assesor e o Titular representado através de nome do Assessor e id do titular
        represent2 = Titular.objects.get(id=titselect2)

        if userid_exists(authasschatid):
            msg = 'O id do usuário informado já está cadastrado no sistema'
            messages.add_message(request, messages.ERROR, msg)
            return redirect(reverse('add_authorization'))

        assessor = Assessor(nome_assessor=authnameAss2,
                            id_chat_a=authasschatid, titular_id=represent2.id, ddd=dddautass, telfnumber=telefautass)
        assessor.save()
        # Exclui Assessor da tabela de pendências
        regassessor = RegAssessor.objects.get(id_a=authasschatid)
        regassessor.delete()
        # Envia uma msg no telegram informando que o cadastro foi relaizado
        messages_send = ["Seu cadastro foi realizado com sucesso!!😃",
                         "A partir de agora o senhor está apto a receber todas as atualizações de ocorrências relacionadas ao senhor(a)"]
        msg_simple_telegram(authasschatid, messages_send)
        # redireciona para a pagina de aprovações
        messages.add_message(request, messages.SUCCESS,
                             "Mensagem encaminhada com sucesso!!")
        return redirect(reverse('add_authorization'))

    else:
        messages.add_message(request, messages.ERROR,
                             "Erro durante o registro")
        return redirect(reverse('add_authorization'))


@has_permission_decorator('cadastrar_recursos')
def auth_deleta_titular(request, titular_id):
    # Exclui o usuário titular do banco de espera por aprovações
    titular = get_object_or_404(RegTitular, id=titular_id)
    authuserchat = titular.id_t
    titular.delete()

    # Encaminha mensagem ao usuario do telegram
    try:
        chat_id = authuserchat  # Substitua pelo chat_id do usuário no Telegram, se necessário
        messages_send = ["Infelizmente seu cadastro não foi aprovado 😔",
                         "Entre em contato com nossa central através da Opção 'Ajuda' no menu abaixo para solucionar-mos o problema"]

        # Crie uma corrotina para executar as chamadas assíncronas
        async def send_messages():
            for message in messages_send:
                await send_telegram_message(chat_id, message)

        # Execute a corrotina
        asyncio.run(send_messages())
    except:
        # Informa em caso de falhas em envio pelo telegram
        messages.error(request, 'Erro ao notificar usuário')
        return redirect(reverse('add_authorization'))

    # Exclui o usuário titular do banco de espera por aprovações
    messages.success(
        request, 'Titular excluído da lista de espera com sucesso.')
    return redirect(reverse('add_authorization'))


@has_permission_decorator('cadastrar_recursos')
def auth_deleta_assessor(request, assessor_id):
    # Exclui o usuário assessor do banco de espera por aprovações
    assessor = get_object_or_404(RegAssessor, id=assessor_id)
    authuserchat = assessor.id_a
    assessor.delete()

    try:
        chat_id = authuserchat  # Substitua pelo chat_id do usuário no Telegram, se necessário
        messages_send = ["Infelizmente seu cadastro não foi aprovado 😔",
                         "Entre em contato com nossa central através da Opção 'Ajuda' no menu abaixo para solucionar-mos o problema"]

        # Crie uma corrotina para executar as chamadas assíncronas
        async def send_messages():
            for message in messages_send:
                await send_telegram_message(chat_id, message)

        # Execute a corrotina
        asyncio.run(send_messages())
    except:
        # Informa em caso de falhas em envio pelo telegram
        messages.error(request, 'Erro ao notificar usuário')
        return redirect(reverse('add_authorization'))

    # Exclui o usuário assessor do banco de espera por aprovações
    messages.success(
        request, 'Assessor excluído da lista de espera com sucesso.')
    return redirect(reverse('add_authorization'))


def auth_aceita_disparador(request):
    if request.method == "POST":
        iddisp = request.POST.get('iddisp', '')
        aprovado = AprovUser.objects.get(id=iddisp)
        decript_password = decrypt_number(aprovado.password)
        # Cria o disparador como usuario real do sistema
        user = Users.objects.create_user(first_name=aprovado.first_name, last_name=aprovado.last_name, username=aprovado.username,
                                         email=aprovado.email, password=decript_password, cargo="D", telfnumber=aprovado.telfnumber, ddd=aprovado.ddd)
        user.save()

        # Envia um email para o disparador informando que seu cadastro foi aprovado
        subject = 'Dai Cadastros | Disparadores'
        to = aprovado.email
        text_content = 'Esta é a versão em texto simples do e-mail.'
        titulo = 'Seu cadastro foi aprovado!! 😃'
        msg = 'Caro disparador. Seu cadastro foi aprovado pela administração do sistema. A partir de agora o senhor está apto a disparar mensagens relevantes para os usuários do sistema</p><p>Acesse o sistema através do link: http://localhost:8000/ e faça seu login com as credenciais cadastradas'
        send_styled_email(subject, to, text_content,  titulo, msg)

        # Exclui o disparador da tabela de pendências
        aprovado.delete()

        messages.success(request, 'Disparador aprovado com sucesso!!')
        return redirect(reverse('add_authorization'))


def auth_deleta_disparador(request):
    if request.method == "POST":
        # Recebe o id do disparador a ser deletado
        iddisp = request.POST.get('iddisp', '')
        aprovado = AprovUser.objects.get(id=iddisp)

        # Envia um email para o disparador informando que seu cadastro foi rejeitado
        subject = 'Dai Cadastros | Disparadores'
        to = aprovado.email
        text_content = 'Esta é a versão em texto simples do e-mail.'
        titulo = 'Infelizmente seu cadastro não foi aprovado 😔'
        msg = 'Caro disparador. Por algum motivo seu cadastro não foi aprovado pela administração do sistema. Entre em contato com o administrador do sistema da Dai Cadastros para buscar maiores informações.'
        send_styled_email(subject, to, text_content,  titulo, msg)

        # Exclui o disparador da tabela de aprovações
        aprovado.delete()

        messages.success(
            request, 'Disparador rejeitado. Foi encaminhada uma mensagem para o email do disparador informando a rejeição.')
        return redirect(reverse('add_authorization'))
