import json
import logging
import os

from app.main.resource.fbchat import Client
from app.main.resource.fbchat.models import *

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s',
                    datefmt='%d-%b-%Y %H:%M:%S')
logger = logging.getLogger()

user = os.getenv('FB_USER_EMAIL_ADDRESS')
password = os.getenv('FB_USER_PASSWORD')
thread_id = int(os.getenv('FB_THREAD_ID'))


def get_client():
    cookies = {}
    try:
        # Load the session cookies
        with open('app/main/config/messenger/session.json', 'r') as f:
            cookies = json.load(f)
            client = Client('email', 'password', session_cookies=cookies)
    except:
        # If it fails, never mind, we'll just login again
        client = Client(user, password)
        cookies = client.getSession()
        with open('app/main/config/messenger/session.json', "w") as f:
            json.dump(cookies, f)

    return client


def send_msg_to_thread(message):
    client = get_client()
    logger.info("Login succeed")
    try:
        logger.info(thread_id)
        client.send(Message(text=message), thread_id=thread_id, thread_type=ThreadType.USER)
    except FBchatUserError as e:
        logger.error(e)
        try:
            client.send(Message(text=message), thread_id=thread_id, thread_type=ThreadType.GROUP)
        except Exception as e:
            raise e

    with open('app/main/config/messenger/session.json', 'w') as f:
        json.dump(client.getSession(), f)
    client.logout()



