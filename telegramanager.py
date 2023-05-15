import datetime
import os
import re

import psycopg2
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            ReplyKeyboardMarkup)

from utils.crypto import decrypt_number, encrypt_number

load_dotenv()

# INICIO OPERAÇÕES COM BANCO DE DADOS


class Database:

    def __init__(self, host, database, user, password):

        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def close_connection(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def __del__(self):
        self.close_connection()

    def inserir_dados_help(self, nome, id_user, categoria, telefone, mensagem, tipo):
        data_atual = datetime.datetime.now()
        telefone = encrypt_number(telefone)
        sql = f"""INSERT INTO cadastrar_ajudamanager (nome, id_user, categoria, telefone, mensagem, tema, data)
                VALUES ('{nome}', '{id_user}', '{categoria}', '{telefone}', '{mensagem}', '{tipo}', '{data_atual}')"""
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def inserir_dado_tit(self, nome_cat, nome_tit, id_t, only_assec, ddd, telfnumber):
        telfnumber = encrypt_number(telfnumber)
        sql = f"INSERT INTO disparo_regtitular (nome_cat, nome_tit, id_t, only_assec, ddd, telfnumber) VALUES ('{nome_cat}', '{nome_tit}', '{id_t}', '{only_assec}', '{ddd}', '{telfnumber}')"
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def busca_banco_tit(self, id):
        sql = f"SELECT * FROM disparo_regtitular WHERE id_t = CAST({id} AS VARCHAR);"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        # Descobrir o índice do campo 'telfnumber' na tupla
        column_names = [desc[0] for desc in cur.description]
        telfnumber_index = column_names.index('telfnumber')

        # Descriptografar o campo 'telfnumber' dos registros retornados
        decrypted_rows = []
        for row in rows:
            decrypted_telfnumber = decrypt_number(row[telfnumber_index])
            decrypted_row = row[:telfnumber_index] + \
                (decrypted_telfnumber,) + row[telfnumber_index + 1:]
            decrypted_rows.append(decrypted_row)

        return decrypted_rows

    def busca_id_tit(self, id):
        print("To dentro do busca id tit...")
        sql = f"SELECT * FROM cadastrar_titular WHERE id = {id};"
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()

        # Descobrir o índice do campo 'telfnumber' na tupla
        column_names = [desc[0] for desc in cur.description]
        telfnumber_index = column_names.index('telfnumber')
        print(f"row: {row}")
        print(f"column_names: {column_names}")
        print(f"telfnumber_index: {telfnumber_index}")

        # Descriptografar o campo 'telfnumber' do registro retornado
        decrypted_telfnumber = decrypt_number(row[telfnumber_index])
        decrypted_row = row[:telfnumber_index] + \
            (decrypted_telfnumber,) + row[telfnumber_index + 1:]

        print(f"decrypted_rows: {decrypted_row}")
        return decrypted_row

    def busca_full_tit(self, id):
        sql = f"SELECT * FROM cadastrar_titular WHERE id_chat_d = CAST({id} AS VARCHAR);"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        # Descobrir o índice do campo 'telfnumber' na tupla
        column_names = [desc[0] for desc in cur.description]
        telfnumber_index = column_names.index('telfnumber')

        # Descriptografar o campo 'telfnumber' dos registros retornados
        decrypted_rows = []
        for row in rows:
            decrypted_telfnumber = decrypt_number(row[telfnumber_index])
            decrypted_row = row[:telfnumber_index] + \
                (decrypted_telfnumber,) + row[telfnumber_index + 1:]
            decrypted_rows.append(decrypted_row)

        return decrypted_rows

    def busca_full_category(self):
        sql = f"SELECT * FROM cadastrar_categorias;"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def busca_one_category(self, id, type_c='nome'):
        if type_c == 'id':
            sql = f"SELECT * FROM cadastrar_categorias WHERE id = {id};"
        else:
            sql = f"SELECT * FROM cadastrar_categorias WHERE nome = '{id}';"
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        return row

    def atualiza_dado_tit(self, user_id, dado, valor, cat):

        if cat == 'p':
            if dado == 'nome_cat':
                sql = f"UPDATE disparo_regtitular SET nome_cat='{valor}' WHERE id_t = CAST({user_id} AS VARCHAR);"
            elif dado == 'nome_tit':
                sql = f"UPDATE disparo_regtitular SET nome_tit='{valor}' WHERE id_t = CAST({user_id} AS VARCHAR);"
            elif dado == 'id_t':
                sql = f"UPDATE disparo_regtitular SET id_t='{valor}' WHERE id_t = CAST({user_id} AS VARCHAR);"
            elif dado == 'only_assec':
                sql = f"UPDATE disparo_regtitular SET only_assec='{valor}' WHERE id_t = CAST({user_id} AS VARCHAR);"
            elif dado == 'ddd':
                sql = f"UPDATE disparo_regtitular SET ddd='{valor}' WHERE id_t = CAST({user_id} AS VARCHAR);"
            elif dado == 'telfnumber':
                valor = encrypt_number(valor)
                sql = f"UPDATE disparo_regtitular SET telfnumber='{valor}' WHERE id_t = CAST({user_id} AS VARCHAR);"
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

        elif cat == 'f':

            if dado == 'nome':
                sql = f"UPDATE cadastrar_titular SET nome='{valor}' WHERE id_chat_d = CAST({user_id} AS VARCHAR);"
            elif dado == 'only_assec':
                sql = f"UPDATE cadastrar_titular SET only_assec='{valor}' WHERE id_chat_d = CAST({user_id} AS VARCHAR);"
            elif dado == 'categoria':
                valor_id = db.busca_one_category(valor, 'nome')[0]
                sql = f"UPDATE cadastrar_titular SET categoria_id='{valor_id}' WHERE id_chat_d = CAST({user_id} AS VARCHAR);"
            elif dado == 'ddd':
                sql = f"UPDATE cadastrar_titular SET ddd='{valor}' WHERE id_chat_d = CAST({user_id} AS VARCHAR);"
            elif dado == 'telfnumber':
                valor = encrypt_number(valor)
                sql = f"UPDATE cadastrar_titular SET telfnumber='{valor}' WHERE id_chat_d = CAST({user_id} AS VARCHAR);"

            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

    def atualiza_dado_ass(self, user_id, dado, valor, cat):

        if cat == 'p':
            if dado == 'nome_ass':
                sql = f"UPDATE disparo_regassessor SET nome_ass='{valor}' WHERE id_a = CAST({user_id} AS VARCHAR);"
            elif dado == 'nome_tit':
                sql = f"UPDATE disparo_regassessor SET nome_tit='{valor}' WHERE id_a = CAST({user_id} AS VARCHAR);"
            elif dado == 'id_a':
                sql = f"UPDATE disparo_regassessor SET id_a='{valor}' WHERE id_a = CAST({user_id} AS VARCHAR);"
            elif dado == 'nome_cat':
                sql = f"UPDATE disparo_regassessor SET nome_cat='{valor}' WHERE id_a = CAST({user_id} AS VARCHAR);"
            elif dado == 'ddd':
                sql = f"UPDATE disparo_regassessor SET ddd='{valor}' WHERE id_a = CAST({user_id} AS VARCHAR);"
            elif dado == 'telfnumber':
                valor = encrypt_number(valor)
                sql = f"UPDATE disparo_regassessor SET telfnumber='{valor}' WHERE id_a = CAST({user_id} AS VARCHAR);"
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

        elif cat == 'f':

            if dado == 'nome_assessor':
                sql = f"UPDATE cadastrar_assessor SET nome_assessor='{valor}' WHERE id_chat_a = CAST({user_id} AS VARCHAR);"

            elif dado == 'ddd':
                sql = f"UPDATE cadastrar_assessor SET ddd='{valor}' WHERE id_chat_a = CAST({user_id} AS VARCHAR);"
            elif dado == 'telfnumber':
                valor = encrypt_number(valor)
                sql = f"UPDATE cadastrar_assessor SET telfnumber='{valor}' WHERE id_chat_a = CAST({user_id} AS VARCHAR);"
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

    def apagar_dado_tit(self, id):
        sql = f"DELETE FROM disparo_regtitular WHERE id={id}"
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()

    # DADOS DE ASSESSORES
    def inserir_dado_ass(self, nome_cat, nome_ass, id_a, nome_tit, ddd, telfnumber):
        telfnumber = encrypt_number(telfnumber)
        sql = f"INSERT INTO disparo_regassessor (nome_cat, nome_ass, id_a, nome_tit, ddd, telfnumber) VALUES ('{nome_cat}', '{nome_ass}', '{id_a}', '{nome_tit}', '{ddd}', '{telfnumber}')"
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def busca_banco_ass(self, id):
        sql = f"SELECT * FROM disparo_regassessor WHERE id_a = CAST({id} AS VARCHAR);"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        # Descobrir o índice do campo 'telfnumber' na tupla
        column_names = [desc[0] for desc in cur.description]
        telfnumber_index = column_names.index('telfnumber')

        # Descriptografar o campo 'telfnumber' dos registros retornados
        decrypted_rows = []
        for row in rows:
            decrypted_telfnumber = decrypt_number(row[telfnumber_index])
            decrypted_row = row[:telfnumber_index] + \
                (decrypted_telfnumber,) + row[telfnumber_index + 1:]
            decrypted_rows.append(decrypted_row)

        return decrypted_rows

    def busca_full_ass(self, id):
        sql = f"SELECT * FROM cadastrar_assessor WHERE id_chat_a = CAST({id} AS VARCHAR);"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        # Descobrir o índice do campo 'telfnumber' na tupla
        column_names = [desc[0] for desc in cur.description]
        telfnumber_index = column_names.index('telfnumber')
        print(f"telfnumber_index: {telfnumber_index}")
        # Descriptografar o campo 'telfnumber' dos registros retornados
        decrypted_rows = []
        for row in rows:
            decrypted_telfnumber = decrypt_number(row[telfnumber_index])
            print(f"decrypted_telfnumber: {decrypted_telfnumber}")
            decrypted_row = row[:telfnumber_index] + \
                (decrypted_telfnumber,) + row[telfnumber_index + 1:]
            decrypted_rows.append(decrypted_row)
        print(f"decrypted_rows: {decrypted_rows}")
        return decrypted_rows

    def apagar_dado_ass(self, sql):
        sql = f"DELETE FROM disparo_regassessor WHERE id={id}"
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()

    # APAGA DADOS
    def apaga_ass(self, user_id):

        full_ass = self.busca_full_ass(user_id)
        us_ass = self.busca_banco_ass(user_id)

        if us_ass:
            sql = f"DELETE FROM disparo_regassessor WHERE id_a = CAST({user_id} AS VARCHAR);"
            cur = self.conn.cursor()
            cur.execute(sql, (id,))
            self.conn.commit()

        elif full_ass:
            sql = f"DELETE FROM cadastrar_assessor WHERE id_chat_a = CAST({user_id} AS VARCHAR);"
            cur = self.conn.cursor()
            cur.execute(sql, (id,))
            self.conn.commit()

    def apaga_titular(self, user_id):
        full_tit = self.busca_full_tit(user_id)
        us_tit = self.busca_banco_tit(user_id)

        if us_tit:
            sql = f"DELETE FROM disparo_regtitular WHERE id_t = CAST({user_id} AS VARCHAR);"
            cur = self.conn.cursor()
            cur.execute(sql, (id,))
            self.conn.commit()

        elif full_tit:
            sql = f"UPDATE cadastrar_titular SET id_chat_d = '', ddd = '', telfnumber = '', only_assec = true WHERE id_chat_d = CAST({user_id} AS VARCHAR);"
            cur = self.conn.cursor()
            cur.execute(sql, (id,))
            self.conn.commit()

# OUTRAS FUNÇÕES


def converte_nome(frase):
    palavras_excecao = ["de", "da", "do", "das", "dos"]
    palavras = frase.split()
    nova_frase = []

    for i, palavra in enumerate(palavras):
        if palavra.lower() in palavras_excecao:
            nova_frase.append(palavra.lower())
        else:
            if len(palavra) == 1 and palavra.lower() in 'aeiou':
                if i == 0:
                    nova_frase.append(palavra.upper())
                else:
                    nova_frase.append(palavra.lower())
            else:
                nova_frase.append(palavra.capitalize())

    return ' '.join(nova_frase)


def whats_is(id_user):
    full_tit = db.busca_full_tit(id_user)
    full_ass = db.busca_full_ass(id_user)
    # Busca no banco de dados local:
    us_tit = db.busca_banco_tit(id_user)
    us_ass = db.busca_banco_ass(id_user)

    if us_ass or full_ass:
        return 'a'
    elif us_tit or full_tit:
        return 't'


def existeuser(id_user, db):
    # Busca nos registros de Titulares e assessores:
    full_tit = db.busca_full_tit(id_user)
    full_ass = db.busca_full_ass(id_user)
    # Busca no banco de dados local:
    us_tit = db.busca_banco_tit(id_user)
    us_ass = db.busca_banco_ass(id_user)
    if us_ass:
        # Verifica se o usuario tem telefone
        telef = us_ass[0][-1]
        return [True, 'Assessor', 'p', telef]

    elif full_ass:
        # Verifica se o usuario tem telefone
        telef = full_ass[0][-1]
        return [True, 'Assessor', 'f', telef]

    elif us_tit:
        # Verifica se o usuario tem telefone
        telef = us_tit[0][-1]
        return [True, us_tit[0][1], 'p', telef]

    elif full_tit:
        # Verifica se o usuario tem telefone
        telef = full_tit[0][-1]
        if (len(full_tit[0]) == 7):
            return [True, db.busca_one_category(full_tit[0][4], 'id')[1], 'f', telef]

    else:
        return [False, None, None, None]


def categoryexists(category, db):
    cat_found = db.busca_one_category(category, 'nome')
    if cat_found:
        return True
    else:
        return False
# FIM OPERAÇÕES COM BANCO DE DADOS
# Crie uma classe personalizada que herda de pyrogram.Client


class MyClient(Client):
    def __init__(self):
        # Inicialize o objeto Client e defina a variável de sessão
        super().__init__(
            "ParlamentarCBMMGBot",
            api_id=os.environ['TELEGRAM_API_ID'],
            api_hash=os.environ['TELEGRAM_API_HASH'],
            bot_token=os.environ['TELEGRAM_BOT_TOKEN'],
        )
        self.user_data = {}
        self.user_states = {}
        self.user_help = {}
        self.user_general = {}

    # Adicione um método para atualizar a variável de sessão com os dados do usuário
    def update_user_data(self, user_id, data):
        self.user_data[user_id] = data

    # Adicione um método para recuperar os dados do usuário da variável de sessão
    def get_user_data(self, user_id):
        return self.user_data.get(user_id, {})

    # Adicione um método para atualizar a variável de sessão para egeneral_session['stado']s de usuário
    def update_user_states(self, user_id, data):
        self.user_states[user_id] = data

    # Adicione um método para recuperar os egeneral_session['stado']s do usuário da variável de sessão
    def get_user_states(self, user_id):
        return self.user_states.get(user_id, {})

    # Adicione um método para atualizar a variável de sessão para egeneral_session['stado']s de usuário
    def update_user_help(self, user_id, data):
        self.user_help[user_id] = data

    # Adicione um método para recuperar os egeneral_session['stado']s do usuário da variável de sessão
    def get_user_help(self, user_id):
        return self.user_help.get(user_id, {})

    def update_user_general(self, user_id, data):
        self.user_general[user_id] = data

    def get_user_general(self, user_id):
        return self.user_general.get(user_id, {})


def registra_sess_data(user_id, data_res, chave):
    # Registra todos os dados na variavel de sessão
    user_data = app.get_user_data(user_id)
    user_data[chave] = data_res
    app.update_user_data(user_id, user_data)


def registra_user_states(user_id, data_res, chave):
    # Registra todos os dados na variavel de sessão
    user_data = app.get_user_states(user_id)
    user_data[chave] = data_res
    app.update_user_states(user_id, user_data)


def registra_user_help(user_id, data_res, chave):
    # Registra todos os dados na variavel de sessão
    user_data = app.get_user_help(user_id)
    user_data[chave] = data_res
    app.update_user_help(user_id, user_data)


def registra_user_general(user_id, data_res, chave):
    # Registra dados gerais do usuario
    user_data = app.get_user_general(user_id)
    user_data[chave] = data_res
    app.update_user_general(user_id, user_data)


def format_titular_data(user_data):
    return f"Categoria: {user_data[1]}\nNome: {user_data[2]}\nRecebe dados={user_data[4]}"


def format_assessor_data(user_data):
    return f"Nome: {user_data[2]}\nCat. Titular: {user_data[1]}\nNome Titular: {user_data[4]}"


def edit_message(chat_id, message_id, text):
    app.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)


