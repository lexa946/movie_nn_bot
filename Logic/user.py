from Logic import SQL


def refresh_state(field_name='kino'):
    def refreshing_state(method):
        def refresher_state(self, value=None):
            if value:
                method(self, value)
            else:
                method(self)
            state = ''
            if field_name == 'kino':
                state = getattr(self, 'state_movie')
            elif field_name == 'user':
                state = getattr(self, 'state_menu')
            SQL.set_state(mode=field_name, id=self.id_, state=state)
        return refresher_state
    return refreshing_state


refresh_movie = refresh_state('kino')
refresh_menu = refresh_state('user')


class User(object):
    __Max_movie = SQL.execute_sql('SELECT COUNT(1) FROM kino')[0][0]

    def __init__(self, id_):
        self.__Id = id_
        states = SQL.get_state(id=self.id_)
        self.__State_movie = states[1]
        self.__State_menu = states[0]

    @property
    def id_(self):
        return self.__Id

    @property
    def state_movie(self):
        return self.__State_movie

    @state_movie.setter
    @refresh_movie
    def state_movie(self, value):
        self.__State_movie = value

    @property
    def state_menu(self):
        return self.__State_menu

    @state_menu.setter
    @refresh_menu
    def state_menu(self, value):
        self.__State_menu = value

    @refresh_movie
    def next_movie(self):
        if self.__State_movie == self.__Max_movie:
            self.__State_movie = 1
        else:
            self.__State_movie += 1

    @refresh_movie
    def previous_movie(self):
        if self.__State_movie == 1:
            self.__State_movie = self.__Max_movie
        else:
            self.__State_movie -= 1

if __name__ == '__main__':
    user = User(508519294)
    user.state_movie = 1
    user.state_menu = 1
    user.next_movie()
    user.previous_movie()
    print(1)
