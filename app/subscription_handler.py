import json
from os import path as os_path
import os
import psycopg2

from parameter_error import ParameterError

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()


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

    cur.execute("SELECT * FROM subscriptions where id = %s;", (str(chat_id),))
    record = cur.fetchone()

    if not record:
        cur.execute("INSERT INTO subscriptions (id, models) VALUES (%s, %s);", (str(chat_id), models))
    else:
        cur.execute("UPDATE subscriptions SET models = %s WHERE id = %s;", (models, str(chat_id)))

    conn.commit()

    return f"You are now subscribed to {models}"


def check_subscriptions(chat_id):
    cur.execute("SELECT * FROM subscriptions where id = %s;", (str(chat_id),))
    record = cur.fetchone()

    if not record:
        return "You are not subscribed to any models yet!"
    else:
        return f"You are subscribed to {record[1]}"


def unsubscribe_all(chat_id):
    cur.execute("DELETE FROM subscriptions where id = %s;", (str(chat_id),))
    conn.commit()

    return "You are now unsubscribed!"


def get_all_subscriptions():
    cur.execute("SELECT * FROM subscriptions;")
    records = cur.fetchall()
    return [{"id": subscription[0], "models": subscription[1]} for subscription in records]