def user_full_date(user_id):
    # Busca nos registros de Titulares e assessores:
    full_tit = db.busca_full_tit(user_id)
    full_ass = db.busca_full_ass(user_id)
    # Busca no banco de dados local:
    us_tit = db.busca_banco_tit(user_id)
    us_ass = db.busca_banco_ass(user_id)

    if (full_tit):
        return [full_tit, "T"]
    elif (full_ass):
        return [full_ass, "A"]
    elif (us_tit):
        return [us_tit, "T"]
    elif (us_ass):
        return [us_ass, "A"]
    else:
        return None


def convertbool(dats):
    recebdd = "Não" if dats == True else "Sim" if dats == False else None
    return recebdd


def update_field(user_id, field, value):

    # Busca nos registros de Titulares e assessores:
    full_tit = db.busca_full_tit(user_id)
    full_ass = db.busca_full_ass(user_id)
    # Busca no banco de dados local:
    us_tit = db.busca_banco_tit(user_id)
    us_ass = db.busca_banco_ass(user_id)

    if (full_tit):

        if field == "Categoria":
            ...
        if field == "Nome":
            print("Full Nome")
        if field == "Recebe_dados":
            print("Full Recebe_dados")

    elif (full_ass):

        if field == "Nome":
            print("Full Nome")
        if field == "Categoria_Titular":
            print("Full Categoria_Titular")
        if field == "Nome_Titular":
            print("Full Nome_Titular")

    elif (us_tit):

        if field == "Categoria":
            print("Normal Categoria")
        if field == "Nome":
            print("Normal Nome")
        if field == "Recebe_dados":
            print("Normal Recebe_dados")

    elif (us_ass):

        if field == "Nome":
            print("Normal Nome")
        if field == "Categoria_Titular":
            print("Normal Categoria_Titular")
        if field == "Nome_Titular":
            print("Normal Nome_Titular")

    else:

        return None

    # Atualizar campo no banco de dados
    # cursor.execute(f"UPDATE usuarios SET {field} = %s WHERE user_id = %s", (new_value, user_id))

    # message.reply_text(f"{field.capitalize()} atualizado com sucesso!")


def limpaddd(text):
    return ''.join(char for char in text if char.isdigit())


