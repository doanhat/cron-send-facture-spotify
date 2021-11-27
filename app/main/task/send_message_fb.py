import json
import os

from dotenv import load_dotenv
from google.cloud import secretmanager

from app.main.config.environment.environment_configuration import CONFIG
from app.main.helper.gcp_helper import get_secret, add_secret
from app.main.helper.logger import logger
from app.main.resource.fbchat import Client
from app.main.resource.fbchat.models import *

load_dotenv("env/.env")
THREAD_ID = int(CONFIG.get("FB_THREAD_ID"))
PROJECT_ID = CONFIG.get("PROJECT_ID")
SES_SECRET_ID = CONFIG.get("SES_SECRET_ID")
CLIENT = secretmanager.SecretManagerServiceClient()


def get_client():
    try:
        # Load the session cookies
        cookies = json.load(get_secret(CLIENT, PROJECT_ID, SES_SECRET_ID))
        client = Client('email', 'password', session_cookies=cookies)
    except Exception as e:
        logger.error(e)
        # If it fails, never mind, we'll just login again
        user = os.getenv('FB_USER_EMAIL_ADDRESS')
        password = os.getenv('FB_USER_PASSWORD')
        client = Client(user, password)
        cookies = client.getSession()
        add_secret(CLIENT, PROJECT_ID, SES_SECRET_ID, json.dumps(cookies))

    return client


def send_msg_to_thread(message):
    client = get_client()
    logger.info("Login succeed")
    try:
        logger.info(THREAD_ID)
        client.send(Message(text=message), thread_id=THREAD_ID, thread_type=ThreadType.USER)
    except FBchatUserError as e:
        logger.error(e)
        try:
            client.send(Message(text=message), thread_id=THREAD_ID, thread_type=ThreadType.GROUP)
        except Exception as e:
            raise e

    add_secret(CLIENT, PROJECT_ID, SES_SECRET_ID, json.dumps(client.getSession()))
    client.logout()
