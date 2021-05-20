from __future__ import print_function
import telegram
import logging
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import time
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials





# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


# The ID and range of a sample spreadsheet.

def main():
    global service
    global rows
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API

    result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    print('{0} rows retrieved.'.format(len(rows)))
    print(rows)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
updater = Updater(token='1712370197:AAGxuYYL1YhqBzy6KlEIUchMFh2fgvpgUTw', use_context=True)
dispatcher = updater.dispatcher
def  checkid(update, context):
        id = update.message.text
        try:
            global spreadsheet_id
            spreadsheet_id = id.split(" ")[1]
            print(spreadsheet_id)
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Comando ambiguo, ID es incorrecto, o la sintaxis es incorrecta. Uso:  /id_<id_del_documento>, ejemplo: /id h2fgvpgUTw")
def  readsend(update, context):
    #try:
        #global srows
        main()
        print (rows)
        #rows = srows
        #srows = rows.split('"')[0]
        context.bot.send_message(chat_id=update.effective_chat.id, text=rows)
    #except:
    #    context.bot.send_message(chat_id=update.effective_chat.id, text='Error al ejecutar; ID incorrecto, se ha excedido el limite de solicitudes a la API de google, se ha configurado mal  la api de google o error desconocido. Para mas ayuda, visita: https://developers.google.com/sheets/api/quickstart/python y sigue los pasos de los prerequesitos apartir del punto 2.')
def  cell(update, context):
        global range_name
        range_name = update.message.text
        range_name = range_name.split(" ")[1]
        try:
            print(range_name)
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Comando ambiguo, ID es incorrecto, o la sintaxis es incorrecta. Uso:  /id_<id_del_documento>, ejemplo: /id h2fgvpgUTw")


def ayuda(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Indicamos el ID del documento mediante /ID. /celda para indicar donde trabajaremos. Insertar para escribir.")

def write(update, context):
    value_input_option = 'RAW'
    mensaje = update.message.text
    celda = mensaje.split(" ")[1]

    print(celda)
    values = [
            [
                    celda
            ],
                # Additional rows ...
            ]
    body = {
                'values': values
            }
    result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name,
    valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))




start_handler = CommandHandler('id', checkid)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('leer', readsend)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('celda', cell)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('ayuda', ayuda)
dispatcher.add_handler(start_handler)



start_handler = CommandHandler('insertar', write)
dispatcher.add_handler(start_handler)

dispatcher.add_handler(start_handler)
updater.start_polling()


