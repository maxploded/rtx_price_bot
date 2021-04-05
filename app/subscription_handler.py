import json
from tinydb import TinyDB, Query
from os import path as os_path

from parameter_error import ParameterError

db = TinyDB('subscription_db.json')
user = Query()


def subscribe_user(chat_id, models: list):
    if type(models) is not list:
        raise RuntimeError("models should be of type list")

    if not models or len(models) == 0:
        raise ParameterError("Please provide model names you want to subscribe to!")

    with open(os_path.join(os_path.dirname(os_path.abspath(__file__)), "rtx_models.json")) as models_json:
        models_list = json.load(models_json)
        for model in models:
            if model not in models_list:
                raise ParameterError(f"'{model}' is not a supported model")

    record = db.search(user.id == chat_id)

    if not record:
        db.insert({"id": chat_id, "models": models})
    else:
        db.update({"models": models}, user.id == chat_id)

    return f"You are now subscribed to {models}"


def check_subscriptions(chat_id):
    record = db.search(user.id == chat_id)

    if not record:
        return "You are not subscribed to any models yet!"
    else:
        return f"You are subscribed to {record[0]['models']}"


def unsubscribe_all(chat_id):
    db.remove(user.id == chat_id)

    return "You are now unsubscribed!"


def get_all_subscriptions():
    return db.all()
