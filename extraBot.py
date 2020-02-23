from telethon import TelegramClient, sync, events
import httplib2
import apiclient
import socks

from oauth2client.service_account import ServiceAccountCredentials
spreadsheet_id = '1Ovtm-tYWbjWOtc791bdVRELTrJDmjQDCy_I0Ummo-ho'


api_id = 1018539
api_hash = '9576da03392f023e777ec252ffe58715'

CREDENTIALS_FILE = 'creds.json'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


client = TelegramClient('test_ses', api_id, api_hash)


@client.on(events.NewMessage())
async def normal_handler(event):
#    print(event.message)
    listSpread = (str(event.message.to_dict()['message']).split("\n"))
    values = [
        [
            str(str(event.message.to_dict()['message']))
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
    print(listSpread)


client.start()
client.run_until_disconnected()

