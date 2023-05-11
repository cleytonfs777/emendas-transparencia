import asyncio

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from dotenv import load_dotenv

from disparo.telegram_utils import send_telegram_message
from utils.crypto import decrypt_number, encrypt_number
from utils.viaturas import VIATURAS_ALL

from .decorators import has_permission_decorator
from .forms import ViaturaFilterForm
from .models import (AjudaManager, Assessor, Categorias, RegistroDisparo,
                     Titular, Viatura)
from .sync import syncronize_database

# Carregue as variáveis de ambiente
load_dotenv()

# Função para formatar o nome


def format_name(full_name):
    # Lista de exceções que devem ser mantidas em minúsculas
    exceptions = ['de', 'da', 'das', 'do', 'dos']

    # Separa o nome completo em palavras
    name_parts = full_name.split()

    # Converte cada palavra de acordo com as regras especificadas
    formatted_parts = []
    for part in name_parts:
        if part.lower() in exceptions:
            formatted_parts.append(part.lower())
        else:
            formatted_parts.append(part.capitalize())

    # Combina as palavras formatadas em um único nome completo
    formatted_name = ' '.join(formatted_parts)
    return formatted_name


def viatura_exists(data_placa):
    viatura = Viatura.objects.filter(placa=data_placa).first()
    if viatura:
        return True
    else:
        return False


def userid_exists(data_userid):
    if data_userid == "":
        return False
    titular = Titular.objects.filter(id_chat_d=data_userid).first()
    assessor = Assessor.objects.filter(id_chat_a=data_userid).first()
    if titular or assessor:
        return True
    else:
        return False


def category_exists(cat_sel):

    categoria = Categorias.objects.filter(nome=cat_sel).first()
    if categoria:
        return True
    else:
        return False


def home(request):
    return redirect(reverse('enviar_disparo'))


@has_permission_decorator('cadastrar_recursos')
def cadastrar(request):
    titulares = Titular.objects.all()
    categorias = Categorias.objects.all()
    return render(request, 'cadastrar.html', {'titulares': titulares, 'categorias': categorias, 'viaturas_l': VIATURAS_ALL})


@has_permission_decorator('cadastrar_recursos')
def editar_titular(request, id):

    if request.method == 'POST':

        if request.POST.get('only_assec') == 'on':
            only_assec_trat = True
        else:
            only_assec_trat = False

        titular = Titular.objects.get(id=id)
        if (request.POST.get('categoria')) != (titular.categoria):
            categ_sel = request.POST.get('categoria')
            categ = Categorias.objects.get(nome=categ_sel)
            titular.categoria = categ

        if (request.POST.get('nome')) != (titular.nome):
            titular.nome = request.POST.get('nome')

        if (request.POST.get('dddmodaltit')) != (titular.ddd):
            titular.ddd = request.POST.get('dddmodaltit')

        if (request.POST.get('idtelegtit')) != (titular.id_chat_d):
            # Verifica se o id do usuário já está cadastrado no sistema
            try:
                if userid_exists(request.POST.get('idtelegtit')):
                    msg = 'O id do usuário informado já está cadastrado no sistema'
                    messages.add_message(request, messages.ERROR, msg)
                    return redirect(reverse('listar'))
            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR,
                                     "Falha durante a edição")

            titular.id_chat_d = request.POST.get('idtelegtit')

        # Encripta o telefone para comparar as hashs
        telef_crypt = encrypt_number(request.POST.get('telefmodaltit'))
        if (telef_crypt) != (titular.telfnumber):
            titular.telfnumber = telef_crypt

        if only_assec_trat != (titular.only_assec):
            titular.only_assec = only_assec_trat

        try:
            titular.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Edição realizada com sucesso!!")
        except Exception as e:
            print(e)

            messages.add_message(request, messages.ERROR,
                                 "Falha durante a edição")

    # recuperar o número da página e o nome da tabela da sessão
    page_titular = request.session.get('page_titular', 1)
    tabela = request.session.get('tabela', 'titular')

    # redirecionar para a página com os parâmetros corretos
    return redirect(f"{reverse('listar')}?page_titular={page_titular}&tabela={tabela}")


