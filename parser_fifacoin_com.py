from bs4 import BeautifulSoup
from parser_common import get_coins_list

URL = {
    'pc': 'https://www.fifacoin.com/fifa-22-coins-pc.html',
    'ps': 'https://www.fifacoin.com/fifa-22-coins-ps4.html',
    'xbox': 'https://www.fifacoin.com/fifa-22-coins-xboxone.html'
    }

REF_URL = {
    'pc': 'https://www.fifacoin.com/fifa-22-coins-pc.html',
    'ps': 'https://www.fifacoin.com/fifa-22-coins-ps4.html',
    'xbox': 'https://www.fifacoin.com/fifa-22-coins-xboxone.html'
    }

DOMAIN = 'fifacoin.com'

#REF_CODE = ''


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    div = soup.find('div', class_ = 'prd-list-table coins-list-table')  # контейнер, в котором лежат все карточки
    if not div:
        return
    items = div.find_all('li')  # карточки

    coins_list = {}

    for item in items:
        item_name = item.find('div', class_='text')  # получаем название
        if item_name:
            item_name = item_name.contents[0].strip().replace('K', '000')  # текст находится в контейнере, где несколько строк текста, поэтому get_text не прокатывает
            space_index = item_name.rfind(' ')  # индекс последнего пробела в строке
            item_value = item_name[space_index + 1:]
            # если значение прошло проверку на число, то к числу и преобразуем, иначе - пропускаем это значение
            if not item_value.isdigit:
                continue
            item_value = int(item_value)

            item_price = item.find('span', class_='price')  # получаем цену
            if not item_price:
                continue

            item_price = item_price.get_text().replace('USD', '')  # если строка с ценой найдена, то вычленяем из неё текст без тэгов
            if item_price.isdigit:
                coins_list[item_value] = float(item_price)

    return coins_list            


def get_content(platform):
    coins_list = get_coins_list(URL[platform], parse)
    return coins_list


#parse({'platform': 'pc', 'quantity': '300000'})