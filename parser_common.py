from random import choice
import requests

USER_AGENTS = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
               'Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12 Version/12.16',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.1; rv:84.0) Gecko/20100101 Firefox/84.0',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
               'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko']


def get_headers():
    return {'user-agent': choice(USER_AGENTS),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def get_html(url, params=None):
    r = requests.get(url, headers = get_headers(), params = params)
    return r


def get_coins_list(url, parse_func):
    coins_list = {}
    try:
        html = get_html(url)
        coins_list = parse_func(html.text)
    except:
        return {}

    return coins_list