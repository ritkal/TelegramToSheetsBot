from telethon import TelegramClient, sync, events
import httplib2
import apiclient
import os
from oauth2client.service_account import ServiceAccountCredentials

spreadsheet_id = '1Ovtm-tYWbjWOtc791bdVRELTrJDmjQDCy_I0Ummo-ho'
current = ''
api_id = 1018539
api_hash = '9576da03392f023e777ec252ffe58715'
exceptions = ['Request information:', 'Additional information:', 'https://ya-p.ru/publish (https://ya-p.ru/publish)',
              '-----', 'https://ya-p.ru/publish', 'Form Name: publish', 'https://ya-p.ru/']
CREDENTIALS_FILE = 'creds.json'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

client = TelegramClient('bot_session', api_id, api_hash)

di = dict([('rec162216335', 'pool1'), ('rec163698462', 'pool2'), ('rec166615195', 'pool3'),
           ('rec166624024', 'pool4'), ('rec166627915', 'pool5'), ('rec165502298', 'pool6'),
           ('rec166207181', 'pool7'), ('rec166503934', 'pool8')
           ])

trans_dictionary = {
    'base': dict([('Name', 'name'), ('Block ID', 'event'),
                  ('Phone', 'phone'),
                  ]),
    'volunteer': dict([('Name_2', 'name2'),
                       ('Email', 'mail'),
                       ('Ссылка_на_социальную_сеть', 'social'), ('Выберите_дату', 'date'),
                       ('Выберите_задачу', 'job'), ('Выберите_благодарность', 'thanks'),
                       ]),
    'publish': dict([('Название_мероприятия', 'eventName'), ('Название_организации', 'organizationName'),
                     ('Адрес_места_проведения', 'eventAddress'), ('Ближайшее_метро', 'nearestMetro'),
                     ('Дата_начала', 'startDate'), ('Дата_окончания', 'endDate'),
                     ('Время_начала', 'startTime'), ('Время_окончания', 'endTime'),
                     ('Периодичность_мероприятия', 'eventPeriodicity'),
                     ('Описание_мероприятия', 'eventDescription'),
                     ('Правила_поведения_на_мероприятии', 'eventRules'), ('Задачи', 'eventTasks'),
                     ('Требования_к_волонтёру', 'eventRequirements'),
                     ('Необходимое_количество_волонтёров', 'volunteerAmount'),
                     ('Фотографии_для_публикации', 'eventPhotos'),
                     ]),
}


def union2(dict1, dict2):
    return dict(list(dict1.items()) + list(dict2.items()))


def update_sheet(name, body):
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=name,
        valueInputOption='RAW', body=body).execute()


def generate_body(array):
    return {
        'majorDimension': 'ROWS',
        'values': [array]
    }


@client.on(events.NewMessage())
async def normal_handler(event):
    sender = await event.get_sender()
    current = ''
    array = []
    prepared_data = {
        'base': dict([('name', ''), ('phone', ''),
                      ('event', '')
                      ]),
        'volunteer': dict([('name2', ''),
                           ('mail', ''),
                           ('social', ''), ('date', ''),
                           ('job', ''), ('thanks', '')
                           ]),
        'publish': dict([('eventName', ''), ('organizationName', ''),
                         ('eventAddress', ''), ('nearestMetro', ''),
                         ('startDate', ''), ('endDate', ''),
                         ('startTime', ''), ('endTime', ''),
                         ('eventPeriodicity', ''),
                         ('eventDescription', ''),
                         ('eventRules', ''), ('eventTasks', ''),
                         ('eventRequirements', ''),
                         ('volunteerAmount', ''),
                         ('eventPhotos', '')
                         ])

    }
    if sender.username == 'TildaFormsBot':

        list_spread = (str(event.message.to_dict()['message']).split("\n"))
        for x in list_spread:
            # разбиваем сообщение, берем значения ключей
            if len(x) > 0 & (x.find(':') != -1):
                if x not in exceptions:
                    index = x.find(':')
                    out = ['', '']
                    out[0] = x[:index]
                    out[1] = x[index + 2:]
                    if out[0] != 'Transaction ID':
                        if out[0] in trans_dictionary['base']:
                            prepared_data['base'][trans_dictionary['base'][out[0]]] = out[1].strip()
                        else:
                            if out[0] in trans_dictionary['volunteer']:
                                prepared_data['volunteer'][trans_dictionary['volunteer'][out[0]]] = out[1].strip()
                            else:
                                if out[0] in trans_dictionary['publish']:
                                    prepared_data['publish'][trans_dictionary['publish'][out[0]]] = out[1].strip()
                                    current = trans_dictionary['publish'][out[0]]
                                else:
                                    if len(current) != 0:
                                        prepared_data['publish'][current] = prepared_data['publish'][
                                                                                current] + os.linesep + x
        if prepared_data['base']['event'] != 'rec165396626':
            data = union2(prepared_data['base'], prepared_data['volunteer'])
            data['event'] = di[data['event'].strip()]

            for x in data:
                array.append(data[x])

            # swap
            var = array[1]
            array[1] = array[3]
            array[3] = var

            body = generate_body(array)
            update_sheet("generalPool", body)
            update_sheet(data['event'], body)
        else:
            data = union2(prepared_data['base'], prepared_data['publish'])

            del data['event']

            for x in data:
                array.append(data[x])
            body = generate_body(array)
            update_sheet("publish", body)


client.start()
client.run_until_disconnected()