@has_permission_decorator('cadastrar_recursos')
def editar_assessor(request, id):

    assessor = Assessor.objects.get(id=id)

    if request.method == 'POST':
        # Verifica se o id do usuário já está cadastrado no sistema
        try:
            if userid_exists(request.POST.get('idtelegtit')):
                msg = 'O id do usuário informado já está cadastrado no sistema'
                messages.add_message(request, messages.ERROR, msg)
                return redirect(reverse('listar'))
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR,
                                 "Falha durante a edição")

        titular_id = request.POST.get('depRep2')

        if assessor.titular is None or titular_id != str(assessor.titular.id):
            titular = Titular.objects.get(id=titular_id)
            assessor.titular = titular

        if (request.POST.get('nameAss2')) != (assessor.nome_assessor):
            assessor.nome_assessor = request.POST.get('nameAss2')

        if (request.POST.get('idtelegass')) != (assessor.id_chat_a):
            assessor.id_chat_a = request.POST.get('idtelegass')

        if (request.POST.get('dddmodalass')) != (assessor.ddd):
            assessor.ddd = request.POST.get('dddmodalass')

        # Criptografa o telefone para comparar o hash
        telef_crypt = encrypt_number(request.POST.get('telefmodalass'))
        if (telef_crypt) != (assessor.telfnumber):
            assessor.telfnumber = telef_crypt

        try:
            assessor.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Edição realizada com sucesso!!")
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR,
                                 "Falha durante a edição")

    # recuperar o número da página e o nome da tabela da sessão
    page_assessor = request.session.get('page_assessor', 1)
    tabela = request.session.get('tabela', 'assessor')

    # redirecionar para a página com os parâmetros corretos
    return redirect(f"{reverse('listar')}?page_assessor={page_assessor}&tabela={tabela}")


@has_permission_decorator('cadastrar_recursos')
def editar_viatura(request, id):

    viatura = Viatura.objects.get(id=id)

    if request.method == 'POST':

        titular_id = request.POST.get('tipoDep3')

        if viatura.titular is None or titular_id != str(viatura.titular.id):
            titular = Titular.objects.get(id=titular_id)
            viatura.titular = titular

        if (request.POST.get('tipoVit2')) != (viatura.tipo):
            viatura.tipo = request.POST.get('tipoVit2')

        if (request.POST.get('placaVit2')) != (viatura.placa):
            viatura.placa = request.POST.get('placaVit2')

        try:
            viatura.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Edição realizada com sucesso!!")
        except:
            messages.add_message(request, messages.ERROR,
                                 "Falha durante a edição")

    # recuperar o número da página e o nome da tabela da sessão
    page_viatura = request.session.get('page_viatura', 1)
    tabela = request.session.get('tabela', 'viatura')

    # redirecionar para a página com os parâmetros corretos
    return redirect(f"{reverse('listar')}?page_viatura={page_viatura}&tabela={tabela}")


@has_permission_decorator('cadastrar_recursos')
def deleta_titular(request, titular_id):
    titular = get_object_or_404(Titular, id=titular_id)
    titular.delete()
    messages.success(request, 'Titular excluído com sucesso.')

    # Se 'page_titular' não existir, usa '1' como padrão
    page_titular = request.GET.get('page_titular', '1')
    # Se 'tabela' não existir, usa 'default_table' como padrão
    tabela = request.GET.get('tabela', 'default_table')

    # recuperar o número da página e o nome da tabela da sessão
    # page_titular = request.session.get('page_titular', 1)
    # tabela = request.session.get('tabela', 'titular')

    # redirecionar para a página com os parâmetros corretos
    return redirect(f"{reverse('listar')}?page_titular={page_titular}&tabela={tabela}")


@has_permission_decorator('cadastrar_recursos')
def deleta_assessor(request, id):
    assessor = get_object_or_404(Assessor, id=id)
    assessor.delete()
    messages.success(request, 'Assessor excluído com sucesso.')

    # Se 'page_assessor' não existir, usa '1' como padrão
    page_assessor = request.GET.get('page_assessor', '1')
    # Se 'tabela' não existir, usa 'default_table' como padrão
    tabela = request.GET.get('tabela', 'assessor')

    # redirecionar para a página com os parâmetros corretos
    return redirect(f"{reverse('listar')}?page_assessor={page_assessor}&tabela={tabela}")


@has_permission_decorator('cadastrar_recursos')
def deleta_viatura(request, id):
    viatura = get_object_or_404(Viatura, id=id)
    viatura.delete()
    messages.success(request, 'Viatura excluído com sucesso.')

    # Se 'page_viatura' não existir, usa '1' como padrão
    page_viatura = request.GET.get('page_viatura', '1')
    # Se 'tabela' não existir, usa 'default_table' como padrão
    tabela = request.GET.get('tabela', 'viatura')

    # redirecionar para a página com os parâmetros corretos
    return redirect(f"{reverse('listar')}?page_viatura={page_viatura}&tabela={tabela}")


