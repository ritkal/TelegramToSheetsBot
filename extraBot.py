from telethon import TelegramClient, sync, events

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)


spreadsheet_id = '1Ovtm-tYWbjWOtc791bdVRELTrJDmjQDCy_I0Ummo-ho'

api_id = 1018539
api_hash = '9576da03392f023e777ec252ffe58715'

CREDENTIALS_FILE = 'creds.json'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
# httpAuth = credentials.authorize(httplib2.Http())
# service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
google_client = gspread.authorize(credentials)
sh = google_client.open('SheetsTest')

client = TelegramClient('test_ses3', api_id, api_hash)

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

        # worksheet.update(row=next_row, sender.username)
        massageArrOfRows = (str(event.message.to_dict()['message']).split("\n"))
        for x in massageArrOfRows:
            # разбиваем сообщение, берем значения ключей
            if len(x) > 0 & (x.find(':') != -1):
                if x != '-----':
                    out = x.split(":")
                    if out[0] in TransDictionary:
                        prepearedData[TransDictionary[out[0]]] = out[1]

        for x in prepearedData:
            array.append(prepearedData[x])

        worksheet = sh.sheet1
        next_row = next_available_row(worksheet)
        cell_list = worksheet.range('A' + str(next_row) + ':J' + str(next_row))
        i = 0
        for cell in cell_list:
            cell.value = array[i]
            i = i + 1

        worksheet.update_cells(cell_list)

        worksheets = sh.worksheets()
        for item in worksheets:
            print(item.title.strip(), prepearedData['event'].strip(), item.title.strip() == prepearedData['event'].strip())
            if item.title.strip() == prepearedData['event'].strip():
                next_row = next_available_row(item)

                cell_list = item.range('A' + str(next_row) + ':J' + str(next_row))

                i = 0
                for cell in cell_list:
                    cell.value = array[i]
                    i = i + 1
                item.update_cells(cell_list)



client.start()
client.run_until_disconnected()
