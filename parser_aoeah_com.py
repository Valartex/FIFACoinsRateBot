from bs4 import BeautifulSoup
from parser_common import get_coins_list

URL = {
    'pc': 'https://www.aoeah.com/fifa-coins/fifa22-coins/pc',
    'ps': 'https://www.aoeah.com/fifa-coins/fifa22-coins/ps4',
    'xbox': 'https://www.aoeah.com/fifa-coins/fifa22-coins/xbox%20one'
    }

REF_URL = {
    'pc': 'https://www.aoeah.com/sellers/fifa22-coins-pc',
    'ps': 'https://www.aoeah.com/sellers/fifa22-coins-ps4',
    'xbox': 'https://www.aoeah.com/sellers/fifa22-coins-xbox'
    }

DOMAIN = 'aoeah.com'

#REF_CODE = ''


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    # всего таких дивов два: первый отображается (Player Auction), второй скрыт (Comfort Trade)
    div = soup.find_all('div', class_='gold-list')
    if div:
        # находим кнопки добавления в корзину
        addcart_buttons = div[1].find_all('input', class_='sign addcart')
    else:
        return    

    coins_list = {}

    for addcart_button in addcart_buttons:
        tr = addcart_button.parent.parent.parent  # получаем строку таблицы, в которой находится кнопка добавления в корзину
        item_name = tr.find('td', class_='')  # получаем название
        if item_name:
            item_name = item_name.get_text().strip()
            space_index = item_name.rfind(' ')  # индекс последнего пробела в строке
            item_value = item_name[space_index + 1:].replace('K', '000')
            # если значение прошло проверку на число, то к числу и преобразуем, иначе - пропускаем это значение
            if item_value.isdigit:
                item_value = int(item_value)
            else:
                continue    

            item_price = tr.find('label', class_='')  # получаем цену либо отсюда
            if not item_price:
                item_price = tr.find('b', class_='oprice2')  # либо, если не получилось найти, то отсюда
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