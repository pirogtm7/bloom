import telebot
import dbconnector as conn
from client2 import Client2
client_dict = {}

TOKEN = "831438027:AAFON5uOLiPcGq7bmS_gxbvYa983AToYcSw"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(regexp='Начать сначала')
def send_welcome(message):
    print(message.chat.id)
    markup_menu = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_menu.row("Начать сначала")
    markup_menu.row("Готовый букет")
    bot.send_message(message.from_user.id, 'Привет! Готовы принять Ваш заказ :)', reply_markup=markup_menu )
    #bot.forward_message(627340612,message.chat.id, message.message_id)


def show_keyboard_low_price(call,counter,list_of_flowers):
    keyboard = telebot.types.InlineKeyboardMarkup(True)
    callback_button = telebot.types.InlineKeyboardButton(text = "<<НАЗАД", callback_data="previous"+ str(counter-1))
    callback_button2 = telebot.types.InlineKeyboardButton(text = "ВПЕРЕД>>", callback_data="next" + str(counter+1))
    callback_button3 = telebot.types.InlineKeyboardButton(text="ДОБАВИТЬ В КОРЗИНУ", callback_data="add_low"+str(counter+1))
    keyboard.add(callback_button,callback_button2,callback_button3)
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=telebot.types.InputMediaPhoto(conn.get_url_image(str(list_of_flowers[counter+1]))),reply_markup=keyboard)
    bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.message_id,caption=str(conn.get_price(str(list_of_flowers[counter+1])))
    + "\n" + conn.get_description(str(list_of_flowers[counter+1])),reply_markup=keyboard)


def show_keyboard_high_price(call,counter):
     high_price = conn.get_flower_high_price()
     keyboard = telebot.types.InlineKeyboardMarkup(True)
     callback_button = telebot.types.InlineKeyboardButton(text = "<<НАЗАД", callback_data="previous_high"+ str(counter-1))
     callback_button2 = telebot.types.InlineKeyboardButton(text = "ВПЕРЕД>>", callback_data="next_high" + str(counter+1))
     callback_button3 = telebot.types.InlineKeyboardButton(text="ДОБАВИТЬ В КОРЗИНУ", callback_data="add_high"+str(counter+1))
     keyboard.add(callback_button,callback_button2,callback_button3)
     bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=telebot.types.InputMediaPhoto(conn.get_url_image(str(high_price[counter+1]))),reply_markup=keyboard)
     bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.message_id,caption=str(conn.get_price(str(high_price[counter+1])))
     + "\n" + conn.get_description(str(high_price[counter+1])),reply_markup=keyboard)


def order_finish(call):
     reply_key = telebot.types.ReplyKeyboardMarkup(True,True)
     reply_key.row("Оформить заказ")
     bot.send_message(chat_id=call.message.chat.id,text="Вы желаете оформить заказ?",reply_markup=reply_key)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Готовый букет":
        mark_upmenu2 = telebot.types.ReplyKeyboardMarkup(True,True)
        mark_upmenu2.row("500-1000 грн","1000-2000 грн","Начать сначала")
        bot.send_message(message.from_user.id, 'Пожалуйста, выберите ценовой диапазон',reply_markup=mark_upmenu2)
    if message.text == "500-1000 грн":
       keyboard = telebot.types.InlineKeyboardMarkup(True)
       callback_button = telebot.types.InlineKeyboardButton(text = "<<НАЗАД", callback_data="previous")
       callback_button2 = telebot.types.InlineKeyboardButton(text = "ВПЕРЕД>>", callback_data="next0")
       callback_button3 = telebot.types.InlineKeyboardButton(text="ДОБАВИТЬ В КОРЗИНУ", callback_data="add_high"+str(0))
       keyboard.add(callback_button,callback_button2,callback_button3)
       bot.send_chat_action(message.from_user.id, 'upload_photo')
       low_price = conn.get_flower_low_price()
       bot.send_photo(chat_id=message.from_user.id, photo=conn.get_url_image(str(low_price[0])),caption=str(conn.get_price(str(low_price[0])))+
                                                                                                        "\n" + conn.get_description(str(low_price[0])),reply_markup=keyboard)

    if message.text == "1000-2000 грн":
       keyboard = telebot.types.InlineKeyboardMarkup(True)
       callback_button = telebot.types.InlineKeyboardButton(text = "<<НАЗАД", callback_data="previous_high")
       callback_button2 = telebot.types.InlineKeyboardButton(text = "ВПЕРЕД>>", callback_data="next_high0")
       callback_button3 = telebot.types.InlineKeyboardButton(text="ДОБАВИТЬ В КОРЗИНУ", callback_data="add_high"+str(0))
       keyboard.add(callback_button,callback_button2,callback_button3)
       bot.send_chat_action(message.from_user.id, 'upload_photo')
       high_price = conn.get_flower_high_price()
       bot.send_photo(chat_id=message.from_user.id, photo=conn.get_url_image(str(high_price[0])),caption=str(conn.get_price(str(high_price[0])))+ "\n" + conn.get_description(str(high_price[0])),reply_markup=keyboard)
    if message.text == "Оформить заказ":
     newmessage = bot.reply_to(message, 'Ваше имя:')
     bot.register_next_step_handler(newmessage, process_name_step)
    if message.text == "Подтвердить":
       bot.send_message(message.from_user.id, 'Ваш заказ принят.\n Ожидайте звонок менеджера')


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        client = Client2(name)
        client_dict[chat_id] = client
        newmessage = bot.reply_to(message, "Ваша фамилия:")
        bot.register_next_step_handler(newmessage, process_last_name_step)
        client.client_id = message.from_user.id
    except Exception as e:
        bot.reply_to(message, "Попробуйте ещё раз")


