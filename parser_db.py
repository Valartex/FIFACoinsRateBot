import sqlite3
import datetime
from ref_url import get_ref_url

DB_PATH = 'db/parsing.db'


# Получаем из БД список сайтов
def get_all_sites():
    with sqlite3.connect(DB_PATH) as db_connection:
        sites = []
        cursor = db_connection.cursor()
        cursor.execute('SELECT DISTINCT site FROM parsed_data')
        for site in cursor.fetchall():
            sites.append(site[0])
        return sites


# Формирование финального списка ссылок на сайты
def get_coins_list(parsing_parameters):
    platform = parsing_parameters['platform']
    quantity = int(parsing_parameters['quantity'])

    price_list = []

    sites = get_all_sites()

    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()
        for site in sites:           
            cursor.execute(f'SELECT quantity, price FROM parsed_data WHERE platform="{platform}" AND site="{site}"')
            items_list = cursor.fetchall()

            count = 0
            for item in sorted(items_list):
                item_quantity = item[0]
                item_price = item[1]
                count += 1
                if (item_quantity >= quantity) or (count == len(items_list)):
                    coins_value = str(item_quantity)[::-1].replace('000', 'K', 1)[::-1]
#                    link = f'<a href="{url[platform] + ref_code}"><b>{coins_value} - {coins_list[item_value]}$</b> | {domain}</a>'
                    link = f'<a href="{get_ref_url(site, platform)}"><b>{coins_value} - {item_price}$</b> | {site}</a>'
                    price_list.append((item_price, link))
                    break

        # формируем финальный список из ссылок на сайты
        coins_list = []

        for item in sorted(price_list):
            if item[0] != 0:
                coins_list.append(item[1])            

    return coins_list


# Запись спарсинных данных в БД
def update_data(coins_list, site, platform):
    if not coins_list:
        return

    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS parsed_data ('
                       'site TEXT NOT NULL,'
                       'platform TEXT NOT NULL,'
                       'quantity INTEGER NOT NULL,'
                       'price REAL NOT NULL,'
                       'update_time TEXT,'
                       'CONSTRAINT pk PRIMARY KEY (site, platform, quantity))')

        # удаляем из БД неактуальные записи
        cursor.execute("DELETE FROM parsed_data WHERE julianday('now') - julianday(update_time) > 1")

        for quantity in coins_list.keys():
            price = coins_list[quantity]
            update_time = datetime.datetime.now()
            cursor.execute('INSERT OR REPLACE INTO parsed_data (site, platform, quantity, price, update_time) VALUES (?,?,?,?,?)', (site, platform, quantity, price, update_time))

        db_connection.commit()