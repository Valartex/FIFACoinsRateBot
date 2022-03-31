from bs4 import BeautifulSoup
from parser_common import get_coins_list

URL = {
    'pc': 'https://www.u7buy.com/fut22/fut22-coins/pc.html',
    'ps': 'https://www.u7buy.com/fut22/fut22-coins/ps4.html',
    'xbox': 'https://www.u7buy.com/fut22/fut22-coins/xboxone.html'
    }

REF_URL = {
    'pc': 'https://www.u7buy.com/fut22/fut22-coins/pc.html?code=473428',
    'ps': 'https://www.u7buy.com/fut22/fut22-coins/ps4.html?code=473428',
    'xbox': 'https://www.u7buy.com/fut22/fut22-coins/xboxone.html?code=473428'
    }

DOMAIN = 'u7buy.com'

#REF_CODE = '?code=473428'


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', {'class': 'area product-single clear-float', 'style': ''})
    if not items:
        return

    coins_list = {}

    for item in items:
        item_name = item.find('i', class_='')  # получаем название
        if item_name:
            item_value = item_name.get_text().replace('K ', '000')
            # если значение прошло проверку на число, то к числу и преобразуем, иначе - пропускаем это значение
            if not item_value.isdigit:
                continue
            item_value = int(item_value)

            item_price = item.find('span', class_='nprice')  # получаем цену
            if not item_price:
                continue

            item_price = item_price.get_text().replace(' USD $ ', '').replace(',', '')  # если строка с ценой найдена, то вычленяем из неё текст без тэгов
            if item_price.isdigit:
                coins_list[item_value] = float(item_price)

    return coins_list            


def get_content(platform):
    coins_list = get_coins_list(URL[platform], parse)
    return coins_list


# print(get_content('pc'))
# print(get_content('ps'))
# print(get_content('xbox'))