def process_last_name_step(message):
    try:
        chat_id = message.chat.id
        lastname = message.text
        client = client_dict[chat_id]
        client.lastname = lastname
        newmessage = bot.reply_to(message,"Введите район:")
        bot.register_next_step_handler(newmessage,process_area_step)
    except Exception as e:
        bot.reply_to(message, "Попробуйте ещё раз")


def process_area_step(message):
    try:
        chat_id = message.chat.id
        area = message.text
        client = client_dict[chat_id]
        client.area = area
        newmessage = bot.reply_to(message, "Введите улицу:")
        bot.register_next_step_handler(newmessage, process_street_step)
    except Exception as e:
        bot.reply_to(message, "Попробуйте ещё раз")


def process_street_step(message):
    try:
        chat_id = message.chat.id
        street = message.text
        client = client_dict[chat_id]
        client.street = street
        newmessage = bot.reply_to(message, "Введите номер дома:")
        bot.register_next_step_handler(newmessage, process_entrance_step)
    except Exception as e:
        bot.reply_to(message, "Попробуйте ещё раз")


def process_entrance_step(message):
    try:
        chat_id = message.chat.id
        entrance = message.text
        client = client_dict[chat_id]
        client.entrance = entrance
        newmessage = bot.reply_to(message, "Введите номер квартиры:")
        bot.register_next_step_handler(newmessage, process_apartment_step)
    except Exception as e:
        bot.reply_to(message, "Попробуйте ещё раз")


def process_apartment_step(message):
    try:
        chat_id = message.chat.id
        apartment = message.text
        client = client_dict[chat_id]
        client.apartment = apartment
        newmessage = bot.reply_to(message,"Введите этаж")
        bot.register_next_step_handler(newmessage,process_floor_step)
    except Exception as e:
        bot.reply_to(message, "Попробуйте ещё раз")


list_price = []


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

     low_price = conn.get_flower_low_price()
     if call.data == "next" + str(len(low_price)):
        bot.send_message(chat_id=call.message.chat.id,text="Больше букетов нет")
     if call.data == "previous" + str(-2):
        bot.send_message(chat_id=call.message.chat.id,text="Больше букетов нет")
     if call.data == "add_low" + str(0):
        list_price.append(conn.get_price(str(low_price[0])))
        order_finish(call)
     for i in range(len(low_price)+1):
      if i < len(low_price)-1 and call.data == "next" + str(i):
          show_keyboard_low_price(call, i, low_price)

      counter = i-1
      if counter > -2 and call.data == "previous" + str(counter):
        show_keyboard_low_price(call, i-1, low_price)

      if call.data == "add_low" + str(i-1):
        list_price.append(conn.get_price(str(low_price[i-1])))
        print(list_price)
        order_finish(call)

     high_price = conn.get_flower_high_price()
     if call.data == "next_high" + str(len(low_price)):
       bot.send_message(chat_id=call.message.chat.id,text="Больше букетов нет")
     if call.data == "previous_high" + str(-2):
         bot.send_message(chat_id=call.message.chat.id,text="Больше букетов нет")
     if call.data == "add_high"+ str(0):
         list_price.append(conn.get_price(str(low_price[0])))
         order_finish(call)
     for m in range(len(high_price)):
      if m< len(high_price)-1 and call.data == "next_high"+str(m):
       show_keyboard_high_price(call,m)
      counter2 = m-1

      if counter2 > -2 and call.data == "previous_high" + str(counter2):
          show_keyboard_high_price(call,m-1)

      if call.data == "add_high"+ str(m):
         list_price.append(conn.get_price(str(low_price[m-1])))
         print(list_price)
         order_finish(call)
         #bot.send_message(chat_id=call.message.chat.id, text=len(count_oreder(conn.get_price(high_price[m]))))


def process_floor_step(message):
    try:
        chat_id = message.chat.id
        floor = message.text
        client = client_dict[chat_id]
        client.floor = floor
        replykey= telebot.types.ReplyKeyboardMarkup(True,True)
        replykey.row("Подтвердить")
        replykey.row("Начать сначала")
        newmessage = bot.send_message(chat_id, "Ваш заказ: \n Имя: " + client.name + "\nФамилия: " + client.lastname + "\n Район: " + client.area + "\n Улица: " + client.street + "\n Номер дома: " + client.entrance +  "\n Номер квартиры: "
                         + client.apartment + "\n Этаж: " + client.floor + "\n Статус заказа: ", reply_markup=replykey)
        conn.connect(conn, client.client_id, client.name, client.lastname, client.area, client.street, client.entrance, client.apartment, client.floor)
        #conn.connect(conn, 1314214,"adad","sdad","asdasd","700")
    except Exception as e:
        bot.reply_to(message, "Вы готовы подтвердить?")


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling(timeout=60)

