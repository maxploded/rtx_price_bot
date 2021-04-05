from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import path as os_path

import subscribtion_handler
from parameter_error import ParameterError

with open(os_path.abspath(os_path.join(os_path.dirname(__file__), "../BOT_TOKEN.txt")), "r") as token_file:
    TOKEN = token_file.read().strip()


def start(update, context):
    # TODO: Update messages
    update.message.reply_text("Use command /subscribe and models you want to subscribe to! Available models: 3060, 3070, 3080, 3090. Example: \n /subscribe 3070 3090")


def subscribe(update, context):
    try:
        result = subscribtion_handler.subscribe_user(update.effective_chat.id, context.args)
    except ParameterError as e:
        result = str(e)

    update.message.reply_text(result)


def unsubscribe(update, context):
    result = subscribtion_handler.unsubscribe_all(update.effective_chat.id)

    update.message.reply_text(result)


def check_subscriptions(update, context):
    result = subscribtion_handler.check_subscriptions(update.effective_chat.id)

    update.message.reply_text(result)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("check", check_subscriptions))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
