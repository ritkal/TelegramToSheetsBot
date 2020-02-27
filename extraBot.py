from telethon import TelegramClient, sync, events
import httplib2
import apiclient
import os
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials

spreadsheet_id = '1Ovtm-tYWbjWOtc791bdVRELTrJDmjQDCy_I0Ummo-ho'
current = ''
api_id = 1018539
api_hash = '9576da03392f023e777ec252ffe58715'
exceptions = ['Request information:', 'Additional information:', 'https://ya-p.ru/publish (https://ya-p.ru/publish)', '-----']
CREDENTIALS_FILE = 'creds.json'
answer2 = '''
Требования_к_волонтёру: sdasd
sadsad:123
asdsad
asd
asd
'''
# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

client = TelegramClient('bot_session', api_id, api_hash)

di = dict([('rec162216335', 'hiddenPool1'), ('rec163725745', 'hiddenPool2'), ('rec163698462', 'hiddenPool3')])

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
    # values = [
    #     array
    #     # Additional rows ...
    # ]
    return {
        'majorDimension': 'ROWS',
        'values': [array]
    }


@client.on(events.NewMessage())
async def normal_handler(event):
    sender = await event.get_sender()
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
                                prepared_data['publish'][current] = prepared_data['publish'][current] + os.linesep + x
        pprint(prepared_data['publish'])
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
            update_sheet("hiddenPool", body)
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


# answer = '''Request information:
# Название_мероприятия: dsfsfdsd
# Название_организации: sadsadsd
# Адрес_места_проведения: МОСКВА
# Ближайшее_метро: sdsadasd
# Дата_начала: 29/02/2020
# Дата_окончания: 01/03/2020
# Время_начала: 12:32
# Время_окончания: 22:44
# Периодичность_мероприятия: 123213sdsd
# Описание_мероприятия: sdsdasd
# sdsdad
# sdasdsad
# Правила_поведения_на_мероприятии: sdasdasdsad
# Задачи: sadedwdw
# Требования_к_волонтёру: sdasd
# sadsad
# asdsad
# asd
# asd
# Необходимое_количество_волонтёров: 23
# Name: Никита Трикалинос
# Phone: +7 891 650 02 95
#
# Additional information:
# Transaction ID: 1891284:652630252
# Block ID: rec165396626
# Form Name: publish
# https://ya-p.ru/publish (https://ya-p.ru/publish)
# -----'''
#

# cur = ''
# array = []
# prepared_data = {
#     'base': dict([('name', ''), ('phone', ''),
#                   ('event', '')
#                   ]),
#     'volunteer': dict([('name2', ''),
#                        ('mail', ''),
#                        ('social', ''), ('date', ''),
#                        ('job', ''), ('thanks', '')
#                        ]),
#     'publish': dict([('eventName', ''), ('organizationName', ''),
#                      ('eventAddress', ''), ('nearestMetro', ''),
#                      ('startDate', ''), ('endDate', ''),
#                      ('startTime', ''), ('endTime', ''),
#                      ('eventPeriodicity', ''),
#                      ('eventDescription', ''),
#                      ('eventRules', ''), ('eventTasks', ''),
#                      ('eventRequirements', ''),
#                      ('volunteerAmount', ''),
#                      ('eventPhotos', '')
#                      ])
# }
#
# cur = ''
# exceptions = ['Request information:', 'Additional information:', 'https://ya-p.ru/publish (https://ya-p.ru/publish)', '-----']
#
# list_spread = answer2.split("\n")
# for x in list_spread:
#     # разбиваем сообщение, берем значения ключей
#     if len(x) > 0 & (x.find(':') != -1):
#         if x not in exceptions:
#             index = x.find(':')
#             out = ['', '']
#             out[0] = x[:index]
#             out[1] = x[index + 2:]
#             if out[0] in trans_dictionary['base']:
#                 prepared_data['base'][trans_dictionary['base'][out[0]]] = out[1].strip()
#             else:
#                 if out[0] in trans_dictionary['volunteer']:
#                     prepared_data['volunteer'][trans_dictionary['volunteer'][out[0]]] = out[1].strip()
#                 else:
#                     if out[0] in trans_dictionary['publish']:
#                         prepared_data['publish'][trans_dictionary['publish'][out[0]]] = out[1].strip()
#                         cur = trans_dictionary['publish'][out[0]]
#                     else:
#                         prepared_data['publish'][cur] = prepared_data['publish'][cur] + os.linesep + x
#     if cur:
#         if x.find(':') == -1:
#             if x != '-----':
#                 prepared_data['publish'][cur] = prepared_data['publish'][cur]+os.linesep+x
#

# pprint(prepared_data['publish'])