def generate_keyboard(cat):
    ddds = [31, 32, 33, 34, 35, 37, 38, "Outro"]
    buttons = []
    for ddd in ddds:
        buttons.append(InlineKeyboardButton(
            str(ddd), callback_data=f"{ddd}_ddd_{cat}"))

    # Divida a lista de botões em duas fileiras
    row1 = buttons[:4]
    row2 = buttons[4:]

    # Crie o teclado com as duas fileiras
    keyboard = InlineKeyboardMarkup([row1, row2])
    return keyboard


# VARIAVEIS DE ESTADOS
# Dicionário para armazenar os egeneral_session['stado']s dos usuários
user_states = {}

# Egeneral_session['stado']s possíveis
# T = Titular A = Assessor P = Principal F = Fase
EDIT_CATEGORIA_T_P = "edit_Categoria_t_p"
EDIT_NOME_T_P = "edit_Nome_t_p"
EDIT_DDD_T_P = "edit_Ddd_t_p"
EDIT_TELEFONE_T_P = "edit_Telefone_t_p"
EDIT_RECEBE_DADOS_T_P = "edit_Recebe_dados_t_p"
EDIT_CATEGORIA_T_F = "edit_Categoria_t_f"
EDIT_NOME_T_F = "edit_Nome_t_f"
EDIT_DDD_T_F = "edit_Ddd_t_f"
EDIT_TELEFONE_T_F = "edit_Telefone_t_f"
EDIT_RECEBE_DADOS_T_F = "edit_Recebe_dados_t_f"
EDIT_NOME_A_F = "edit_Nome_a_f"
EDIT_CATEGORIA_TITULAR_A_F = "edit_Categoria_Titular_a_f"
EDIT_NOME_TITULAR_A_F = "edit_Nome_Titular_a_f"
EDIT_DDD_A_F = "edit_Ddd_a_f"
EDIT_TELEFONE_A_F = "edit_Telefone_a_f"
EDIT_NOME_A_P = "edit_Nome_a_p"
EDIT_CATEGORIA_TITULAR_A_P = "edit_Categoria_Titular_a_p"
EDIT_NOME_TITULAR_A_P = "edit_Nome_Titular_a_p"
EDIT_DDD_A_P = "edit_Ddd_a_p"
EDIT_TELEFONE_A_P = "edit_Telefone_a_p"
HELP_USER_MESSAGE = "help_user_message"

# Expressões Regulares
pattern = r"Por favor, insira o novo valor para (\w+):"

# Crie a conexão com o o banco de dados
db = Database(os.environ["PGHOST"], os.environ["PGDATABASE"],
              os.environ["PGUSER"], os.environ["PGPASSWORD"])

# Crie o aplicativo
app = MyClient()


# O aplicativo captura o comando dado ao bot escolhido e oferece um texto baseado na requisição


@app.on_message(filters.command('start'))
async def inicio(Client, message):
    try:
        registra_user_states(message.chat.id, None, "state")
    except:
        pass
    teclado = ReplyKeyboardMarkup(
        [
            ['Cadastrar', 'Editar', 'Remover', 'Ajuda']
        ], resize_keyboard=True
    )
    await message.reply(
        '🤖 Seja bem vindo ao bot de atualizações em tempo real do CBMMG. Selecione uma das opções do menu 🤖', reply_markup=teclado
    )
    print(f"message.chat: {message.chat}")
    print(f"message.chat.id: {message.chat.id}")
    print(f"message.id: {message.id}")


# O que vai editar os dados do titular
@app.on_message(filters.regex("Editar"))
async def editar(Client, message):
    try:
        registra_user_states(message.chat.id, None, "state")
    except:
        pass
    if app.get_user_states(message.chat.id) == None:
        app.update_user_states(message.chat.id, {"state": None})
    print(app.get_user_states(message.chat.id))
    if existeuser(message.chat.id, db)[0]:
        obj_comp = user_full_date(message.chat.id)[0][0]
        if user_full_date(message.chat.id)[1] == "T":
            # Verifica se o antepenultimo valor é um boleano, que é o valor padrão para dados de edição de titulares
            if isinstance(obj_comp[-3], bool) and isinstance(obj_comp[-3], int):
                print(isinstance(obj_comp[-3], (int)))
                print(obj_comp[-3])
                recebdd = convertbool(obj_comp[4])
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        f"Categoria: {obj_comp[1]}", callback_data="edit_Categoria_t_p")],
                    [InlineKeyboardButton(
                        f"Nome: {obj_comp[2]}", callback_data="edit_Nome_t_p")],
                    [InlineKeyboardButton(
                        f"Recebe_dados: {recebdd}", callback_data="edit_Recebe_dados_t_p")],
                    [InlineKeyboardButton(
                        f"Telefone: ({obj_comp[-2]}) {obj_comp[-1]}", callback_data="edit_Telefone_t_p")],
                ])

                await message.reply_text("Selecione o campo que deseja editar:", reply_markup=reply_markup)

            else:
                recebdd = convertbool(obj_comp[3])

                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        f"Categoria: {db.busca_one_category(obj_comp[4],'id')[1]}", callback_data="edit_Categoria_t_f")],
                    [InlineKeyboardButton(
                        f"Nome: {obj_comp[1]}", callback_data="edit_Nome_t_f")],
                    [InlineKeyboardButton(
                        f"Recebe_dados: {recebdd}", callback_data="edit_Recebe_dados_t_f")],
                    [InlineKeyboardButton(
                        f"Telefone: ({obj_comp[-2]}) {obj_comp[-1]}", callback_data="edit_Telefone_t_f")],
                ])
                await message.reply_text("Selecione o campo que deseja editar:", reply_markup=reply_markup)

        elif user_full_date(message.chat.id)[1] == "A":
            if len(obj_comp) == 6:
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        f"Nome: {obj_comp[1]}", callback_data="edit_Nome_a_f")],
                    [InlineKeyboardButton(
                        f"Titular: {db.busca_one_category(db.busca_id_tit(obj_comp[3])[4],'id')[1]} {db.busca_id_tit(obj_comp[3])[1]}", callback_data="edit_Cat_Nome_Titular_a_f")],
                    [InlineKeyboardButton(
                        f"Telefone: ({obj_comp[-2]}) {obj_comp[-1]}", callback_data="edit_Telefone_a_f")],
                ])

                await message.reply_text("Selecione o campo que deseja editar:", reply_markup=reply_markup)
            else:
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        f"Nome: {obj_comp[2]}", callback_data="edit_Nome_a_p")],
                    [InlineKeyboardButton(
                        f"Titular: {obj_comp[1]} {obj_comp[4]}", callback_data="edit_Cat_Nome_Titular_a_p")],
                    [InlineKeyboardButton(
                        f"Telefone: ({obj_comp[-2]}) {obj_comp[-1]}", callback_data="edit_Telefone_a_p")],
                ])

                await message.reply_text("Selecione o campo que deseja editar:", reply_markup=reply_markup)

        else:
            await message.reply_text("Usuário não encontrado.")

    else:
        await message.reply_text("Usuário não cadastrado. Acione o botão 'Cadastrar' abaixo. Se não houver menu acione o comando /start")
        # Usuario não existe


# O que vai remover os dados do titular
@app.on_message(filters.regex("Remover"))
async def remover(Client, message):
    try:
        registra_user_states(message.chat.id, None, "state")
    except:
        pass
    if existeuser(message.chat.id, db)[0]:
        res = whats_is(message.chat.id)

        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    f"Sim", callback_data=f"remove_yes_{res}"),
                InlineKeyboardButton(f"Não", callback_data=f"remove_no_{res}")
            ]
        ])

        await message.reply_text("Realmente deseja apagar seu usuário? Todas as informações serão perdidas", reply_markup=reply_markup)
    else:
        await message.reply('O senhor não possui usuário cadastrado. Fineza inserir o comando /start para iniciar cadastro')


# O que vai adjudar os dados do titular
@app.on_message(filters.regex("Ajuda"))
async def adjudar(Client, message):
    TEMA_CHOICES = [
        ("NRC", "NAO SEI REALIZAR O CADASTRO"),
        ("DA", "DIFICULDADE DE ACESSO"),
        ("ED", "ERRO NOS DADOS"),
        ("NRD", "NÃO RECEBO MAIS DADOS"),
        ("NQD", "NÃO QUERO MAIS RECEBER DADOS"),
        ("TT", "TROQUEI DE TITULAR"),
        ("OT", "OUTRO")]
    if existeuser(message.chat.id, db)[0]:
        obj_comp = user_full_date(message.chat.id)[0][0]
        if user_full_date(message.chat.id)[1] == "T":
            # Verifica se o antepenultimo valor é um boleano, que é o valor padrão para dados de edição de titulares
            if isinstance(obj_comp[-3], bool) and isinstance(obj_comp[-3], int):
                registra_user_help(
                    message.chat.id, f"{obj_comp[2]}", "nome")
                registra_user_help(
                    message.chat.id, f"{obj_comp[1]}", "categoria")
                registra_user_help(
                    message.chat.id, f"({obj_comp[-2]}) {obj_comp[-1]}", "telefone")

            else:

                registra_user_help(
                    message.chat.id, f"{obj_comp[1]}", "nome")
                registra_user_help(
                    message.chat.id, f"{db.busca_one_category(obj_comp[4],'id')[1]}", "categoria")
                registra_user_help(
                    message.chat.id, f"({obj_comp[-2]}) {obj_comp[-1]}", "telefone")

        elif user_full_date(message.chat.id)[1] == "A":
            if len(obj_comp) == 6:
                registra_user_help(
                    message.chat.id, f"{obj_comp[1]}", "nome")
                registra_user_help(
                    message.chat.id, f"Assessor({db.busca_one_category(db.busca_id_tit(obj_comp[3])[4],'id')[1]} {db.busca_id_tit(obj_comp[3])[1]})", "categoria")
                registra_user_help(
                    message.chat.id, f"({obj_comp[-2]}) {obj_comp[-1]}", "telefone")

            else:

                registra_user_help(
                    message.chat.id, f"{obj_comp[2]}", "nome")
                registra_user_help(
                    message.chat.id, f"Assessor({obj_comp[1]} {obj_comp[4]})", "categoria")
                registra_user_help(
                    message.chat.id, f"({obj_comp[-2]}) {obj_comp[-1]}", "telefone")

    categ = [[InlineKeyboardButton(
        f"{b}", callback_data=f"HELP_{a}")] for a, b in TEMA_CHOICES]
    # Registra a lista no banco de dados
    reply_markup = InlineKeyboardMarkup(categ)
    await message.reply_text("Selecione o tema que deseja ajuda:", reply_markup=reply_markup)
