from python_rucaptcha import ImageCaptcha
import requests
from bs4 import BeautifulSoup



class Captcha(object):
    __Token = 'your_token'
    __Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'accept': '*/*',
    }

    def __init__(self, url):
        response = requests.get(url, headers=self.__Headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.__Url = url
        self.__Image = soup.find('div', class_='captcha__image').contents[0].attrs['src']
        self.__Redirect = soup.find('input', class_='form__retpath').attrs['value']
        self.__Key = soup.find('input', class_='form__key').attrs['value']
        self.__Task_id = None
        self.__Answer = self.__decide()


    @property
    def answer(self):
        return f'https://afisha.yandex.ru/checkcaptcha?key={self.__Key}&retpath={self.__Redirect}&rep={self.__Answer}'

    def get_description(self):
        response = requests.get(self.answer, headers=self.__Headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            description = soup.find('div', class_="concert-description__text-wrap").text
            report = requests.get(f'https://rucaptcha.com/res.php?key={self.__Token}&action=reportgood&id={self.__Task_id}')
            print(f'Report Good - ANSWER:{report.text}')
            return description
        except AttributeError:
            return None

    def __decide(self):
        user_answer_full = ImageCaptcha.ImageCaptcha(
            rucaptcha_key=self.__Token,
            service_type='rucaptcha',
            save_format="temp",
            phrase=0,
            regsense=0,
            numeric=0,
            calc=0,
            min_len=0,
            max_len=0,
            language=0,
            textinstructions="",
            pingback="",
        ).captcha_handler(captcha_link=self.__Image, verify=True, proxies={})

        if not user_answer_full["error"]:
            # решение капчи
            self.__Task_id = user_answer_full["taskId"]
            return user_answer_full["captchaSolve"]
        elif user_answer_full["error"]:
            # Тело ошибки, если есть
            print(user_answer_full["errorBody"]["text"])
            print(user_answer_full["errorBody"]["id"])





if __name__ == '__main__':
    C = Captcha('https://afisha.yandex.ru/nizhny-novgorod/cinema/vpered-2020?schedule-preset=today')
    description = C.get_description()
    print(1)