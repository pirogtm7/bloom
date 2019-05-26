#import mysql.connector
#from closeststore import *
import telebot
from linkedlist import *

# подключение к бд
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Qwerty12345',
    db='flower',
    # charset='utf8mb4'
)

# изъятие данных из бд
connection = mydb
mycursor = connection.cursor(buffered=True)
name = "SELECT first_name FROM client"
mycursor.execute(name)
name1 = mycursor.fetchone()

surname = "SELECT last_name FROM client"
mycursor.execute(surname)
surname1 = mycursor.fetchone()

area = "SELECT area FROM client"
mycursor.execute(area)
area1 = mycursor.fetchone()

street = "SELECT street FROM client"
mycursor.execute(street)
street1 = mycursor.fetchone()

house = "SELECT house FROM client"
mycursor.execute(house)
house1 = mycursor.fetchone()

entrance = "SELECT entrance FROM client"
mycursor.execute(entrance)
entrance1 = mycursor.fetchone()

floor = "SELECT floor FROM client"
mycursor.execute(floor)
floor1 = mycursor.fetchone()

apartment = "SELECT apartment FROM client"
mycursor.execute(apartment)
apartment1 = mycursor.fetchone()

phone = "SELECT phone FROM client"
mycursor.execute(phone)
phone1 = mycursor.fetchone()

bouq = "SELECT idbouquet FROM client"
mycursor.execute(bouq)
bouq1 = mycursor.fetchone()

bill = "SELECT bill FROM client"
mycursor.execute(bill)
bill1 = mycursor.fetchone()


bot_token = '742172883:AAH3ti-vJY4yNX5NMlpeEkMAnRK27T-CSew'
bot = telebot.TeleBot(bot_token)


# первое инлайн сообщение, спрашивает у менеджера про подтверждение заказа
@bot.message_handler(commands=['start'])
def inline(message):
    key = telebot.types.InlineKeyboardMarkup()
    but_1 = telebot.types.InlineKeyboardButton(text='Подтвердить', callback_data='Подтвердить')
    but_2 = telebot.types.InlineKeyboardButton(text='Отменить', callback_data='Отменить')
    key.add(but_1, but_2)
    bot.send_message(message.chat.id, 'Новый заказ ' + str(bouq1) + '\nИмя клиента: ' + str(name1) + ' ' + str(surname1) + '\nАдрес: район ' + str(area1) + ', ул. ' + str(street1) + ", дом " + str(house1) + ", этаж " + str(floor1) + ", кв. " + str(apartment1) + '\nСчет: ' + str(bill1) + '\nСтатус: не подтвержден менеджером',
                     reply_markup=key)


# второе инлайн сообщение, предлагает курьерам взять заказ
def inline2(message):
    dj = str(dijkstra())
    key = telebot.types.InlineKeyboardMarkup()
    but_3 = telebot.types.InlineKeyboardButton(text='Взять', callback_data='Взять')
    key.add(but_3)
    bot.send_message(message.chat.id, 'Заказ ' + str(bouq1) + '\nИмя клиента: ' + str(name1) + ' ' + str(surname1) + '\nАдрес: район ' + str(area1) + ', ул. ' + str(street1) + ", дом " + str(house1) + ", этаж " + str(floor1) + ", кв. " + str(apartment1) + '\nСчет: ' + str(bill1) + '\nСтатус: подтвержден менеджером' + '\nБлижайшие магазины: ' + dj,
                     reply_markup=key)


# третье инлайн сообщение, предлагает курьеру отказаться от заказа
def inline3(message):
    key = telebot.types.InlineKeyboardMarkup()
    but_3 = telebot.types.InlineKeyboardButton(text='Отказаться', callback_data='Отказаться')
    key.add(but_3)
    send = bot.send_message(message.chat.id, 'Заказ ' + str(bouq1) + '\nСтатус: передан курьеру ...', reply_markup=key)
    bot.register_next_step_handler(send, inline2)


# коллбек, указывает боту, что отправлять в ответ на выбор пользователя, отправляет пользователю сообщение в лс
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "Подтвердить":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            inline2(call.message)
            bot.send_message(call.from_user.id,
                             'Вы подтвердили заказ: ' + str(bouq1) + '\nИмя клиента: ' + str(name1) + ' ' + str(surname1) + '\nАдрес: район ' + str(area1) + ', ул. ' + str(street1) + ", дом " + str(house1) + ", подъезд " + str(entrance1) + ", этаж " + str(floor1) + ", кв. " + str(apartment1) + '\nТелефон: ' + str(phone1) + '\nСчет: ' + str(bill1))
        if call.data == "Отменить":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Заказ ' + str(bouq1) + ' отменен менеджером')
            bot.send_message(call.from_user.id, 'Вы отменили заказ ' + str(bouq1))
        if call.data == "Взять":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            inline3(call.message)
            bot.send_message(call.from_user.id,
                             'Вы взяли заказ: ' + str(bouq1) + '\nИмя клиента: ' + str(name1) + ' ' + str(surname1) + '\nАдрес: район ' + str(area1) + ', ул. ' + str(street1) + ", дом " + str(house1) + ", подъезд " + str(entrance1) + ", этаж " + str(floor1) + ", кв. " + str(apartment1) + '\nТелефон: ' + str(phone1) + '\nСчет: ' + str(bill1))
        if call.data == "Отказаться":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            inline2(call.message)
            bot.send_message(call.from_user.id, 'Вы отказались от заказа ' + str(bouq1))


print(L)

bot.polling(none_stop=True, interval=0, timeout=60)
