from . import SQL


class Emoji:
    lol = u'\U0001F602'
    default = u'\U0001F601'
    podmig = u'\U0001F609'
    uhmilka = u'\U0001F60F'
    roket = u'\U0001F680'
    down = u'\U000023EC'
    save = u'\U0001F4BE'
    like = u'\U0001F44D'
    reload_ = u'\U0001F504'
    clock = u'\U0001F55C'
    face_cold = u'\U0001F613'
    finger_down = u'\U0001F447'
    check = u'\U00002611'
    right = u'\U000027A1'
    left = u'\U00002B05'


class Message(object):
    def __init__(self, id_):
        data = SQL.get_from_base(id_=id_)[0]
        self.__Title = data[0]
        self.__Image = data[1]
        self.__Rating = data[2]
        self.__Slogan = data[3]
        self.__Url = data[4]
        self.__Trailer = data[5]
        self.__Description = data[6]
        self.__Cinemas = data[7].split(',')[:-1]
        self.__Sessions = data[8].split(';')[:-1]
        self.__Text = "Сегодня ничего в прокате нету!"


    def __str__(self):
        return self.__Text

    @property
    def text(self):
        return self.__Text

    @property
    def image(self):
        return self.__Image

    @property
    def trailer(self):
        return self.__Trailer

    @property
    def total_cinemas(self):
        return len(self.__Cinemas)

    def menu(self, username):
        self.__Text = f'Привет, {username}\n' \
                      f'Давай посмотрим какие премьеры у нас сегодня {Emoji.check}\n' \
                      f'{Emoji.finger_down}{Emoji.finger_down}{Emoji.finger_down}'

    def main_(self):
        self.__Text = f'<b>{self.__Title}</b>\n\n'
        if self.__Rating:
            self.__Text += f'Кинопоиск: {self.__Rating}\n\n'
        if self.__Slogan:
            self.__Text += f'<i>{self.__Slogan}</i>'

    def more(self):
        length_desc = len(self.__Description)
        length_title = len(self.__Title)
        length_common = length_desc + length_title
        # print(length)
        if length_common > 1024:
            self.__Description = self.__Description[:1020-length_title] + "..."
            print(self.__Description)
        self.__Text = f'<b>{self.__Title}</b>\n<i>{self.__Description}</i>'

    def cinemas(self):
        self.__Text = f'<b>{self.__Title}</b>\n'
        if self.__Cinemas != '-':
            self.__Text += 'Посмотреть можно в:\n\n'
            for _ in range(len(self.__Cinemas)):
                self.__Text += f'{_ + 1}. {self.__Cinemas[_]}\n'# - {self.__Sessions[_]} \n\n'
        else:
            self.__Text += 'К сожалени сегодня нигде не показывают'
        self.__Text += '\nВы можете выбрать кинотеатр и посмотреть сеансы.'

    def session(self, cinema):
        self.__Text = f'<b>{self.__Title}</b>\n'
        self.__Text += f'Сеансы в {self.__Cinemas[cinema]}:\n'
        sessions = self.__Sessions[cinema].split(',')
        for session in sessions:
            self.__Text += f'{session}\t'

if __name__ == '__main__':
    pass
    test_msg = Message(1)
    test_msg.main_()

    print(test_msg)