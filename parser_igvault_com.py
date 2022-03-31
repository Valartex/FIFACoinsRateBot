# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from parser_sel_common import get_coins_list

URL = {
    'pc': 'https://www.igvault.com/FIFA-22-Coins',
    'ps': 'https://www.igvault.com/FIFA-22-Coins',
    'xbox': 'https://www.igvault.com/FIFA-22-Coins'
    }

REF_URL = {
    'pc': 'https://www.igvault.com/FIFA-22-Coins',
    'ps': 'https://www.igvault.com/FIFA-22-Coins',
    'xbox': 'https://www.igvault.com/FIFA-22-Coins'
    }

DOMAIN = 'igvault.com'
selected_platform = ''

#REF_CODE = ''


def parse(web_driver):
    COINS_RANGES = [range(200, 1000, 100), range(1000, 10000, 500), range(10000, 21000, 1000)]
    coins_list = {}

    # меняем валюту на USD
    web_driver.find_element_by_class_name('use-xiala').click()
    web_driver.find_element_by_xpath('/html/body/header/div[1]/div/div/div[2]/ul/li[2]/div/div[2]/div/div/input').click()
    web_driver.find_element_by_xpath('/html/body/header/div[1]/div/div/div[2]/ul/li[2]/div/div[2]/div/div/ul/li[1]').click()
    # select_element = web_driver.find_element_by_xpath('/html/body/header/div[1]/div/div/div[2]/ul/li[4]/div/div[2]/div/select')

    # select_object = Select(select_element)
    # select_object.select_by_visible_text('USD')
    #
    time.sleep(3) #  ждём, пока страница обновится после смены валюты

    # выбираем платформу
    web_driver.find_element_by_xpath('/html/body/section[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div/div[1]').click()
    if selected_platform == 'ps':
        web_driver.find_element_by_xpath('/html/body/section[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div/div[2]/div/ul/li[1]').click()
    if selected_platform == 'pc':
        web_driver.find_element_by_xpath('/html/body/section[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div/div[2]/div/ul/li[3]').click()
    elif selected_platform == 'xbox':
        web_driver.find_element_by_xpath('/html/body/section[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div/div[2]/div/ul/li[2]').click()

    time.sleep(2)    

    input_field = web_driver.find_element_by_xpath('/html/body/section[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[3]/div/div/input') #  поле ввода

    for coins_range in COINS_RANGES:
        for coin_value in coins_range:
            input_field.send_keys(Keys.CONTROL, 'a') # выделяем предыдущий текст в поле ввода, чтобы он стёрся при вводе нового
            input_field.send_keys(str(coin_value)) # вводим новое количество монет в поле

            time.sleep(1.8) # ждём, чтобы успела посчитаться цена

            coin_price = web_driver.find_element_by_xpath('/html/body/section[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/strong[1]') # находим элемент, содержащий цену
            coin_price = coin_price.text.strip().replace('$', '')
            coin_price = coin_price.replace(',', '')
            if coin_price.isdigit:
                coins_list[coin_value * 1000] = float(coin_price)  

    return coins_list            


def get_content(platform):
    global selected_platform 
    selected_platform = platform
    coins_list = get_coins_list(URL[platform], parse)
    return coins_list


# print(get_content('pc'))
# print(get_content('ps'))
# print(get_content('xbox'))