from bot import bot
from messages import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('GroupBot-c3226796520a.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Data").sheet1


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, HELLO_MESSAGE)


@bot.message_handler(content_types=["text"])  # Любой текст
def answer_message(message):
    result = sheet.get_all_records()
    send = False

    if len(message.text.split(' ')) > 1:
        bot.send_message(message.from_user.id, TWO_RMESSAGES)
        send = True
    else:
        for x in result:
            if message.text in x.get('Name').split(' '):
                send = True
                bot.send_message(message.from_user.id, 'Ось кого я знайшов:\n\n' + '<b>ПІБ</b>: ' + str(x.get('Name')) +
                                 '\n<b>Номер телефону</b>:' + '0' + str(x.get('Phone number')) +
                                 '\n<b>День народження</b>: ' + str(x.get('Birth date')) + '\n<b>Гуртожиток</b>: ' +
                                 str(x.get('Dorm №')), parse_mode='HTML')
    if send is False:
        bot.send_message(message.from_user.id, ERRORNAME, parse_mode='HTML')


if __name__ == '__main__':
     bot.polling(none_stop=True)
