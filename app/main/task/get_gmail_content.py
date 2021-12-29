import base64
import json
from datetime import date, timedelta

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.cloud import secretmanager
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.main.config.environment.environment_configuration import PROJECT_ID, TOK_SECRET_ID, CRE_SECRET_ID
from app.main.data.GmailData import GmailData
from app.main.helper.gcp_helper import get_secret, add_secret
from app.main.helper.logger import logger

load_dotenv("env/.env")

# Define the SCOPES. If modifying it, delete the token.json file.

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

CLIENT = secretmanager.SecretManagerServiceClient()


def get_google_service():
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # Uncomment this section if using local token.json
    # ---
    # The file token.json contains the user access token.
    # Check if it exists
    # if os.path.exists('app/main/config/google/API/token.json'):
    #     # Read the token from the file and store it in the variable creds
    #     creds = Credentials.from_authorized_user_file('app/main/config/google/API/token.json', SCOPES)
    # ---

    # Get token.json from Secret Manager
    creds = Credentials.from_authorized_user_info(json.loads(get_secret(CLIENT, PROJECT_ID, TOK_SECRET_ID)), SCOPES)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError as re:
                logger.error("Credentials could not be refreshed, possibly the authorization was revoked by the user.")
                # uncomment if local token.json
                # os.unlink('token.json')
                CLIENT.delete_secret(request={"name": TOK_SECRET_ID})
                return
        else:
            # Uncomment this line if using local credentials.json
            # flow = InstalledAppFlow.from_client_secrets_file('app/main/config/google/API/credentials.json', SCOPES)

            flow = InstalledAppFlow.from_client_config(
                json.loads(get_secret(CLIENT, PROJECT_ID, CRE_SECRET_ID)),
                SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.json file for the next run

        # Uncomment this section if using local token.json
        # ---
        # with open('app/main/config/google/API/token.json', 'w') as token:
        #     token.write(creds.to_json())
        # ---

        add_secret(CLIENT, PROJECT_ID, TOK_SECRET_ID, creds.to_json())

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    return service


def generate_gmail_query(sender, subject, key_words):
    inf_date = (date.today() - timedelta(10)).isoformat()
    sup_date = (date.today() + timedelta(10)).isoformat()
    # TODO : Comment 2 lines below in prod
    # inf_date = (date(2021, 10, 25) - timedelta(5)).isoformat()
    # sup_date = (date(2021, 10, 25) + timedelta(5)).isoformat()
    return f"from:({','.join(sender)}) subject:({','.join(subject)}) " + ','.join(
        key_words) + f" after:{inf_date} before:{sup_date}"


def get_html_body(payload: dict):
    # The Body of the message is in Encrypted format. So, we have to decode it.
    # Get the data and decode it with base 64 decoder.
    # parts = payload.get('parts')[0]
    data = payload['body']['data']
    data = data.replace("-", "+").replace("_", "/")
    decoded_data = base64.b64decode(data)

    # Now, the data obtained is in lxml. So, we will parse
    # it with BeautifulSoup library
    soup = BeautifulSoup(decoded_data, "lxml")
    paragraphs = soup.find_all("span")
    body = []
    for b in paragraphs:
        text = b.text.strip().split("\n")
        text = "\n".join(list(filter(None, text)))
        if text:
            body.append(text)
    body = list(dict.fromkeys(body))
    return body[1:5]


def get_mail_contents(service, sender, subject, key_words):
    received_date = ""
    query = generate_gmail_query(sender, subject, key_words)
    # request a list of all the messages
    result = service.users().messages().list(userId='me', maxResults=3, q=query, includeSpamTrash=True).execute()

    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')

    # messages is a list of dictionaries where each dictionary contains a message id.
    # logger.info()
    # iterate through all the messages
    try:
        gmail_list = []
        for msg in messages:
            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            # Use try-except to avoid any Errors
            try:
                # Get value of 'payload' from dictionary 'txt'
                payload = txt['payload']
                headers = payload['headers']
                body = get_html_body(payload)
                # Look for Subject and Sender Email in the headers
                for h in headers:
                    if h['name'] == 'Subject':
                        subject = h['value']
                    if h['name'] == 'From':
                        sender = h['value']
                    if h['name'] == 'Date':
                        received_date = h['value']

                content = "\n".join(body)

                # Printing the subject, sender's email and message
                logger.info(f"Subject: {subject}")
                logger.info(f"From: {sender}")
                logger.info(f"Date: {received_date}")
                logger.info(f"Content: {content}")
                gmail_data = GmailData(subject, sender, received_date, content)
                gmail_list.append(gmail_data)
            except RuntimeError as re:
                logger.error(f"Error while getting email content : {re}")
        return gmail_list
    except TypeError as te:
        logger.error(f"Error while getting emails : {te}")
        return ""
