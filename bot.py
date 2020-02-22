import telebot
import httplib2
import apiclient

from oauth2client.service_account import ServiceAccountCredentials
TOKEN = '<TOKEN>'
spreadsheet_id = '<spreadsheet_id>'

bot = telebot.TeleBot(TOKEN)
CREDENTIALS_FILE = 'creds.json'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_message(message.chat.id, 'Запись добавлена в таблицу Sheets')
    values = [
        [
            str(message.text)
        ],
        # Additional rows ...
    ]

    body = {
        "majorDimension": "ROWS",
        'values': values
    }
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range='A:A',
        valueInputOption='RAW', body=body).execute()


bot.polling()
