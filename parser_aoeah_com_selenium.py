from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from parser_sel_common import get_coins_list

URL = {
    'pc': 'https://www.aoeah.com/fifa-coins/fifa21-coins/pc/',
    'ps': 'https://www.aoeah.com/fifa-coins/fifa21-coins/ps4/',
    'xbox': 'https://www.aoeah.com/fifa-coins/fifa21-coins/xbox%20one/'
    }

REF_URL = {
    'pc': 'https://www.aoeah.com/sellers/fifa21-coins-pc',
    'ps': 'https://www.aoeah.com/sellers/fifa21-coins-ps4',
    'xbox': 'https://www.aoeah.com/sellers/fifa21-coins-xbox'
    }

DOMAIN = 'aoeah.com'

#REF_CODE = ''


def parse(web_driver):
    COINS_VALUE = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000]
    coins_list = {}

    # input_field = WebDriverWait(web_driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="items"]/div/div/div[1]/div/div[1]/div[2]/div/input')))
    input_field = web_driver.find_element_by_class_name('cnum')  #input-na

    if not input_field:
        return {}

    for coin_value in COINS_VALUE:
        input_field.send_keys(Keys.CONTROL, 'a') # выделяем предыдущий текст в поле ввода, чтобы он стёрся при вводе нового
        input_field.send_keys(str(coin_value)) # вводим новое количество монет в поле
        time.sleep(0.5) # ждём пол-секунды, чтобы успела посчитаться цена

        coin_price = web_driver.find_element_by_class_name('cprice') # находим элемент, содержащий цену
        coin_price = coin_price.text.strip()
        if coin_price.isdigit:
            coins_list[coin_value * 1000] = float(coin_price)

    return coins_list


def get_content(platform):
    coins_list = get_coins_list(URL[platform], parse)
    return coins_list


# print(get_content('pc'))
# print(get_content('ps'))
# print(get_content('xbox'))