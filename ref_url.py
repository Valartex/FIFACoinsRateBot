import parser_aoeah_com
import parser_u7buy_com
import parser_mulefactory_com
import parser_fifacoin_com
import parser_mmoga_com
import parser_buyfifacoin_net
import parser_ssegold_com
import parser_futcoin_net
import parser_utstore_com
import parser_igvault_com
# import parser_utplay_com


def get_ref_url(site, platform):
    SWITCH_URL = {
        'aoeah.com': parser_aoeah_com.REF_URL,
        'u7buy.com': parser_u7buy_com.REF_URL,
        'mulefactory.com': parser_mulefactory_com.REF_URL,
        'fifacoin.com': parser_fifacoin_com.REF_URL,
        'mmoga.com': parser_mmoga_com.REF_URL,
        'buyfifacoin.net': parser_buyfifacoin_net.REF_URL,
        'ssegold.com': parser_ssegold_com.REF_URL,
        'futcoin.net': parser_futcoin_net.REF_URL,
        'utstore.com': parser_utstore_com.REF_URL,
        'igvault.com': parser_igvault_com.REF_URL
        # 'utplay.com': parser_utplay_com.REF_URL
    }

    try:
        url = SWITCH_URL[site][platform]
    except:
        url = ''    

    return url