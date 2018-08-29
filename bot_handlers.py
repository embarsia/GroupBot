
from bot import bot
from messages import HELLO_MESSAGE
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
        bot.send_message(message.from_user.id, "Будь-ласка, введи лише им'я або прізвище")
        send = True
    else:
        for x in result:
            if message.text in x.get('Name').split(' '):
                send = True
                bot.send_message(message.from_user.id,
                                 'Я знайшов ось кого:\n\n' + '<b>ПІБ</b>: ' + str(x.get('Name')) +
                                 '\n<b>Посилання на Телеграм: </b>' + str(x.get('TG Username')) + '\n<b>e-mail</b>: ' +
                                 str(x.get('E-mail')) + '\n<b>Номер телефону</b>: ' + '0' + str(x.get('Phone number')) +
                                 '\n<b>День народження</b>: ' + str(x.get('Birth date')) + '\n<b>Гуртожиток</b>: ' +
                                 str(x.get('Dorm №')), parse_mode='HTML')
    if send is False:
        bot.send_message(message.from_user.id, "Нажаль в списку немає такої людини.\nТи впевнений, що все вірно ввів? "
                                               "<b>Українською</b> мовою та з <b>великої</b> літери?)",
                         parse_mode='HTML')


@bot.message_handler(content_types=["text"])  # Любой текст
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
     bot.polling(none_stop=True)
