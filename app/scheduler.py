import schedule
import time
import json
import traceback
from os import path as os_path

import ozon_parser
import ekatalog_parser
import subscription_handler


def job(bot):
    result = {}
    with open(os_path.join(os_path.dirname(os_path.abspath(__file__)), "rtx_models.json")) as models_json:
        models_list = json.load(models_json)
        for model in models_list:
            try:
                ozon = ozon_parser.parse(model)
            except:
                traceback.print_exc()
                ozon = None

            try:
                ekatalog = ekatalog_parser.parse(model)
            except:
                traceback.print_exc()
                ekatalog = None

            result[model] = {
                "ozon": ozon,
                "ekatalog": ekatalog
            }

    subscriptions = subscription_handler.get_all_subscriptions()

    for subscription in subscriptions:
        message = ""
        for model in subscription["models"]:
            ozon = result[model]["ozon"]
            ekatalog = result[model]["ekatalog"]
            if not ozon and not ekatalog:
                raise RuntimeError("All requests failed")

            message += f"{model} prices today are:"

            if ozon:
                message += f"\n ozon.ru: {ozon[0]} - {ozon[1]}"

            if ekatalog:
                message += f"\n e-katalog.ru: {ekatalog[0]} - {ekatalog[1]}"

            bot.send_message(subscription["id"], message)


def run(bot):
    schedule.every().day.at("12:50").do(lambda: job(bot))

    while True:
        schedule.run_pending()
        time.sleep(60)
