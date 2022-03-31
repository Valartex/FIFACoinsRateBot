from bs4 import BeautifulSoup
from parser_common import get_coins_list

URL = {
    'pc': 'https://www.mmoga.com/FIFA-Coins/FUT-Coins-PC,FIFA-22,Comfort-Trade/',
    'ps': 'https://www.mmoga.com/FIFA-Coins/FUT-Coins-PS4-PS5,FIFA-22,Comfort-Trade/',
    'xbox': 'https://www.mmoga.com/FIFA-Coins/FUT-Coins-Xbox-One-XS,FIFA-22,Comfort-Trade/'
    }

REF_URL = {
    'pc': 'https://www.mmoga.com/FIFA-Coins/FUT-Coins-PC,FIFA-22,Comfort-Trade/',
    'ps': 'https://www.mmoga.com/FIFA-Coins/FUT-Coins-PS4-PS5,FIFA-22,Comfort-Trade/',
    'xbox': 'https://www.mmoga.com/FIFA-Coins/FUT-Coins-Xbox-One-XS,FIFA-22,Comfort-Trade/'
    }

DOMAIN = 'mmoga.com'

#REF_CODE = ''


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('li', class_='futPsListItem')
    if not items:
        return

    coins_list = {}

    for item in items:
        item_name = item.find('div', class_='futPsName')  # получаем название
        if item_name:
            item_name = item_name.get_text().strip()           
            space_index = item_name.find(' ')  # индекс первого пробела в строке
            item_value = item_name[:space_index].replace('.', '')            
            # если значение прошло проверку на число, то к числу и преобразуем, иначе - пропускаем это значение
            if not item_value.isdigit:
                continue
            item_value = int(item_value)

            item_price = item.find('div', class_='futPsPrice')  # получаем цену
            if not item_price:
                continue

            item_price = item_price.get_text().replace('$', '').replace('.', '').replace(',', '.').strip()  # если строка с ценой найдена, то вычленяем из неё текст без тэгов
            if item_price.isdigit:
                coins_list[item_value] = float(item_price)

    return coins_list            


def get_content(platform):
    coins_list = get_coins_list(URL[platform], parse)
    return coins_list


# print(get_content('pc'))
# print(get_content('ps'))
# print(get_content('xbox'))
