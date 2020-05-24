import requests
from bs4 import BeautifulSoup
from Logic import SQL
from ya_captcha import Captcha

def update():
    all_data = []
    url = 'https://afisha.yandex.ru/api/events/selection/cinema-today'
    offset = 0
    while True:
        par = {'limit': 20, 'offset': offset, 'hasMixed': 0, 'city': 'nizhny-novgorod'}
        json = requests.get(url, par).json()
        if json['paging']['total'] < offset:
            print(json['paging']['total'])
            print(offset)
            break
        for _, item in enumerate(json['data']):
            title = item['event']['title']
            image = item['event']['image']['sizes']['featuredSelection']['url']
            movie_url = 'https://afisha.yandex.ru' + item['event']['url']
            trailer = search_trailer(title)
            try:
                rating = item['event']['kinopoisk']['value']
            except TypeError:
                rating = None
            try:
                slogan = item['event']['argument']  # or item['event']['argument']
            except TypeError:
                slogan = None
            description = search_description(movie_url)
            event_id = item['event']['id']
            date_movies = item['scheduleInfo']['dates'][0]
            cinemas, sessions = search_cinemas_and_sessions(date_movies, event_id)

            prepare = {'title': title, 'rating': rating,
                       'image': image, 'slogan': slogan,
                       'url': movie_url, 'trailer': trailer,
                       'description': description, 'cinemas': cinemas,
                       'sessions': sessions}
            all_data.append(prepare)
            print(f'{title} записал!')
        offset += 20
    SQL.add_to_base(all_data)
    print("База обновлена")

def search_description(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'accept': '*/*',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        description = soup.contents[1].contents[1].contents[2].contents[0].contents[2].contents[0].contents[0].contents[6].contents[0].contents[1].contents[1].contents[1].text
        return description
    except (AttributeError, IndexError):
        while True:
            try:
                description = Captcha(url).get_description()
                if description:
                    return description
                else:
                    continue
            except AttributeError:
                continue

def search_trailer(title):
    i = 0
    replace_dict = {' ': '+', ',': '%2C', '\'': '%27', ':': '%3A'}

    url = 'https://www.youtube.com/results?search_query='
    for key in replace_dict.keys():
        title = title.replace(key, replace_dict[key])
    url += title + '+трейлер'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'accept': '*/*',
    }
    while True:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        youtube_title = soup.find_all('a', class_='yt-uix-tile-link')[i]
        try:
            if 'watch' in youtube_title.attrs['href']:
                trailer = 'https://www.youtube.com' + youtube_title.attrs['href']
                return trailer
            else:
                i += 1
        except AttributeError:
            continue


def search_cinemas_and_sessions(date, event_id):
    all_cinemas = ''
    all_sessions = ''
    url = f'https://afisha.yandex.ru/api/events/{event_id}/schedule_cinema'
    prm = {
        'limit': '20',
        'offset': '0',
        'date': date,
        'city': 'nizhny-novgorod',
    }
    response_cinemas = requests.get(url, prm).json()
    items_cinemas = response_cinemas["schedule"]["items"]
    print(f'Количество кинотеатров - {len(items_cinemas)}')
    if len(items_cinemas) == 0:
        return '-', '-'
    for item in items_cinemas:
        title = item['place']['title']
        all_cinemas += f'{title},'
        items_sessions = item['schedule'][0]['sessions']
        sessions = ', '.join(session['datetime'][11:-3] for session in items_sessions)
        all_sessions += f'{sessions};'
    return all_cinemas, all_sessions





if __name__ == '__main__':
    update()
