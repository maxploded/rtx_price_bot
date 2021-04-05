import schedule
import time

import ozon_parser
import subscription_handler


def job(bot):
    min_price, max_price = ozon_parser.parse()
    chat_ids = subscription_handler.get_subscribed_users()

    for chat_id in chat_ids:
        bot.send_message(chat_id, f"3080 price: {min_price}-{max_price}")


def run(bot):
    schedule.every().day.at("12:50").do(lambda: job(bot))

    while True:
        schedule.run_pending()
        time.sleep(60)