@has_permission_decorator('cadastrar_recursos')
def listar(request):

    # Extraia o valor do parâmetro tabela
    tabela = request.GET.get('tabela', '')
    print(f"tabela: {tabela}")

    # Obtenha o número da página atual para cada tabela
    page_titular = request.GET.get('page_titular', '1')
    page_assessor = request.GET.get('page_assessor', '1')
    page_viatura = request.GET.get('page_viatura', '1')

    # Limite de exibições de arquivos por página
    limite_titular = '10'
    limite_assessor = '10'
    limite_viatura = '10'

    # Consulte todos os objetos
    titulares_all = Titular.objects.all().order_by('categoria', 'nome')
    assessores_all = Assessor.objects.all().order_by('titular', 'nome_assessor')
    viaturas_all = Viatura.objects.all().order_by('titular', 'tipo', 'placa')
    categorias = Categorias.objects.all().order_by('nome')

    if tabela == 'titular':

        search_nome_tit = request.GET.get('search_nome_tit', '')
        search_categoria_tit = request.GET.get('search_categoria_tit', '')

        # Filtragem pelo nome do titular
        if search_nome_tit:
            titulares_all = titulares_all.filter(
                nome__icontains=search_nome_tit)

        # Filtragem pela categoria
        if search_categoria_tit:
            titulares_all = titulares_all.filter(
                categoria__nome__icontains=search_categoria_tit)

    if tabela == 'assessor':

        search_nome_ass = request.GET.get('search_nome_ass', '')
        search_titular_ass = request.GET.get('search_titular_ass', '')

        # Filtragem pelo nome do assessor
        if search_nome_ass:
            titulares_all = titulares_all.filter(
                nome_assessor__icontains=search_nome_ass)

        # Filtragem pela categoria
        if search_titular_ass:
            titulares_all = titulares_all.filter(
                titular__nome__icontains=search_titular_ass)

    if tabela == 'viatura':

        search_titular = request.GET.get('search_titular', '')
        search_placa = request.GET.get('search_placa', '')
        search_tipo = request.GET.get('search_tipo', '')

        # Adicione a filtragem por titular aqui
        if search_titular:
            viaturas_all = viaturas_all.filter(
                titular__nome__icontains=search_titular
            )

        # Adicione a filtragem por placa aqui
        if search_placa:
            viaturas_all = viaturas_all.filter(
                placa__icontains=search_placa
            )

        # Adicione a filtragem por tipo aqui
        if search_tipo:
            viaturas_all = viaturas_all.filter(
                tipo__icontains=search_tipo
            )

    # Desencriptar os dados telfnumber
    for titular in titulares_all:
        if titular.telfnumber != '':
            titular.telfnumber = decrypt_number(titular.telfnumber)
    for assessor in assessores_all:
        if assessor.telfnumber != '':
            assessor.telfnumber = decrypt_number(assessor.telfnumber)

    # Crie os paginadores para cada tabela
    paginator_titular = Paginator(titulares_all, limite_titular)
    paginator_assessor = Paginator(assessores_all, limite_assessor)
    paginator_viatura = Paginator(viaturas_all, limite_viatura)

    # Obtenha os objetos paginados para a página atual
    titulares = paginator_titular.get_page(page_titular)
    assessores = paginator_assessor.get_page(page_assessor)
    viaturas = paginator_viatura.get_page(page_viatura)

    # armazenar o número da página e a tabela na sessão
    request.session['page_titular'] = request.GET.get('page_titular', 1)
    request.session['page_assessor'] = request.GET.get('page_assessor', 1)
    request.session['page_viatura'] = request.GET.get('page_viatura', 1)
    request.session['tabela'] = request.GET.get('tabela', 'titular')

    # Passe os objetos paginados para o contexto
    if tabela == 'viatura':
        print("Entrou em viatura")

        context = {
            'titulares': titulares,
            'assessores': assessores,
            'viaturas': viaturas,
            'categorias': categorias,
            'titulares_all': titulares_all,
            'viaturas_l': VIATURAS_ALL,
            'search_titular': search_titular,
            'search_tipo': search_tipo,
            'search_placa': search_placa,
            'tabela': tabela,
        }
    elif tabela == 'titular':

        print("Entrou em titular")
        context = {
            'titulares': titulares,
            'assessores': assessores,
            'viaturas': viaturas,
            'categorias': categorias,
            'titulares_all': titulares_all,
            'viaturas_l': VIATURAS_ALL,
            'search_nome_tit': search_nome_tit,
            'search_categoria_tit': search_categoria_tit,
            'tabela': tabela,
        }

    else:

        print("Entrou em assessor")
        context = {
            'titulares': titulares,
            'assessores': assessores,
            'viaturas': viaturas,
            'categorias': categorias,
            'titulares_all': titulares_all,
            'viaturas_l': VIATURAS_ALL,
            'search_nome_ass': search_nome_ass,
            'search_titular_ass': search_titular_ass,
            'tabela': tabela,
        }

    return render(request, 'listar.html', context)


