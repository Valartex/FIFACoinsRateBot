from parser_db import update_data
import parser_aoeah_com
import parser_u7buy_com
import parser_mulefactory_com
import parser_fifacoin_com
import parser_mmoga_com
# import parser_utplay_com
import parser_buyfifacoin_net
import parser_ssegold_com
import parser_futcoin_net
import parser_utstore_com
import parser_igvault_com

PLATFORMS = ['pc', 'ps', 'xbox']


def update_parser_db():
    # парсим сайты и записываем результат в БД
    for platform in PLATFORMS:
        coins_list = parser_aoeah_com.get_content(platform)
        update_data(coins_list, 'aoeah.com', platform)

        coins_list = parser_u7buy_com.get_content(platform)
        update_data(coins_list, 'u7buy.com', platform)

        coins_list = parser_mulefactory_com.get_content(platform)
        update_data(coins_list, 'mulefactory.com', platform)

        coins_list = parser_fifacoin_com.get_content(platform)
        update_data(coins_list, 'fifacoin.com', platform)

        coins_list = parser_mmoga_com.get_content(platform)
        update_data(coins_list, 'mmoga.com', platform)

        coins_list = parser_buyfifacoin_net.get_content(platform)
        update_data(coins_list, 'buyfifacoin.net', platform)

        coins_list = parser_ssegold_com.get_content(platform)
        update_data(coins_list, 'ssegold.com', platform)

        coins_list = parser_futcoin_net.get_content(platform)
        update_data(coins_list, 'futcoin.net', platform)

        coins_list = parser_utstore_com.get_content(platform)
        update_data(coins_list, 'utstore.com', platform)     

        coins_list = parser_igvault_com.get_content(platform)
        update_data(coins_list, 'igvault.com', platform)

        # копирует aoeah.com
        # coins_list = parser_utplay_com.get_content(platform)
        # update_data(coins_list, 'utplay.com', platform)

update_parser_db()