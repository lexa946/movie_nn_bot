import config
import socks, socket
from Logic import User, Message, Emoji, start, SQL, Markup
from telebot import TeleBot, apihelper, types
import requests

bot = TeleBot(config.TOKEN)



def delete_message(func):
    def wrapper(call):
        try:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=f"Подождите {Emoji.reload_}")
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except (requests.exceptions.SSLError, apihelper.ApiException):
            pass
        func(call)
    return wrapper


@bot.message_handler(func=lambda message: True, commands=['test'])
def test(message):
    keyboard = Markup()
    # keyboard.test()
    bot.send_message(message.chat.id, 'test', reply_markup=keyboard.keyboard)


@bot.message_handler(func=lambda message: True, commands=['start'])
def start(message):
    is_exist = start(message.chat.id)
    msg = Message(1)
    msg.menu(message.chat.username)
    keyboard = Markup()
    keyboard.start()
    if is_exist:
        pass
    else:
        bot.send_message(message.chat.id, 'Добро пожаловать')
        bot.send_message(message.chat.id, msg.text, reply_markup=keyboard.keyboard)


@bot.message_handler(commands=['help'])
def start(message):
    msg = Message(1)
    msg.menu(message.chat.username)
    keyboard = Markup()
    keyboard.start()
    bot.send_message(message.chat.id, msg.text, reply_markup=keyboard.keyboard)


# ------ОБРАБОТКА КНОПОК -----------------------------

@bot.callback_query_handler(func=lambda call: call.data == 'new')
@delete_message
def call_body_new(call):
    id_ = call.message.chat.id
    user = User(id_)
    user.state_movie = 1
    msg = Message(1)
    msg.main_()
    keyboard = Markup()
    keyboard.select()
    bot.send_photo(user.id_, msg.image, msg.text, parse_mode='HTML',
                   reply_markup=keyboard.keyboard)


# TODO: Сделать декоратор для отправки собщения

@bot.callback_query_handler(func=lambda call: call.data in ('next', 'previous', 'now'))
def call_body_next(call):
    id_ = call.message.chat.id
    msg_id = call.message.json['message_id']
    user = User(id_)
    # --------------------------------------
    if call.data == 'next':
        user.next_movie()
    elif call.data == 'previous':
        user.previous_movie()
    elif call.data == 'now':
        pass
    else:
        assert "Этого не должно произойти, но может.\n Обрабатываем кнопку Далее и Назад"
    # --------------------------------------
    msg = Message(user.state_movie)
    msg.main_()
    keyboard = Markup()
    keyboard.select()
    bot.edit_message_media(chat_id=id_, message_id=msg_id,
                           media=types.InputMediaPhoto(msg.image, caption=msg.text, parse_mode='HTML'),
                           reply_markup=keyboard.keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'more')
def call_body_more(call):
    id_ = call.message.chat.id
    msg_id = call.message.json['message_id']
    user = User(id_)
    msg = Message(user.state_movie)
    msg.more()
    keyboard = Markup()
    keyboard.more(msg.trailer)
    bot.edit_message_media(chat_id=id_, message_id=msg_id,
                           media=types.InputMediaPhoto(msg.image, caption=msg.text, parse_mode='HTML'),
                           reply_markup=keyboard.keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'cinema')
def call_body_cinema(call):
    id_ = call.message.chat.id
    msg_id = call.message.json['message_id']
    user = User(id_)
    msg = Message(user.state_movie)
    msg.cinemas()
    keyboard = Markup()
    keyboard.cinemas(msg.total_cinemas)
    bot.edit_message_media(chat_id=id_, message_id=msg_id,
                           media=types.InputMediaPhoto(msg.image, caption=msg.text, parse_mode='HTML'),
                           reply_markup=keyboard.keyboard)

@bot.callback_query_handler(func=lambda call: call.data in [str(i) for i in range(1,21)])
def call_session(call):
    id_ = call.message.chat.id
    msg_id = call.message.json['message_id']
    user = User(id_)
    msg = Message(user.state_movie)
    msg.session(int(call.data)-1)
    keyboard = Markup()
    keyboard.back()
    bot.edit_message_media(chat_id=id_, message_id=msg_id,
                           media=types.InputMediaPhoto(msg.image, caption=msg.text, parse_mode='HTML'),
                           reply_markup=keyboard.keyboard)



#TODO доделать клавиатуру с сеансами

@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
@delete_message
def call_main_menu(call):
    msg = Message(1)
    msg.menu(call.message.chat.username)
    keyboard = Markup()
    keyboard.start()
    bot.send_message(call.message.chat.id, msg.text, reply_markup=keyboard.keyboard)


if __name__ == '__main__':
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket = socks.socksocket
    print('Стартанул')
    # bot.remove_webhook()
    bot.infinity_polling(timeout=5000)