@has_permission_decorator('cadastrar_recursos')
def processar_titular(request):
    if request.method == 'POST':
        # Processar o primeiro formulário
        catdep = request.POST.get('opcaoCat', '')
        nomed = request.POST.get('nameDep', '')
        idd = request.POST.get('idDep', '')
        reInfo = request.POST.get('reInfo', '')
        ddd = request.POST.get('dddtit', '')
        telf = request.POST.get('telefonetit', '')
        # Criptografa o telefone
        telf = encrypt_number(telf)

        reInfo = True if reInfo == 'on' else False

        if catdep == "" or nomed == "":
            msg = "Todos os campos devem estar preenchidos"
            messages.add_message(request, messages.ERROR, msg)
            return redirect(reverse('cadastrar'))
        elif reInfo == False and idd == "":
            msg = 'Apenas o assessor recebe a informação" está desativada deve ser passado o ID do usuário'
            messages.add_message(request, messages.ERROR, msg)
            return redirect(reverse('cadastrar'))
        else:
            cat_op = Categorias.objects.get(nome=catdep)
            if userid_exists(idd):
                msg = 'O id do usuário informado já está cadastrado no sistema'
                messages.add_message(request, messages.ERROR, msg)
                return redirect(reverse('cadastrar'))

            titular = Titular(categoria=cat_op, nome=nomed, id_chat_d=idd,
                              only_assec=reInfo, ddd=ddd, telfnumber=telf)
            titular.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Cadastro de titular realizado com sucesso!!")
            return redirect(reverse('cadastrar'))

    # Retornar uma resposta HTTP padrão
    return HttpResponse("O formulário não foi enviado.")


@has_permission_decorator('cadastrar_recursos')
def processar_assessor(request):
    if request.method == 'POST':
       # Processar o primeiro formulário
        depRep = request.POST.get('depRep', '')
        nameAss = request.POST.get('nameAss', '')
        idAss = request.POST.get('idAss', '')
        dddass = request.POST.get('dddass', '')
        telefoneass = request.POST.get('telefoneass', '')
        # Criptografa o telefone
        telefoneass = encrypt_number(telefoneass)
        print(depRep, nameAss, idAss)

        represent = Titular.objects.get(id=depRep)

        if represent == "" or nameAss == "":
            msg = "Todos os campos devem estar preenchidos"
            messages.add_message(request, messages.ERROR, msg)
            return redirect(reverse('cadastrar'))
        else:
            if userid_exists(idAss):
                msg = 'O id do usuário informado já está cadastrado no sistema'
                messages.add_message(request, messages.ERROR, msg)
                return redirect(reverse('cadastrar'))

            assessor = Assessor(nome_assessor=nameAss, id_chat_a=idAss,
                                titular=represent, ddd=dddass, telfnumber=telefoneass)
            assessor.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Cadastro de Assessor realizado com sucesso!!")
            return redirect(reverse('cadastrar'))

    # Retornar uma resposta HTTP padrão
    return HttpResponse("O formulário não foi enviado.")


@has_permission_decorator('cadastrar_recursos')
def processar_viatura(request):
    if request.method == 'POST':
       # Processar o primeiro formulário
        tipoVit = request.POST.get('tipoVit', '')
        placaVit = request.POST.get('placaVit', '')
        tipoDep = request.POST.get('tipoDep', '')

        represent = Titular.objects.get(id=tipoDep)

        print(tipoVit, placaVit, represent)

        if tipoVit == "" or placaVit == "" or tipoDep == "":
            msg = "Todos os campos devem estar preenchidos"
            messages.add_message(request, messages.ERROR, msg)
            return redirect(reverse('cadastrar'))
        else:
            if viatura_exists(placaVit):
                msg = 'Essa placa de viatura já está cadastrado no sistema'
                messages.add_message(request, messages.ERROR, msg)
                return redirect(reverse('cadastrar'))
            viatura = Viatura(tipo=tipoVit, placa=placaVit, titular=represent)
            viatura.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Cadastro de Viatura realizado com sucesso!!")
            return redirect(reverse('cadastrar'))

    # Retornar uma resposta HTTP padrão
    return HttpResponse("O formulário não foi enviado.")


