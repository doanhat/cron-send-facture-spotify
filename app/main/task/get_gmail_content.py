# import the required libraries
import logging
from datetime import date, timedelta

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s',
                    datefmt='%d-%b-%Y %H:%M:%S')
logger = logging.getLogger()

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_google_service():
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists('app/main/config/google/API/token.pickle'):
        # Read the token from the file and store it in the variable creds
        with open('app/main/config/google/API/token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('app/main/config/google/API/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('app/main/config/google/API/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    return service


def generate_gmail_query(sender, subject, words):
    inf_date = (date.today() - timedelta(5)).isoformat()
    sup_date = (date.today() + timedelta(5)).isoformat()
    # TODO : Comment 2 lines below in prod
    # inf_date = (date(2021, 10, 25) - timedelta(5)).isoformat()
    # sup_date = (date(2021, 10, 25) + timedelta(5)).isoformat()
    return f"from:({sender}) subject:({subject}) " + ', '.join(words) + f" after:{inf_date} before:{sup_date}"


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
    body = soup.body()
    return body


def send_message_fb(content):
    pass


def get_first_mail_content(service, sender, subject, words: list):
    received_date = ""
    query = generate_gmail_query(sender, subject, words)
    # request a list of all the messages
    result = service.users().messages().list(userId='me', maxResults=3, q=query, includeSpamTrash=True).execute()

    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')

    # messages is a list of dictionaries where each dictionary contains a message id.
    # logger.info()
    # iterate through all the messages
    try:
        for msg in messages:
            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            # Use try-except to avoid any Errors
            try:
                # Get value of 'payload' from dictionary 'txt'
                payload = txt['payload']
                headers = payload['headers']

                # Look for Subject and Sender Email in the headers
                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
                    if d['name'] == 'From':
                        sender = d['value']
                    if d['name'] == 'Date':
                        received_date = d['value']

                content = txt['snippet']

                # Printing the subject, sender's email and message
                logger.info(f"Subject: {subject}")
                logger.info(f"From: {sender}")
                logger.info(f"Date: {received_date}")
                logger.info(f"Content: {content}")
                return content
            except RuntimeError as re:
                logger.error(f"Error while getting email content : {re}")
    except TypeError as te:
        logger.error(f"Error while getting emails : {te}")
        return ""
