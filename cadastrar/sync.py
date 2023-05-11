import json
import os

import google.auth
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.crypto import encrypt_number

from .models import Categorias, Titular, Viatura

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


def get_last_row_index(service, spreadsheet_id):
    range_name = "Placas!C:C"
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    last_row_index = len(values)
    while last_row_index > 0 and not values[last_row_index - 1]:
        last_row_index -= 1

    return last_row_index


def syncronize_database():
    # Carregue as credenciais do Google Sheets a partir da variável de ambiente

    credentials_json = json.loads(os.getenv('GOOGLE_CREDENTIALS'))

    # Configure as credenciais e o escopo
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = service_account.Credentials.from_service_account_info(
        credentials_json, scopes=scopes)

    # Crie uma instância da API Google Sheets
    service = build('sheets', 'v4', credentials=credentials)

    # O ID da planilha e o intervalo que deseja ler (por exemplo, 'A1:E10' para ler as células A1 até E10 da primeira aba)
    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    # Obtenha o índice da última linha não vazia da coluna C
    last_row_index = get_last_row_index(service, spreadsheet_id)

    # Defina o intervalo para ler com base no índice da última linha
    range_name = f'Placas!C2:G{last_row_index}'

    contador = 0

    print(range_name)
    # Leia os dados da planilha
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        for i in range(0, len(rows)):
            if (rows[i][0] == ''):
                break
            rows[i][0] = format_name(rows[i][0])
        for row in rows:
            if row[0] == '':
                break
            # Logica para inserir no banco de dados
            # passo 1: verificar se a placa já existe no banco de dados
            viatura = Viatura.objects.filter(placa=row[3]).first()
            if viatura:
                continue
            # passo 2: verificar se o titular já está cadastrado. Se não estiver, cadastrar
            titular = Titular.objects.filter(nome=row[0]).first()
            if not titular:
                categorias = Categorias.objects.filter(nome=row[4]).first()
                if not categorias:
                    categorias = Categorias.objects.create(nome=row[4])
                cat_id = categorias.id
                titular = Titular.objects.create(
                    nome=row[0], id_chat_d='', only_assec=True, categoria_id=cat_id, ddd='', telfnumber='')

            # passo 2: verificar se a viatura já está cadastrada.
            viatura = Viatura.objects.create(
                tipo=row[2], placa=row[3], titular_id=titular.id)

            contador += 1
            print(row)
        return contador

    except HttpError as error:
        print(f"Ocorreu um erro: {error}")
        return -1


if __name__ == '__main__':
    syncronize_database()
