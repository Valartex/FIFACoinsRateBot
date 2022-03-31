from bs4 import BeautifulSoup
from parser_common import get_coins_list

URL = {
    'pc': 'https://www.mulefactory.com/fut_22/pc/',
    'ps': 'https://www.mulefactory.com/fut_22/ps4_ps5/',
    'xbox': 'https://www.mulefactory.com/fut_22/xbox_one_series/'
    }

REF_URL = {
    'pc': 'https://www.mulefactory.com/fut_22/pc/?ref=334577&campaign=25200',
    'ps': 'https://www.mulefactory.com/fut_22/ps4_ps5/?ref=334577&campaign=25200',
    'xbox': 'https://www.mulefactory.com/fut_22/xbox_one_series/?ref=334577&campaign=25200'
    }

DOMAIN = 'mulefactory.com'

#REF_CODE = '?ref=334577&campaign=25200'


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='data')
    if not items:
        return

    coins_list = {}

    for item in items:
        item_name = item.find('h4', class_='')  # получаем название
        if item_name:
            item_value = item_name.get_text().replace(' K Coins', '000')
            # если значение прошло проверку на число, то к числу и преобразуем, иначе - пропускаем это значение
            if not item_value.isdigit:
                continue
            item_value = int(item_value)

            item_price = item.find('label', class_='price tooltip')  # получаем цену
            if not item_price:
                continue

            item_price = item_price.get_text().replace(' USD', '')  # если строка с ценой найдена, то вычленяем из неё текст без тэгов
            if item_price.isdigit:
                coins_list[item_value] = float(item_price)

    return coins_list            


def get_content(platform):
    coins_list = get_coins_list(URL[platform], parse)
    return coins_list


#parse()