@has_permission_decorator('cadastrar_recursos')
def add_categoria(request):
    try:
        cat_receb = request.POST.get('nomeCat2', '')
        if category_exists(cat_receb):
            msg = "Erro ao cadastrar categoria"
            messages.add_message(request, messages.ERROR, msg)
            return redirect(reverse('cadastrar'))

        categoria = Categorias(nome=cat_receb)
        categoria.save()
        msg = "Categoria adicionada com sucesso!!"
        messages.add_message(request, messages.SUCCESS, msg)
        return redirect(reverse('cadastrar'))
    except Exception as e:
        print(e)
        msg = "Erro ao cadastrar categoria"
        messages.add_message(request, messages.ERROR, msg)
        return redirect(reverse('cadastrar'))


@has_permission_decorator('cadastrar_recursos')
def sync_database(request):

    # Sincronizar o banco de dados
    dados_sinc = syncronize_database()
    if dados_sinc < 0:
        msg = "Erro ao sincronizar o banco de dados"
        messages.add_message(request, messages.ERROR, msg)
        return redirect(reverse('cadastrar'))
    else:
        msg = f"{dados_sinc} registros sincronizados com sucesso!!"
        messages.add_message(request, messages.SUCCESS, msg)
        return redirect(reverse('cadastrar'))


@has_permission_decorator('cadastrar_recursos')
def log_disparo(request):
    if request.method == "GET":
        # Obtenha o número da página atual para cada tabela
        page_registro = request.GET.get('page_registro', '1')

        # Limite de exibições de arquivos por página
        limite_registro = '10'

        registros_all = RegistroDisparo.objects.all().order_by('disparador')

        # Crie os paginadores para cada tabela
        paginator_registro = Paginator(registros_all, limite_registro)

        # Obtenha os objetos paginados para a página atual
        registros = paginator_registro.get_page(page_registro)

        return render(request, 'log_disparo.html', {'registros': registros})


@has_permission_decorator('cadastrar_recursos')
def ajuda_manager(request):
    if request.method == "GET":
        # Obtenha o número da página atual para cada tabela
        page_ajuda = request.GET.get('page_ajuda', '1')

        # Limite de exibições de arquivos por página
        limite_ajuda = '10'

        ajudas_all = AjudaManager.objects.all().order_by('nome')

        # Crie os paginadores para cada tabela
        paginator_ajuda = Paginator(ajudas_all, limite_ajuda)

        # Obtenha os objetos paginados para a página atual
        ajudas = paginator_ajuda.get_page(page_ajuda)

        for ajuda in ajudas:
            ajuda.telefone = decrypt_number(ajuda.telefone)

        return render(request, 'ajuda_manager.html', {'ajudas': ajudas})


@has_permission_decorator('cadastrar_recursos')
def responde_user(request):
    if request.method == 'POST':
        usertelegram = request.POST.get('usertelegram', '')
        resposta = request.POST.get('resposta', '')
        h3_text = request.POST.get('h3_text', '')
        msgpadrao = request.POST.get('msgpadrao', '')
        modalidentif = request.POST.get('modalidentif', '')

        # return HttpResponse(f"usertelegram: {usertelegram} resposta: {resposta} h3_text: {h3_text} msgpadrao: {msgpadrao} modalidentif: {modalidentif}")

        msg_p = []
        if msgpadrao:
            msg_p.append(
                f"Caro usuario. Verificamos sua solicitação com o tema: '{h3_text}'. Estamos trabalhando para resolver o problema. Em breve entraremos em contato com o senhor para resolução")
        else:
            msg1 = "Caro usuario. Analisamos o problema apresentado e trouxemos as seguintes informações:"
            msg2 = resposta
            msg3 = "Nos colocamos a diposição para sanar quaisquer outras dúvidas"
            msg_p.append(msg1)
            msg_p.append(msg2)
            msg_p.append(msg3)

        # Remova do Banco de ajuda o registro de ajuda
        ajudamanager = AjudaManager.objects.filter(id=modalidentif)
        ajudamanager.delete()

        chat_id = usertelegram  # Substitua pelo chat_id do usuário no Telegram, se necessário

        # Crie uma corrotina para executar as chamadas assíncronas

        async def send_messages():
            for message in msg_p:
                await send_telegram_message(chat_id, message)

        # Execute a corrotina
        asyncio.run(send_messages())

        # redireciona para a pagina de aprovações
        messages.add_message(request, messages.SUCCESS,
                             "Resposta encaminhada com sucesso!!")
        return redirect(reverse('ajuda_manager'))
