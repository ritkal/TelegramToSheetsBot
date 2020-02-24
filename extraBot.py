from telethon import TelegramClient, sync, events
import httplib2
import apiclient

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

TransDictionary = dict([('Name', 'name'), ('Name_2', 'name2'),
                        ('Email', 'mail'), ('Phone', 'phone'),
                        ('Ссылка_на_социальную_сеть', 'social'), ('Выберите_дату', 'data'),
                        ('Выберите_задачу', 'job'), ('Выберите_благодарность', 'thanks'),
                        ('Transaction ID', 'trans'), ('Block ID', 'event'),
                        ])



@client.on(events.NewMessage())
async def normal_handler(event):
    sender = await event.get_sender()
    array = []
    prepearedData = dict([('name', ''), ('name2', ''),
                          ('mail', ''), ('phone', ''),
                          ('social', ''), ('data', ''),
                          ('job', ''), ('thanks', ''),
                          ('trans', ''), ('event', ''),
                          ])
    if sender.username == 'TildaFormsBot':

        listSpread = (str(event.message.to_dict()['message']).split("\n"))
        for x in listSpread:
            # разбиваем сообщение, берем значения ключей
            if len(x) > 0 & (x.find(':') != -1):
                if x != '-----':
                    out = x.split(":")
                    if out[0] in TransDictionary:
                        prepearedData[TransDictionary[out[0]]] = out[1]

        for x in prepearedData:
            array.append(prepearedData[x])

        # array.pop()
        print(array)
        values = [
            array
            # Additional rows ...
        ]

        body = {
            "majorDimension": "ROWS",
            'values': values
        }
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range='A:K',
            valueInputOption='RAW', body=body).execute()


client.start()
client.run_until_disconnected()
