from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_coins_list(url, parse_func):
    coins_list = {}

    web_driver_path = "web_drivers/chromedriver.exe"
    # web_driver_path = "/home/fifa_crb/web_drivers/chromedriver"
    # web_driver_path = "/snap/bin/chromium.chromedriver"
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-gpu')
    web_driver = webdriver.Chrome(executable_path=web_driver_path, chrome_options=options)
    web_driver.set_window_size(1920, 1080)

    try:
        web_driver.get(url)
        coins_list = parse_func(web_driver)
    except Exception as ex:
        print(ex)
    finally:
        web_driver.close()
        web_driver.quit()

    return coins_list