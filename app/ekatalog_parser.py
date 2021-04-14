import requests
from lxml import html
import re


def parse(model):
    if model != '3080':
        raise ValueError('3080 only supported') # TODO: update for other models

    headers = {
        'authority': 'www.e-katalog.ru',
        'scheme': 'https',
        'path': '/ek-list.php?katalog_=189&presets_=42257&order_=price',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'if-modified-since': 'Wed, 14 Apr 2021 11:06:01 GMT'

    }

    page = requests.get("https://www.e-katalog.ru/ek-list.php?katalog_=189&presets_=42257&order_=price", headers=headers)
    tree = html.fromstring(page.content)

    prices = []

    usual_prices = tree.xpath("//div[@class='model-price-range']/parent::div")
    for div in usual_prices:
        not_available_div = div.xpath("./div[contains(@class, 'model-hot-prices-not-avail')]")
        if not not_available_div:
            spans = div.xpath("./div/a/span[contains(@id,'price_')]")
            if spans:
                value = re.sub(r"\D+", '', spans[0].text)
                try:
                    prices.append(int(value))
                except:
                    pass

    hot_prices = tree.xpath("//td[contains(@class, 'model-hot-prices-td')]//div[@class='pr31 ib']/span/text()")
    for hot_price in hot_prices:
        value = re.sub(r"\D+", '', hot_price)
        try:
            prices.append(int(value))
        except:
            pass

    min_price = min(prices)
    max_price = max(prices)

    return min_price, max_price
