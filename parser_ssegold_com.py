from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from parser_sel_common import get_coins_list

URL = {
    'pc': 'https://www.ssegold.com/fifa22-coins-pc.html',
    'ps': 'https://www.ssegold.com/fifa22-coins-ps4-ps5.html',
    'xbox': 'https://www.ssegold.com/fifa22-coins-xbox-one-xbox-series.html'
    }

REF_URL = {
    'pc': 'https://www.ssegold.com/fifa22-coins-pc.html?affiliateid=5065570',
    'ps': 'https://www.ssegold.com/fifa22-coins-ps4-ps5.html?affiliateid=5065570',
    'xbox': 'https://www.ssegold.com/fifa22-coins-xbox-one-xbox-series.html?affiliateid=5065570'
    }

DOMAIN = 'ssegold.com'

#REF_CODE = '?affiliateid=5065570'


def parse(web_driver):
    # div = WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="items"]/div/div/div[1]/div/div[2]/div[3]/div/input')))

    time.sleep(10)

    # div = web_driver.find_element_by_class_name('fifa-order-cont')  # контейнер, в котором лежат все карточки
    # if not div:
    #     return {}
    #
    # items = div.find_elements_by_class_name('fifa21-list')  # карточки

    items = web_driver.find_element_by_class_name('fifa-order-cont').find_elements_by_class_name('fifa21-list')

    coins_list = {}

    for item in items:
        item_name = item.find('h2', class_ = 'product-name')  # получаем название

        if item_name:
            item_value = item_name.get_text().replace(' K', '000').strip()
            # если значение прошло проверку на число, то к числу и преобразуем, иначе - пропускаем это значение
            if not item_value.isdigit:
                continue
            item_value = int(item_value)

            item_price = item.find('span', class_='product-price')  # получаем цену
            if not item_price:
                continue

            item_price = item_price.get_text().replace('$ ', '').strip()  # если строка с ценой найдена, то вычленяем из неё текст без тэгов
            if item_price.isdigit:
                coins_list[item_value] = float(item_price)

    return coins_list            


def get_content(platform):
    coins_list = get_coins_list(URL[platform], parse)
    return coins_list


print(get_content('pc'))
# print(get_content('ps'))
# print(get_content('xbox'))
