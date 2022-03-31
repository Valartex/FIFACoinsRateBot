from bs4 import BeautifulSoup
from parser_common import get_coins_list

URL = {
    'pc': 'https://www.utplay.com/fifa-22-coins/pc',
    'ps': 'https://www.utplay.com/fifa-22-coins/ps4',
    'xbox': 'https://www.utplay.com/fifa-22-coins/xbox%20one'
    }

REF_URL = {
    'pc': 'https://www.utplay.com/sellers/fifa21-coins-pc',
    'ps': 'https://www.utplay.com/sellers/fifa21-coins-ps4',
    'xbox': 'https://www.utplay.com/sellers/fifa21-coins-xbox'
    }

DOMAIN = 'utplay.com'

#REF_CODE = ''


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    # всего таких дивов два: первый отображается (Player Auction), второй скрыт (Comfort Trade)
    div = soup.find_all('div', class_='list-table')
    if not div:
        return
    # находим все строки таблицы
    items = div[1].find_all('table')[1].find_all('tr', class_='')

    coins_list = {}

    for item in items:
        item_name = item.find('td', class_='')  # получаем строку с названием
        if item_name:
            item_name = item_name.get_text().strip().replace('K', '000')
            space_index = item_name.rfind(' ')  # индекс последнего пробела в строке
            item_value = item_name[space_index + 1:]
            # если значение прошло проверку на число, то к числу и преобразуем, иначе - пропускаем это значение
            if item_value.isdigit:
                item_value = int(item_value)
            else:
                continue    
            
            item_price = item.find('label', class_='')  # получаем цену либо отсюда
            if not item_price:
                item_price = item.find('b', class_='oprice2')  # либо, если не получилось найти, то отсюда
            if item_price:
                item_price = item_price.get_text().replace(' USD', '')  # если строка с ценой найдена, то вычленяем из неё текст без тэгов
                if item_price.isdigit:
                    coins_list[item_value] = float(item_price)

    return coins_list


def get_content(platform):
    coins_list = get_coins_list(URL[platform], parse)
    return coins_list


# print(get_content('pc'))
# print(get_content('ps'))
# print(get_content('xbox'))

