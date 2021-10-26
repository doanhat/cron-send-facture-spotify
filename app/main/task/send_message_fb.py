import logging
import os
from dotenv import load_dotenv

from fbchat import Client
from fbchat.models import *

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s',
                    datefmt='%d-%b-%Y %H:%M:%S')
logger = logging.getLogger()
load_dotenv("config/facebook/fbchat/.env")

user = os.getenv('USER_EMAIL_ADDRESS')
password = os.getenv('USER_PASSWORD')
thread_id = os.getenv('THREAD_ID')


def get_client():
    client = Client(user, password)
    return client


def send_msg_to_group(client, group_id, message):
    client = get_client()
    group = client.fetchGroupInfo(group_id)
    group_thread = group[group_id]
    client.send(Message(text=message), thread_id=group_id, thread_type=ThreadType.GROUP)
    client.logout()


def send_msg_to_user(client, user_id, message):
    client = get_client()
    user = client.fetchUserInfo(user_id)
    user_thread = user[user_id]
    client.send(Message(text=message), thread_id=user_id, thread_type=ThreadType.USER)
    client.logout()


logger.info(user)
# send_msg_to_group(get_client(), thread_id, "Aloooo")