# O vai fazer o cadastro do parlamentar


@app.on_message(filters.regex("Cadastrar"))
async def cadastrar(Client, message):
    try:
        registra_user_states(message.chat.id, None, "state")
    except:
        pass
    if existeuser(message.chat.id, db)[0]:
        await app.send_message(message.chat.id, f'O sennhor já está cadastrado como {existeuser(message.chat.id, db)[1]}')
        await app.send_message(message.chat.id, "Por favor selecione o botão 'Editar' logo abaixo, ou 'Ajuda' em caso de dúvidas")
    else:
        # Vai para o trecho TITULAR_PASSO_1 ou ASSERSSOR_PASSO_1
        opcexiste = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Titular', callback_data='T'),
                    InlineKeyboardButton('Assessor', callback_data='A'),
                ]
            ]
        )
        await message.reply('Por gentileza escolha abaixo em qual opção o senhor se enquadra', reply_markup=opcexiste)


@app.on_callback_query()
async def callback(clinet, callback_query):
    print(f"CALLBACK_QUERY É: {callback_query.data}")
    if callback_query.data.startswith("HELP"):
        registra_user_general(callback_query.message.chat.id, existeuser(
            callback_query.message.chat.id, db)[1], "help_user")
        registra_user_general(callback_query.message.chat.id, existeuser(
            callback_query.message.chat.id, db)[2], "help_tipo")
        registra_user_general(callback_query.message.chat.id, existeuser(
            callback_query.message.chat.id, db)[3], "help_telef")

        helps = app.get_user_general(callback_query.message.chat.id)
        print(f"HELP_USER É: {helps['help_user']}")
        print(f"HELP_TIPO É: {helps['help_tipo']}")
        print(f"HELP_TELEF É: {helps['help_telef']}")
        registra_user_help(callback_query.message.chat.id,
                           callback_query.data[5:], "tipo")
        if callback_query.data[5:] == "DA":
            if not helps['help_user']:
                await callback_query.message.reply_text("Por favor, selecione o botão 'Cadastrar' abaixo, ou a opção 'NAO SEI REALIZAR O CADASTRO' no menu 'Ajuda'")
            else:
                if not helps['help_telef']:
                    await callback_query.message.reply_text("Iremos orienta-lo através de contato telefônico, porém o senhor não tem telefone cadastrado")
                    await callback_query.message.reply_text("Por favor, selecione o botão 'Editar' abaixo para cadastrar seu telefone, ou a opção 'NAO SEI REALIZAR O CADASTRO' no menu 'Ajuda'")
                else:
                    # Fluxo normal de auxilio ao usuário
                    # TODO Criar variavel de ambiente para registrar natureza do questionamento e esvazia-la ao gravar
                    await callback_query.message.reply_text("Muito bem, Nos informe resumidamente o problema que o senhor(a) está enfrentando para que possamos auxilia-lo(a) da melhor forma possível")
                    registra_user_states(
                        callback_query.message.chat.id, HELP_USER_MESSAGE, "state")

        elif callback_query.data[5:] == "ED":
            if not helps['help_user']:
                await callback_query.message.reply_text("Por favor, selecione o botão 'Cadastrar' abaixo, ou a opção 'NAO SEI REALIZAR O CADASTRO' no menu 'Ajuda'")
            else:
                if not helps['help_telef']:
                    await callback_query.message.reply_text("Iremos orienta-lo através de contato telefônico, porém o senhor não tem telefone cadastrado")
                    await callback_query.message.reply_text("Por favor, selecione o botão 'Editar' abaixo para cadastrar seu telefone, ou a opção 'NAO SEI REALIZAR O CADASTRO' no menu 'Ajuda'")
                else:
                    # Fluxo normal de auxilio ao usuário
                    # TODO Criar variavel de ambiente para registrar natureza do questionamento e esvazia-la ao gravar
                    await callback_query.message.reply_text("Muito bem, Nos informe resumidamente o problema que o senhor(a) está enfrentando para que possamos auxilia-lo(a) da melhor forma possível")
                    registra_user_states(
                        callback_query.message.chat.id, HELP_USER_MESSAGE, "state")

        elif callback_query.data[5:] == "NRC":
            await callback_query.message.reply_text("Por favor, selecione o botão 'Cadastrar' abaixo")
            await callback_query.message.reply_text("Caso ainda reste duvidas veja o tutorial detalhado de como realizar o cadastro no link abaixo")
            await callback_query.message.reply_text('<a href="https://www.youtube.com/watch?v=UMSwzV-sJWI">TUTORIAL CADASTRO</a>')

        elif callback_query.data[5:] == "NRD":
            if not helps['help_user']:
                await callback_query.message.reply_text("Por favor, selecione o botão 'Cadastrar' abaixo, ou a opção 'NAO SEI REALIZAR O CADASTRO' no menu 'Ajuda'")
            else:
                if not helps['help_telef']:
                    await callback_query.message.reply_text("Iremos orienta-lo através de contato telefônico, porém o senhor não tem telefone cadastrado")
                    await callback_query.message.reply_text("Por favor, selecione o botão 'Editar' abaixo para cadastrar seu telefone, ou a opção 'NAO SEI REALIZAR O CADASTRO' no menu 'Ajuda'")
                else:
                    # Fluxo normal de auxilio ao usuário
                    # TODO Criar variavel de ambiente para registrar natureza do questionamento e esvazia-la ao gravar
                    await callback_query.message.reply_text("Muito bem, Nos informe resumidamente o problema que o senhor(a) está enfrentando para que possamos auxilia-lo(a) da melhor forma possível")
                    registra_user_states(
                        callback_query.message.chat.id, HELP_USER_MESSAGE, "state")

        elif callback_query.data[5:] == "NQD":
            if not helps['help_user']:
                await callback_query.message.reply_text("Por favor, selecione o botão 'Cadastrar' abaixo, ou a opção 'NAO SEI REALIZAR O CADASTRO' no menu 'Ajuda'")
            else:
                if not helps['help_telef']:
                    await callback_query.message.reply_text("Iremos orienta-lo através de contato telefônico, porém o senhor não tem telefone cadastrado")
                    await callback_query.message.reply_text("Por favor, selecione o botão 'Editar' abaixo para cadastrar seu telefone, ou a opção 'NAO SEI REALIZAR O CADASTRO' no menu 'Ajuda'")
                else:
                    # Fluxo normal de auxilio ao usuário
                    # TODO Criar variavel de ambiente para registrar natureza do questionamento e esvazia-la ao gravar
                    await callback_query.message.reply_text("Muito bem, Nos informe resumidamente o problema que o senhor(a) está enfrentando para que possamos auxilia-lo(a) da melhor forma possível")
                    registra_user_states(
                        callback_query.message.chat.id, HELP_USER_MESSAGE, "state")

        elif callback_query.data[5:] == "TT":
            if not helps['help_user']:
                await callback_query.message.reply_text("Por favor, selecione o botão 'Cadastrar' abaixo, ou a opção 'NAO SEI REALIZAR O CADASTRO' no menu 'Ajuda'")
            else:
                if not helps['help_telef']:
                    await callback_query.message.reply_text("Iremos orienta-lo através de contato telefônico, porém o senhor não tem telefone cadastrado")
                    await callback_query.message.reply_text("Por favor, selecione o botão 'Editar' abaixo para cadastrar seu telefone, ou a opção 'NAO SEI REALIZAR O CADASTRO' no menu 'Ajuda'")
                else:
                    # Fluxo normal de auxilio ao usuário
                    # TODO Criar variavel de ambiente para registrar natureza do questionamento e esvazia-la ao gravar
                    await callback_query.message.reply_text("Muito bem, Nos informe resumidamente o problema que o senhor(a) está enfrentando para que possamos auxilia-lo(a) da melhor forma possível")

                    registra_user_states(
                        callback_query.message.chat.id, HELP_USER_MESSAGE, "state")

        elif callback_query.data[5:] == "OT":
            if not helps['help_user']:
                await callback_query.message.reply_text("Por favor, selecione o botão 'Cadastrar' abaixo, ou a opção 'NAO SEI REALIZAR O CADASTRO' no menu 'Ajuda'")
            else:
                if not helps['help_telef']:
                    await callback_query.message.reply_text("Iremos orienta-lo através de contato telefônico, porém o senhor não tem telefone cadastrado")
                    await callback_query.message.reply_text("Por favor, selecione o botão 'Editar' abaixo para cadastrar seu telefone, ou a opção 'NAO SEI REALIZAR O CADASTRO' no menu 'Ajuda'")
                else:
                    # Fluxo normal de auxilio ao usuário
                    # TODO Criar variavel de ambiente para registrar natureza do questionamento e esvazia-la ao gravar
                    await callback_query.message.reply_text("Muito bem, Nos informe resumidamente o problema que o senhor(a) está enfrentando para que possamos auxilia-lo(a) da melhor forma possível")
                    registra_user_states(
                        callback_query.message.chat.id, HELP_USER_MESSAGE, "state")

    # TITULAR_PASSO_1
    elif callback_query.data == 'T':
        # Verifica se já tem o objeto de sessão. Se não tiver cria um para titular
        if app.get_user_data(callback_query.message.chat.id) == None:
            app.update_user_data(callback_query.message.chat.id, {
                                 "is_titular": True, "nome_cat": "", "nome_tit": "", "ddd_tit": "", "tel_tit": "",  "id_t": "",  "only_assec": ""})

        await app.send_message(callback_query.message.chat.id, f'Perfeito. Entendemos que o senhor é o titular')
        await app.send_message(callback_query.message.chat.id, f'Por gentileza nos informe a categoria que melhor representa o senhor. Ex:. Deputado(a) Federal, Deputado(a) Estadual, Senador(a), Promotor(a), Juiz(a), etc.')
        # Vai para TITULAR_PASSO_2

    # ASSERSSOR_PASSO_1
    elif callback_query.data == 'A':
        # Verifica se já tem o objeto de sessão. Se não tiver cria um para assessor
        if app.get_user_data(callback_query.message.chat.id) == None:
            app.update_user_data(callback_query.message.chat.id, {
                                 "is_titular": False, "nome_cat": "", "nome_ass": "", "ddd_ass": "", "tel_ass": "",  "id_a": "",  "nome_tit": ""})

        await app.send_message(callback_query.message.chat.id, f'Perfeito. Tudo ok senhor assessor')
        await app.send_message(callback_query.message.chat.id, f"Agora me informe o nome pelo qual o(a) senhor(a) gostaria de ser chamado(a).")
        # Vai para ASSESSOR_PASSO_2

    # TITULAR_PASSO_4
    elif callback_query.data == 'queretamb':
        registra_sess_data(callback_query.message.chat.id, True, 'only_assec')
        await app.send_message(callback_query.message.chat.id, f'Estamos indo bem 😀. O senhor receberá todas as informações de ocorrencias relativos a recursos encaminhados pelo senhor!')
        await app.send_message(callback_query.message.chat.id, f'Para finalizar solicitamos que o senhor nos informe o melhor numero de telefone para contato. Não se preocupe por o numero será salvo de maneira criptografada')
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    f"Sim", callback_data="authtel_t_sim"),
                InlineKeyboardButton(
                    f"Não", callback_data="authtel_t_nao")
            ]
        ])

        await callback_query.message.reply_text("Gostaria de fornecer seu telefone?", reply_markup=reply_markup)

    elif callback_query.data == 'apmeuacess':
        registra_sess_data(callback_query.message.chat.id, False, 'only_assec')
        await app.send_message(callback_query.message.chat.id, f'Encaminharemos todas as mensagem apenas ao seu assessor. Fique tranquilo o Senhor não será notificado!')
        await app.send_message(callback_query.message.chat.id, f'Para finalizar solicitamos que o senhor nos informe o melhor numero de telefone para contato')
        await app.send_message(callback_query.message.chat.id, f'Não se preocupe por o numero será salvo de maneira criptografada')
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    f"Sim", callback_data="authtel_t_sim"),
                InlineKeyboardButton(
                    f"Não", callback_data="authtel_t_nao")
            ]
        ])

        await callback_query.message.reply_text("Gostaria de fornecer seu telefone?", reply_markup=reply_markup)

    # QUERY PARA DEFINIR O TIPO DE DEPUTADO QUE O ASSESSOR AUXILIA
    elif callback_query.data.endswith("_editando"):
        db.atualiza_dado_tit(callback_query.message.chat.id,
                             'categoria', callback_query.data[:-9], 'f')
        await callback_query.message.reply_text(f"Edição realizada com sucesso!!")
        print(callback_query.data[:-9])

    elif callback_query.data.startswith("edit_"):
        registra_user_general(callback_query.message.chat.id,
                              callback_query.data[5:-4], "field")
        field_session = app.get_user_general(callback_query.message.chat.id)
        if callback_query.data[-3] == 't':
            print(field_session['field'])
            if field_session['field'] == 'Categoria':
                if callback_query.data[-1] == 'f':
                    print("Altera categoria do full")
                    categorias = [a[1] for a in db.busca_full_category()]
                    categ = [[InlineKeyboardButton(
                        f"{a}", callback_data=f"{a}_editando")] for a in categorias]
                    # Registra a lista no banco de dados
                    reply_markup = InlineKeyboardMarkup(categ)

                    await callback_query.message.reply_text("Selecione a nova categoria desejada:", reply_markup=reply_markup)

                elif callback_query.data[-1] == 'p':
                    print("Altera categoria do edit")
                    await callback_query.message.reply_text(f"Por favor, insira o valor para edição ao campo {field_session['field']}:")
                    registra_user_states(
                        callback_query.message.chat.id, EDIT_CATEGORIA_T_P, "state")

            elif field_session['field'] == 'Nome':
                if callback_query.data[-1] == 'f':
                    print("Altera nome do full")
                    await callback_query.message.reply_text(f"Por favor, insira o valor para edição ao campo {field_session['field']}:")
                    registra_user_states(
                        callback_query.message.chat.id, EDIT_NOME_T_F, "state")

                elif callback_query.data[-1] == 'p':
                    print("Altera nome do edit")
                    await callback_query.message.reply_text(f"Por favor, insira o valor para edição ao campo {field_session['field']}:")
                    registra_user_states(
                        callback_query.message.chat.id, EDIT_NOME_T_P, "state")

            elif field_session['field'] == 'Telefone':
                if callback_query.data[-1] == 'f':
                    print("Altera o DDD")
                    await callback_query.message.reply_text(f"Vamos alterar primeiro o seu DDD")
                    await callback_query.message.reply_text(f"Insira os dois digitos do seu DDD sem o zero")
                    # TODO: Implementar edição de ddd e telefone
                    registra_user_states(
                        callback_query.message.chat.id, EDIT_DDD_T_F, "state")

                elif callback_query.data[-1] == 'p':
                    await callback_query.message.reply_text(f"Vamos alterar primeiro o seu DDD")
                    await callback_query.message.reply_text(f"Insira os dois digitos do seu DDD sem o zero")
                    # TODO: Implementar edição de ddd e telefone
                    registra_user_states(
                        callback_query.message.chat.id, EDIT_DDD_T_P, "state")

            elif field_session['field'] == 'Recebe_dados':
                if callback_query.data[-1] == 'f':
                    print("Altera recebe dados do full")
                    reply_markup = InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(
                                f"Sim", callback_data="sim_receiv_f"),
                            InlineKeyboardButton(
                                f"Não", callback_data="nao_receiv_f")
                        ]
                    ])

                    await callback_query.message.reply_text("Deseja receber resumos e imagens de ocorrencias em seu telegram?", reply_markup=reply_markup)

                elif callback_query.data[-1] == 'p':
                    print("Altera recebe dados do edit")
                    reply_markup = InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(
                                f"Sim", callback_data="sim_receiv_p"),
                            InlineKeyboardButton(
                                f"Não", callback_data="nao_receiv_p")
                        ]
                    ])

                    await callback_query.message.reply_text("Deseja receber resumos e imagens de ocorrencias em seu telegram?", reply_markup=reply_markup)

            else:
                print("Não é igual")
                await callback_query.message.reply_text(f"Por favor, insira o novo valor para {field_session['field']}:")

        elif callback_query.data[-3] == 'a':

            print(field_session['field'])
            if field_session['field'] == 'Nome':
                if callback_query.data[-1] == 'f':
                    print("Altera nome do full assessor")
                    await callback_query.message.reply_text(f"Por favor, insira o valor para edição ao campo {field_session['field']}:")
                    registra_user_states(
                        callback_query.message.chat.id, EDIT_NOME_A_F, "state")

                elif callback_query.data[-1] == 'p':
                    print("Altera nome do edit assessor")
                    await callback_query.message.reply_text(f"Por favor, insira o valor para edição ao campo {field_session['field']}:")
                    registra_user_states(
                        callback_query.message.chat.id, EDIT_NOME_A_P, "state")

            elif field_session['field'] == 'Cat_Nome_Titular':
                await callback_query.message.reply_text(f"🛑 O campo Titular não pode ser alterado 🛑")
                await callback_query.message.reply_text(f"Você deverá clicar em 'Remover' e posteriormente 'Cadastrar' com o nome do novo assessorado")
                await callback_query.message.reply_text(f"Em breve o senhor será notificado caso a edição seja aceita 👍")

            elif field_session['field'] == 'Telefone':
                if callback_query.data[-1] == 'f':
                    print("Altera o DDD")
                    await callback_query.message.reply_text(f"Iremos alterar primeiro o seu DDD")
                    await callback_query.message.reply_text(f"Digite os dois digitos do seu DDD sem o zero")
                    # TODO: Implementar edição de ddd e telefone
                    registra_user_states(
                        callback_query.message.chat.id, EDIT_DDD_A_F, "state")

                elif callback_query.data[-1] == 'p':
                    await callback_query.message.reply_text(f"Iremos alterar primeiro o seu DDD")
                    await callback_query.message.reply_text(f"Digite os dois digitos do seu DDD sem o zero")
                    # TODO: Implementar edição de ddd e telefone
                    registra_user_states(
                        callback_query.message.chat.id, EDIT_DDD_A_P, "state")

            else:
                print("Não é igual")
                await callback_query.message.reply_text(f"Por favor, insira o novo valor para {field_session['field']}:")

    elif "ftitular_edt" in callback_query.data:

        db.atualiza_dado_ass(callback_query.message.chat.id,
                             'titular_id', callback_query.data[0], 'f')
        await callback_query.message.reply_text(f"Edição realizada com sucesso!!")

    elif callback_query.data.startswith("remove_"):
        resp_ = callback_query.data.replace("remove_", "")
        if "no_" in resp_:
            await callback_query.message.reply_text(f"Operação Cancelada. Escolha uma das opções abaixo")

        if "yes_" in resp_:
            if callback_query.data[-1] == 'a':
                db.apaga_ass(callback_query.message.chat.id)
                await callback_query.message.reply(f"Usuário excluido com sucesso!!")
            elif callback_query.data[-1] == 't':
                db.apaga_titular(callback_query.message.chat.id)
                await callback_query.message.reply(f"Usuário excluido com sucesso!!")

    elif callback_query.data.startswith("sim_"):

        if callback_query.data[-1] == 'f':

            db.atualiza_dado_tit(
                callback_query.message.chat.id, 'only_assec', False, 'f')
            # registra_user_states(callback_query.message.chat.id,None,"state")
            await callback_query.message.reply(f"Alteração realizada com sucesso!!")

        elif callback_query.data[-1] == 'p':

            db.atualiza_dado_tit(
                callback_query.message.chat.id, 'only_assec', False, 'p')
            # registra_user_states(callback_query.message.chat.id,None,"state")
            await callback_query.message.reply(f"Alteração realizada com sucesso!!")
            ...
    elif callback_query.data.startswith("nao_"):

        if callback_query.data[-1] == 'f':

            db.atualiza_dado_tit(
                callback_query.message.chat.id, 'only_assec', True, 'f')
            # registra_user_states(callback_query.message.chat.id,None,"state")
            await callback_query.message.reply(f"Alteração realizada com sucesso!!")

        elif callback_query.data[-1] == 'p':
            db.atualiza_dado_tit(
                callback_query.message.chat.id, 'only_assec', True, 'p')
            # registra_user_states(callback_query.message.chat.id,None,"state")
            await callback_query.message.reply(f"Alteração realizada com sucesso!!")

    # TITULAR_PASSO_5
    elif "_ddd_" in callback_query.data:
        print(f"callback_query.data: {callback_query.data}")
        if callback_query.data[-1] == 't':

            if "Outro" in callback_query.data:
                await callback_query.message.reply_text(f"Por favor, digite os dois numeros de seu DDD sem as parênteses")
            else:
                registra_sess_data(callback_query.message.chat.id,
                                   callback_query.data[0:2], 'ddd_tit')
                await callback_query.message.reply_text("Por fim digite apenas os números do melhor telefone para que possamos entrar em contato com o senhor caso necessário")
                print(app.get_user_data(callback_query.message.chat.id))

        elif callback_query.data[-1] == 'a':

            if "Outro" in callback_query.data:
                await callback_query.message.reply_text("Senhor Assessor, digite os dois numeros de seu DDD sem as parênteses")
            else:
                registra_sess_data(callback_query.message.chat.id,
                                   callback_query.data[0:2], 'ddd_ass')
                await callback_query.message.reply_text("Para finalizar nos informe apenas os numeros do telefone que o senhor deseja cadastrar")

    elif callback_query.data.startswith("authtel"):

        if callback_query.data[-5] == "t":
            if callback_query.data[-3:] == 'sim':
                await callback_query.message.reply_text("Ótimo. Apenas contatos solicitados e extremamente necessários serão realizados")
                keyboard = generate_keyboard("t")
                await callback_query.message.reply_text("Selecione o seu DDD. Se não encontrar clique em 'outros'", reply_markup=keyboard)
                # Vai para TITULAR_PASSO_5

            elif callback_query.data[-3:] == 'nao':
                await callback_query.message.reply_text("Compreendemos perfeitamente sua decisão")
                obj_comp = app.get_user_data(callback_query.message.chat.id)
                # Grava os dados em Banco
                if existeuser(callback_query.message.chat.id, db)[0]:
                    await app.send_message(callback_query.message.chat.id, f'O sennhor já está cadastrado como {existeuser(callback_query.message.chat.id, db)[1]}')
                    await app.send_message(callback_query.message.chat.id, "Por favor selecione o botão 'Editar' logo abaixo, ou 'Ajuda' em caso de dúvidas")
                else:
                    db.inserir_dado_tit(nome_cat=converte_nome(obj_comp['nome_cat']), nome_tit=converte_nome(obj_comp['nome_tit']),
                                        id_t=obj_comp['id_t'], only_assec=obj_comp['only_assec'], ddd="", telfnumber="")
                    await app.send_message(callback_query.message.chat.id, f'Sua confirmação de cadastro será encaminhada em breve')

        elif callback_query.data[-5] == "a":
            if callback_query.data[-3:] == 'sim':
                await callback_query.message.reply_text("Certo Sr Assessor. Apenas contatos solicitados e extremamente necessários serão realizados")
                keyboard = generate_keyboard("a")
                await callback_query.message.reply_text("Selecione o seu DDD. Se não encontrar clique em 'outros'", reply_markup=keyboard)
                # Vai para TITULAR_PASSO_5

            elif callback_query.data[-3:] == 'nao':
                await callback_query.message.reply_text("Compreendemos perfeitamente sua decisão")
                await app.send_message(callback_query.message.chat.id, 'Sua confirmação de cadastro será encaminhada em breve')
                obj_comp = app.get_user_data(callback_query.message.chat.id)
                # Grava os dados em Banco
                if existeuser(callback_query.message.chat.id, db)[0]:
                    await app.send_message(callback_query.message.chat.id, f'O sennhor já está cadastrado como {existeuser(callback_query.message.chat.id, db)[1]}')
                    await app.send_message(callback_query.message.chat.id, "Por favor selecione o botão 'Editar' logo abaixo, ou 'Ajuda' em caso de dúvidas")
                else:
                    db.inserir_dado_ass(nome_cat=converte_nome(obj_comp['nome_cat']), nome_ass=converte_nome(obj_comp['nome_ass']), id_a=obj_comp['id_a'],
                                        nome_tit=converte_nome(obj_comp['nome_tit']), ddd="", telfnumber="")


