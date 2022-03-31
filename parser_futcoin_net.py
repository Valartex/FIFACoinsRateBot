from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from parser_sel_common import get_coins_list

URL = {
    'pc': 'https://www.futcoin.net/en/items/pc',
    'ps': 'https://www.futcoin.net/en/items/ps',
    'xbox': 'https://www.futcoin.net/en/items/xb'
    }

REF_URL = {
    'pc': 'https://www.futcoin.net/en/items/pc?ref=v2425',
    'ps': 'https://www.futcoin.net/en/items/ps?ref=v2425',
    'xbox': 'https://www.futcoin.net/en/items/xb?ref=v2425'
    }

DOMAIN = 'futcoin.net'

#REF_CODE = '?ref=v2425'


def parse(web_driver):
    COINS_VALUE = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    coins_list = {}

    input_field = WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="items"]/div/div/div[1]/div/div[2]/div[3]/div/input')))
    # input_field = web_driver.find_element_by_xpath('//*[@id="items"]/div/div/div[1]/div/div[2]/div[3]/div/input')
    # time.sleep(5)
    if not input_field:
        return {}

    for coin_value in COINS_VALUE:
        input_field.send_keys(Keys.CONTROL, 'a') # выделяем предыдущий текст в поле ввода, чтобы он стёрся при вводе нового
        input_field.send_keys(str(coin_value * 1000)) # вводим новое количество монет в поле
        time.sleep(.5) # ждём пол-секунды, чтобы успела посчитаться цена

        coin_price = web_driver.find_element_by_class_name('uk-h1') # находим элемент, содержащий цену
        if not coin_price:
            continue
        coin_price = coin_price.text.strip().replace('$', '')
        if coin_price.isdigit:
            coins_list[coin_value * 1000] = float(coin_price)  

    return coins_list            


def get_content(platform):
    coins_list = get_coins_list(URL[platform], parse)
    return coins_list


# print(get_content('pc'))
# print(get_content('ps'))
# print(get_content('xbox'))