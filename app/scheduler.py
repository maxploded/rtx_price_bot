import schedule
import time
import json
from os import path as os_path

import ozon_parser
import subscription_handler


def job(bot):
    result = {}
    with open(os_path.join(os_path.dirname(os_path.abspath(__file__)), "rtx_models.json")) as models_json:
        models_list = json.load(models_json)
        for model in models_list:
            min_price, max_price = ozon_parser.parse(model)
            result[model] = min_price, max_price

    subscriptions = subscription_handler.get_all_subscriptions()

    for subscription in subscriptions:
        message = ""
        for model in subscription["models"]:
            min_price, max_price = result[model]
            message += f"{model} prices today are: {min_price}-{max_price}"
            bot.send_message(subscription["id"], message)


def run(bot):
    schedule.every().day.at("12:50").do(lambda: job(bot))

    while True:
        schedule.run_pending()
        time.sleep(60)
