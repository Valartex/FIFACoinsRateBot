# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from parser_sel_common import get_coins_list

URL = {
    'pc': 'https://www.utstore.com/fifa/coins/pc',
    'ps': 'https://www.utstore.com/fifa/coins/playstation-4',
    'xbox': 'https://www.utstore.com/fifa/coins/xbox-one'
    }

REF_URL = {
    'pc': 'https://www.utstore.com/fifa/coins/pc',
    'ps': 'https://www.utstore.com/fifa/coins/playstation-4',
    'xbox': 'https://www.utstore.com/fifa/coins/xbox-one'
    }

DOMAIN = 'utstore.com'

#REF_CODE = ''


def parse(web_driver):
    coins_list = {}

    # меняем валюту на доллары
    web_driver.find_element_by_id('dropdown-currency').click()
    web_driver.find_element_by_xpath('//*[@id="currency"]/div/a[3]').click()

    # input_field = WebDriverWait(web_driver, 20).until(EC.element_to_be_clickable((By.XPATH, '')))
    input_field = web_driver.find_element_by_id('quantity')

    if not input_field:
        return {}

    # очищаем поле ввода
    input_field.send_keys(Keys.CONTROL, 'a')
    input_field.send_keys('0')
    input_field.send_keys(Keys.ENTER)

    max_slider_value = web_driver.find_element_by_id('slider').get_attribute('max')
    max_slider_value = int(max_slider_value)

    inc_button = web_driver.find_element_by_id('button-increment') #  находим кнопку инкрементирования количества
    amount_field = web_driver.find_element_by_id('amount') #  скрытый элемент, содержащий текущее положение слайдера (количество монет)
    price_field = web_driver.find_element_by_id('cost-total') #  поле, содержащее цену

    # time.sleep(1)
    coin_value = 1

    while coin_value != max_slider_value:
        # получаем количество монет
        coin_value = amount_field.get_attribute('value')
        coin_value = str(coin_value).replace(',', '').strip()
        coin_value = int(coin_value)

        coin_price = price_field.text.strip() #  получаем цену

        coins_list[coin_value] = float(coin_price) # записываем значения в словарь      
   
        inc_button.click() # кликаем по кнопке инкрементирования количества

    return coins_list            


def get_content(platform):
    coins_list = get_coins_list(URL[platform], parse)
    return coins_list


#print(get_content('pc'))
#print(get_content('ps'))
#print(get_content('xbox'))