@app.on_message()
async def messages(Client, message):
    # Obter o user_id do bot
    me = await app.get_me()
    bot_user_id = me.id
    # await message.reply("Processando solicitação...")
    # Verificar se a mensagem é enviada pelo próprio bot
    if message.from_user.id == bot_user_id:
        return  # Não faça nada se a mensagem for do próprio bot

    # Cria a variavel de sessão namedep
    registra_user_general(message.chat.id, (await app.get_messages(message.chat.id, message.id-2)).text, "namedep")
    registra_user_general(message.chat.id, (await app.get_messages(message.chat.id, message.id-1)).text, "namedep1")
    registra_user_general(message.chat.id, (await app.get_messages(message.chat.id, message.id)).text, "namedep2")
    registra_user_general(message.chat.id, app.get_user_states(
        message.chat.id), "stado")
    general_session = app.get_user_general(message.chat.id)
    print(f"general_session: {general_session}")
    # TITULAR_PASSO_2
    if general_session["namedep"] == 'Perfeito. Entendemos que o senhor é o titular':
        # Registra a categoria de titular que é
        registra_sess_data(
            message.chat.id, general_session['namedep2'], 'nome_cat')
        registra_sess_data(message.chat.id, message.chat.id, 'id_t')

        print(app.get_user_data(message.chat.id))

        await app.send_message(message.chat.id, f"Ótimo Sr(a) {general_session['namedep2']} 😀")
        await app.send_message(message.chat.id, f"Agora me informe o nome pelo qual o(a) senhor(a) gostaria de ser chamado(a).")
        # Vai para TITULAR_PASSO_3

    # Verifica se a expressão regular corresponde ao texto enviado
    elif re.match(pattern, general_session['namedep1']):
        match = re.match(pattern, general_session['namedep1'])
        update_field(message.chat.id, match.group(1),
                     general_session['namedep2'])
        print(
            f"O novo nome de {match.group(1)} será {general_session['namedep2']}")
    # ASSESSOR_PASSO_2
    elif general_session["namedep"] == 'Perfeito. Tudo ok senhor assessor':
        # Registra a categoria de titular que é
        registra_sess_data(
            message.chat.id, general_session['namedep2'], 'nome_ass')
        registra_sess_data(message.chat.id, message.chat.id, 'id_a')

        await app.send_message(message.chat.id, f"Ótimo senhor assessor {general_session['namedep2']}😀")
        await app.send_message(message.chat.id, f'Por gentileza nos informe a categoria do titular que o senhor assessora. Ex:. Deputado(a) Federal, Deputado(a) Estadual, Senador(a), Promotor(a), Juiz(a), etc.')
        # Vai para o ASSESSOR_PASSO_3

    # ASSESSOR_PASSO_4
    elif general_session["namedep"] == 'Estamos quase finalizando nosso cadastro...':
        user_data_f = app.get_user_data(message.chat.id)
        registra_sess_data(
            message.chat.id, general_session['namedep2'], 'nome_tit')
        await app.send_message(message.chat.id, f"Excelente senhor(a) assessor(a) {user_data_f['nome_ass']}😀")
        await app.send_message(message.chat.id, f"Para finalizar solicitamos que o senhor nos informe o melhor numero de telefone para contato")
        await app.send_message(message.chat.id, f"Não se preocupe por o numero será salvo de maneira criptografada")
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    f"Sim", callback_data="authtel_a_sim"),
                InlineKeyboardButton(
                    f"Não", callback_data="authtel_a_nao")
            ]
        ])

        await message.reply_text("Gostaria de fornecer seu telefone?", reply_markup=reply_markup)

    # ASSESSOR_PASSO_3
    elif general_session['namedep1'] == 'Por gentileza nos informe a categoria do titular que o senhor assessora. Ex:. Deputado(a) Federal, Deputado(a) Estadual, Senador(a), Promotor(a), Juiz(a), etc.':
        registra_sess_data(
            message.chat.id, general_session['namedep2'], 'nome_cat')
        await app.send_message(message.chat.id, f"Estamos quase finalizando nosso cadastro...")
        await app.send_message(message.chat.id, f"Agora me informe o nome do(a) {general_session['namedep2']} que o senhor assessora")
        # Vai para ASSESSOR_PASSO_4

    # TITULAR_PASSO_3
    elif general_session['namedep1'] == 'Agora me informe o nome pelo qual o(a) senhor(a) gostaria de ser chamado(a).':
        user_data_f = app.get_user_data(message.chat.id)
        registra_sess_data(
            message.chat.id, general_session['namedep2'], 'nome_tit')
        await app.send_message(message.chat.id, f"Estamos quase finalizando nosso cadastro Sr(a). {user_data_f['nome_cat']} {general_session['namedep2']}")
        await message.reply(f"Por favor. Nos informe se gostaria de receber mensagens de ocorrências de viaturas adquiridas com a fonte recursos direcionada pelo(a) senhor(a) ou apenas o assessor?")
        seassessor = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Quero receber tambem',
                                         callback_data='queretamb'),
                    InlineKeyboardButton('Apenas meu assessor',
                                         callback_data='apmeuacess'),
                ]
            ]
        )
        await message.reply('Selecione uma das opções abaixo...    ', reply_markup=seassessor)
        # Vai para TITULAR_PASSO_4

    #
    elif "Por favor, digite os dois numeros de seu DDD sem as parênteses" in general_session['namedep1'] or "Valor incorreto. Digite apenas os dois numeros do seu DDD" in general_session['namedep1']:
        registra_user_general(message.chat.id, limpaddd(
            general_session['namedep2']), "ddd")
        ddd_session = app.get_user_general(message.chat.id)

        if len(ddd_session['ddd']) > 2:
            await message.reply('Valor incorreto. Digite apenas os dois numeros do seu DDD')
            print("DDD: ", ddd_session['ddd'])
        else:
            registra_sess_data(message.chat.id, ddd_session['ddd'], 'ddd_tit')
            await app.send_message(message.chat.id, f"Por fim nos informe apenas os numeros do telefone que o senhor deseja cadastrar")

    elif "Por fim nos informe apenas os numeros do telefone" in general_session['namedep1'] or "Numero digitado fora do padrão. Um numero de telefone tem que ter 8 ou 9 dígitos" in general_session['namedep1']:
        registra_user_general(message.chat.id, limpaddd(
            general_session['namedep2']), "tel")
        tel_session = app.get_user_general(message.chat.id)

        if len(tel_session["tel"]) > 9 or len(tel_session["tel"]) < 8:
            await message.reply('Numero digitado fora do padrão. Um numero de telefone tem que ter 8 ou 9 dígitos')
            print("DDD: ", tel_session["tel"])
        else:
            registra_sess_data(message.chat.id, tel_session["tel"], 'tel_tit')
            # Vai para o TITULAR_PASSO_5
            await app.send_message(message.chat.id, f'Sua confirmação de cadastro será encaminhada em breve')
            obj_comp = app.get_user_data(message.chat.id)
            # Grava os dados em Banco
            if existeuser(message.chat.id, db)[0]:
                await app.send_message(message.chat.id, f'O sennhor já está cadastrado como {existeuser(message.chat.id, db)[1]}')
                await app.send_message(message.chat.id, "Por favor selecione o botão 'Editar' logo abaixo, ou 'Ajuda' em caso de dúvidas")
            else:
                db.inserir_dado_tit(nome_cat=converte_nome(obj_comp['nome_cat']), nome_tit=converte_nome(obj_comp['nome_tit']),
                                    id_t=obj_comp['id_t'], only_assec=obj_comp['only_assec'], ddd=obj_comp['ddd_tit'], telfnumber=obj_comp['tel_tit'])

    # Referente a titulares
    elif "Por fim digite apenas os números do melhor telefone" in general_session['namedep1'] or "Numero digitado fora do padrão. Um numero de telefone tem que ter 8 ou 9 dígitos" in general_session['namedep1']:
        registra_user_general(message.chat.id, limpaddd(
            general_session['namedep2']), "tel")
        tel_session = app.get_user_general(message.chat.id)

        if len(tel_session["tel"]) > 9 or len(tel_session["tel"]) < 8:
            await message.reply('Numero digitado fora do padrão. Um numero de telefone tem que ter 8 ou 9 dígitos')
            print("DDD: ", tel_session["tel"])
        else:
            registra_sess_data(message.chat.id, tel_session["tel"], 'tel_tit')
            # Vai para o TITULAR_PASSO_5
            await app.send_message(message.chat.id, f'Sua confirmação de cadastro será encaminhada em breve')
            obj_comp = app.get_user_data(message.chat.id)
            # Grava os dados em Banco
            if existeuser(message.chat.id, db)[0]:
                await app.send_message(message.chat.id, f'O sennhor já está cadastrado como {existeuser(message.chat.id, db)[1]}')
                await app.send_message(message.chat.id, "Por favor selecione o botão 'Editar' logo abaixo, ou 'Ajuda' em caso de dúvidas")
            else:
                db.inserir_dado_tit(nome_cat=converte_nome(obj_comp['nome_cat']), nome_tit=converte_nome(obj_comp['nome_tit']),
                                    id_t=obj_comp['id_t'], only_assec=obj_comp['only_assec'], ddd=obj_comp['ddd_tit'], telfnumber=obj_comp['tel_tit'])
    # Referente a Assessores
    elif "Para finalizar nos informe apenas os numeros do telefone que" in general_session['namedep1'] or "Numero digitado fora do padrão. Um numero de telefone tem que ter 8 ou 9 dígitos" in general_session['namedep1']:
        registra_user_general(message.chat.id, limpaddd(
            general_session['namedep2']), "tel")
        tel_session = app.get_user_general(message.chat.id)

        if len(tel_session["tel"]) > 9 or len(tel_session["tel"]) < 8:
            await message.reply('Numero digitado fora do padrão. Um numero de telefone tem que ter 8 ou 9 dígitos')
            print("numero: ", tel_session["tel"])
        else:
            registra_sess_data(message.chat.id, tel_session["tel"], 'tel_ass')
            obj_comp = app.get_user_data(message.chat.id)
            # Grava os dados em Banco
            if existeuser(message.chat.id, db)[0]:
                await app.send_message(message.chat.id, f'O sennhor já está cadastrado como {existeuser(message.chat.id, db)[1]}')
                await app.send_message(message.chat.id, "Por favor selecione o botão 'Editar' logo abaixo, ou 'Ajuda' em caso de dúvidas")
            else:
                db.inserir_dado_ass(nome_cat=converte_nome(obj_comp['nome_cat']), nome_ass=converte_nome(obj_comp['nome_ass']),
                                    id_a=obj_comp['id_a'], nome_tit=converte_nome(obj_comp['nome_tit']), ddd=obj_comp['ddd_ass'], telfnumber=obj_comp['tel_ass'])
                await app.send_message(message.chat.id, 'Sua confirmação de cadastro será encaminhada em breve')

    elif "Senhor Assessor, digite os dois numeros de seu DDD sem as parênteses" in general_session['namedep1'] or "Valor fora das regras. Digite apenas os dois numeros do seu DDD" in general_session['namedep1']:

        registra_user_general(message.chat.id, limpaddd(
            general_session['namedep2']), "ddd")
        ddd_session = app.get_user_general(message.chat.id)

        if len(ddd_session['ddd']) > 2:
            await message.reply('Valor fora das regras. Digite apenas os dois numeros do seu DDD')
            print("DDD: ", ddd_session['ddd'])
        else:
            registra_sess_data(message.chat.id, ddd_session['ddd'], 'ddd_ass')
            await app.send_message(message.chat.id, f"Para finalizar nos informe apenas os numeros do telefone que o senhor deseja cadastrar")

    elif general_session['stado'] and general_session['stado']['state'] != None:
        if general_session['stado']['state'].startswith('help'):
            # Pega a ultima mensagem e insere na variavel de sessão mensagem

            # Verifica se a mensagem tem mais de 800 caracteres
            if len(general_session['namedep2']) < 800:
                registra_user_help(message.chat.id,
                                   general_session['namedep2'], "mensagem")

                registra_user_states(message.chat.id, None, "state")
                # Grava todos os dados no banco
                objeto = app.get_user_help(message.chat.id)
                print(f"Objeto: {objeto}")

                db.inserir_dados_help(nome=converte_nome(objeto['nome']), id_user=message.chat.id, categoria=converte_nome(objeto['categoria']),
                                      telefone=objeto['telefone'], mensagem=objeto['mensagem'], tipo=objeto['tipo'])

                await app.send_message(message.chat.id, f"Sua solicitação foi encaminhada com sucesso 🎉!! Em breve entraremos em contato para juntos sanar-mos o problema 🤝")
            else:
                await app.send_message(message.chat.id, f"Desculpe, mas sua mensagem é muito grande. Por favor, tente novamente com uma mensagem menor")

        elif general_session['stado']['state'][-1] == 'p':

            if general_session['stado']['state'][-3] == 't':

                # Edição de titulares
                if general_session['stado']['state'] == EDIT_CATEGORIA_T_P:
                    db.atualiza_dado_tit(
                        message.chat.id, 'nome_cat', general_session['namedep2'], 'p')
                    registra_user_states(message.chat.id, None, "state")
                    await message.reply("Alteração realizada com sucesso!!")

                elif general_session['stado']['state'] == EDIT_NOME_T_P:
                    db.atualiza_dado_tit(
                        message.chat.id, 'nome_tit', general_session['namedep2'], 'p')
                    registra_user_states(message.chat.id, None, "state")
                    await message.reply("Alteração realizada com sucesso!!")

                elif general_session['stado']['state'] == EDIT_DDD_T_P or "Formato incorreto. Insira apenas" in general_session['namedep1']:

                    registra_user_general(
                        message.chat.id, limpaddd(general_session['namedep2']), "ddd")
                    ddd_session = app.get_user_general(message.chat.id)

                    if len(ddd_session['ddd']) > 2:
                        await message.reply('Formato incorreto. Insira apenas os dois numeros do seu DDD')
                        print("DDD: ", ddd_session['ddd'])
                    else:
                        if (ddd_session['ddd'].isnumeric()):

                            db.atualiza_dado_tit(
                                message.chat.id, 'ddd', general_session['namedep2'], 'p')
                            await message.reply("Perfeito. Para concluir a edição digite o numero de telefone que deverá ser substituir o campo informado")
                            registra_user_states(
                                message.chat.id, EDIT_TELEFONE_T_P, "state")
                        else:
                            await message.reply('Formato incorreto. Insira apenas os dois numeros do seu DDD')

                elif general_session['stado']['state'] == EDIT_TELEFONE_T_P or "Parece que você errou 😅" in general_session['namedep1']:
                    registra_user_general(
                        message.chat.id, limpaddd(general_session['namedep2']), "tel")
                    tel_session = app.get_user_general(message.chat.id)

                    if len(tel_session["tel"]) > 9 or len(tel_session["tel"]) < 8:
                        await message.reply('Parece que você errou 😅. O numero de telefone tem que ter 8 ou 9 dígitos')
                    else:
                        db.atualiza_dado_tit(
                            message.chat.id, 'telfnumber', general_session['namedep2'], 'p')
                        registra_user_states(message.chat.id, None, "state")
                        await message.reply("Alteração realizada com sucesso!!")

            # Edição de assessores
            elif general_session['stado']['state'][-3] == 'a':

                if general_session['stado']['state'] == EDIT_CATEGORIA_TITULAR_A_P:
                    db.atualiza_dado_ass(
                        message.chat.id, 'nome_cat', general_session['namedep2'], 'p')
                    registra_user_states(
                        message.chat.id, EDIT_NOME_TITULAR_A_P, "state")
                    await message.reply("Perfeito. Agora nos informe o nome do Titular que o senhor assessora")

                elif general_session['stado']['state'] == EDIT_NOME_TITULAR_A_P:
                    db.atualiza_dado_ass(
                        message.chat.id, 'nome_tit', general_session['namedep2'], 'p')
                    await message.reply("Alterações realizada com sucesso!!")

                elif general_session['stado']['state'] == EDIT_NOME_A_P:
                    db.atualiza_dado_ass(
                        message.chat.id, 'nome_ass', general_session['namedep2'], 'p')
                    # registra_user_states(message.chat.id,None ,"state")
                    await message.reply("Alterações realizada com sucesso!!")

                elif general_session['stado']['state'] == EDIT_DDD_A_P or "Tente novamente. Insira apenas" in general_session['namedep1']:

                    registra_user_general(
                        message.chat.id, limpaddd(general_session['namedep2']), "ddd")
                    ddd_session = app.get_user_general(message.chat.id)

                    if len(ddd_session['ddd']) != 2:
                        await message.reply('Tente novamente. Insira apenas os dois numeros do seu DDD')
                        print("DDD: ", ddd_session['ddd'])
                    else:
                        if (ddd_session['ddd'].isnumeric()):
                            db.atualiza_dado_ass(
                                message.chat.id, 'ddd', general_session['namedep2'], 'p')
                            await message.reply("Perfeito Sr assessor. Concluindo nossa edição digite o numero de telefone que deverá ser substituir o campo informado")
                            registra_user_states(
                                message.chat.id, EDIT_TELEFONE_A_P, "state")
                        else:
                            await message.reply('Tente novamente. Insira apenas os dois numeros do seu DDD')

                elif general_session['stado']['state'] == EDIT_TELEFONE_A_P or "Algo está incorreto !!" in general_session['namedep1']:
                    registra_user_general(
                        message.chat.id, limpaddd(general_session['namedep2']), "tel")
                    tel_session = app.get_user_general(message.chat.id)

                    if len(tel_session["tel"]) > 9 or len(tel_session["tel"]) < 8:
                        await message.reply('Algo está incorreto !!. O numero de telefone deve que ter 8 ou 9 dígitos')
                    else:
                        db.atualiza_dado_ass(
                            message.chat.id, 'telfnumber', general_session['namedep2'], 'p')
                        registra_user_states(message.chat.id, None, "state")
                        await message.reply("Alteração concluída com sucesso!!")

        elif general_session['stado']['state'][-1] == 'f':
            if general_session['stado']['state'][-3] == 't':

                if general_session['stado']['state'] == EDIT_NOME_T_F:
                    db.atualiza_dado_tit(
                        message.chat.id, 'nome', general_session['namedep2'], 'f')
                    registra_user_states(message.chat.id, None, "state")
                    await message.reply("Alteração realizada com sucesso!!")

                # Banco Full
                elif general_session['stado']['state'] == EDIT_DDD_T_F or "Algo incorreto. Insira apenas" in general_session['namedep1']:

                    registra_user_general(
                        message.chat.id, limpaddd(general_session['namedep2']), "ddd")
                    ddd_session = app.get_user_general(message.chat.id)

                    if len(ddd_session['ddd']) > 2:
                        await message.reply('Algo incorreto. Insira apenas os dois numeros do seu DDD')
                        print("DDD: ", ddd_session['ddd'])
                    else:
                        if (ddd_session['ddd'].isnumeric()):

                            db.atualiza_dado_tit(
                                message.chat.id, 'ddd', general_session['namedep2'], 'f')
                            await message.reply("Perfeito. Para concluir a edição digite o numero de telefone que deverá ser substituir o campo informado")
                            registra_user_states(
                                message.chat.id, EDIT_TELEFONE_T_F, "state")
                        else:
                            await message.reply('Algo incorreto. Insira apenas os dois numeros do seu DDD')

                elif general_session['stado']['state'] == EDIT_TELEFONE_T_F or "Me parece que se enganou 😅" in general_session['namedep1']:
                    registra_user_general(
                        message.chat.id, limpaddd(general_session['namedep2']), "tel")
                    tel_session = app.get_user_general(message.chat.id)

                    if len(tel_session["tel"]) > 9 or len(tel_session["tel"]) < 8:
                        await message.reply('Me parece que se enganou 😅. O numero de telefone tem que ter 8 ou 9 dígitos')
                    else:
                        db.atualiza_dado_tit(
                            message.chat.id, 'telfnumber', general_session['namedep2'], 'f')
                        registra_user_states(message.chat.id, None, "state")
                        await message.reply("Alteração realizada com sucesso!!")
            else:

                if general_session['stado']['state'] == EDIT_NOME_A_F:
                    db.atualiza_dado_ass(
                        message.chat.id, 'nome_assessor', general_session['namedep2'], 'f')
                    registra_user_states(message.chat.id, None, "state")
                    await message.reply("Alteração realizada com sucesso!!")
                # Banco Full
                elif general_session['stado']['state'] == EDIT_DDD_A_F or "Algo incorreto. Insira apenas" in general_session['namedep1']:

                    registra_user_general(
                        message.chat.id, limpaddd(general_session['namedep2']), "ddd")
                    ddd_session = app.get_user_general(message.chat.id)

                    if len(ddd_session['ddd']) > 2:
                        await message.reply('Algo incorreto. Insira apenas os dois numeros do seu DDD')
                        print("DDD: ", ddd_session['ddd'])
                    else:
                        if (ddd_session['ddd'].isnumeric()):

                            db.atualiza_dado_ass(
                                message.chat.id, 'ddd', general_session['namedep2'], 'f')
                            await message.reply("Perfeito. Para concluir a edição digite o numero de telefone que deverá ser substituir o campo informado")
                            registra_user_states(
                                message.chat.id, EDIT_TELEFONE_A_F, "state")
                        else:
                            await message.reply('Algo incorreto. Insira apenas os dois numeros do seu DDD')

                elif general_session['stado']['state'] == EDIT_TELEFONE_A_F or "Me parece que se enganou 😅" in general_session['namedep1']:
                    registra_user_general(
                        message.chat.id, limpaddd(general_session['namedep2']), "tel")
                    tel_session = app.get_user_general(message.chat.id)

                    if len(tel_session["tel"]) > 9 or len(tel_session["tel"]) < 8:
                        await message.reply('Me parece que se enganou 😅. O numero de telefone tem que ter 8 ou 9 dígitos')
                    else:
                        db.atualiza_dado_ass(
                            message.chat.id, 'telfnumber', general_session['namedep2'], 'f')
                        registra_user_states(message.chat.id, None, "state")
                        await message.reply("Alteração realizada com sucesso!!")

        else:
            print("Egeneral_session['stado'] tem coisa...")
            print(general_session['stado'])

    else:
        print(f"general_session['namedep1']: {general_session['namedep1']}")
        await message.reply(f"Desculpe não entendi sua solicitação")
        await message.reply(f"Escolha uma das opções do menu abaixo ou digite /start")
        try:
            registra_user_states(message.chat.id, None, "state")
        except:
            pass
        # Inserir um dado no banco


app.run()
