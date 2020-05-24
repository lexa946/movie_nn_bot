from telebot import types
from Logic.message import Emoji
from Logic import SQL

class Markup(object):
    def __init__(self):
        self.__Keyboard = types.InlineKeyboardMarkup()
        self.__Buttons = []

    @property
    def keyboard(self):
        return self.__Keyboard


    def inline_markup(*args):
        """
        создает клавиатуру
        :param args: передаем кортэж кортэжей типа ((текст, значение),(текст, значение))
        :return: клавиатуру с заданными кнопками
        """
        keyboard = types.InlineKeyboardMarkup()
        for item in args:
            text, calldata = item
            callback_button = types.InlineKeyboardButton(text=text, callback_data=calldata)
            keyboard.add(callback_button)
        return keyboard

    def start(self):
        self.__Keyboard.add(types.InlineKeyboardButton(text='Кино на сегодня', callback_data='new'))

    def back(self):
        self.__Keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='cinema'))
        self.__Keyboard.add(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu'))

    def select(self):
        keys = ((Emoji.left, 'previous'),('Выбрать', 'more'), (Emoji.right, 'next'),)
        for item in keys:
            text, calldata = item
            self.__Buttons.append(types.InlineKeyboardButton(text=text, callback_data=calldata))
        self.__Keyboard.add(self.__Buttons[0], self.__Buttons[1], self.__Buttons[2])
        self.__Keyboard.add(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu'))

    def cinemas(self, length):
        need = length//3
        out_of_need = length%3
        index = 0
        for i in range(1,need+1):
            buttons = []
            for x in range(1,4):
                index += 1
                buttons.append(types.InlineKeyboardButton(text=index, callback_data=index))
            self.__Keyboard.add(buttons[0], buttons[1], buttons[2])
        if out_of_need == 1:
            self.__Keyboard.add(types.InlineKeyboardButton(text=length, callback_data=length))
        elif out_of_need == 2:
            self.__Keyboard.add(types.InlineKeyboardButton(text=length-1, callback_data=length-1),
                                types.InlineKeyboardButton(text=length, callback_data=length))
        self.__Keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='more'))
        self.__Keyboard.add(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu'))


    def more(self, trailer=None):
        self.__Keyboard.add(types.InlineKeyboardButton(text='К выбору кино', callback_data='now'))
        self.__Keyboard.add(types.InlineKeyboardButton(text='Трейлер', url=trailer))
        self.__Keyboard.add(types.InlineKeyboardButton(text='Где посмотреть', callback_data='cinema'))
        self.__Keyboard.add(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu'))

    def session(self):
        pass


    #Пользовательские клавиатуры

    # body_back = inline_markup(('Назад', 'more'), ('Главное меню', 'main_menu'))
    nothing = inline_markup(('Главное меню', 'main_menu'),)




    #Админские клавиатуры
    admin_start = inline_markup(('Кино на сегодня', 'new'), ('Admin', 'admin'))
    admin_main = inline_markup(('Обновить базу', 'refresh'),('Главное меню', 'main_menu'))
