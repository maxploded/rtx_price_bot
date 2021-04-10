from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import environ
import traceback

import subscription_handler
import scheduler
from parameter_error import ParameterError

token = environ.get('RTX_TOKEN')
updater = Updater(token, use_context=True)

admin_chat_id = environ.get('ADMIN_CHAT_ID')


def test_error(update, context):
    try:
        raise RuntimeError("Test runtime error")
    except:
        handle_exception()


def handle_exception():
    traceback.print_exc()
    updater.bot.send_message(admin_chat_id, traceback.format_exc())


def start(update, context):
    try:
        available_models = subscription_handler.get_available_models()
        available_models_string = ", ".join(available_models)
    except:
        handle_exception()
        return

    update.message.reply_text(f"Use command /subscribe and models you want to subscribe to! Available models: "
                              f"{available_models_string}. Example: \n /subscribe 3070 3090")


def subscribe(update, context):
    try:
        result = subscription_handler.subscribe_user(update.effective_chat.id, context.args)
    except ParameterError as e:
        result = str(e)
    except:
        handle_exception()
        return

    update.message.reply_text(result)


def unsubscribe(update, context):
    try:
        result = subscription_handler.unsubscribe_all(update.effective_chat.id)
    except:
        handle_exception()
        return

    update.message.reply_text(result)


def check_subscriptions(update, context):
    try:
        result = subscription_handler.check_subscriptions(update.effective_chat.id)
    except:
        handle_exception()
        return

    update.message.reply_text(result)


def main():
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("check", check_subscriptions))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dp.add_handler(CommandHandler("testerror", test_error))

    updater.start_polling()

    try:
        scheduler.run(updater.bot)
    except:
        handle_exception()

    updater.idle()


if __name__ == '__main__':
    main()

