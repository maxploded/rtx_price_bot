import requests
from lxml import html


def parse():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-language": "en-US,en;q=0.9",
        "authority": "www.ozon.ru"
    }

    page = requests.get("https://www.ozon.ru/category/videokarty-rtx3080/", headers=headers)

    tree = html.fromstring(page.content)
    input_element = tree.xpath("//input[@min]")[0]
    min_value = input_element.attrib['min']
    max_value = input_element.attrib['max']

    return min_value, max_value
