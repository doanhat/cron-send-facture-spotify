# Importing libraries
import imaplib, email
import os
from datetime import timedelta, date
from dotenv import load_dotenv
import logging
from bs4 import BeautifulSoup
import lxml
import unicodedata

load_dotenv()
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s',
                    datefmt='%d-%b-%Y %H:%M:%S')
logger = logging.getLogger()

user = os.getenv('USER_EMAIL_ADDRESS')
password = os.getenv('USER_PASSWORD')
imap_url = 'imap.gmail.com'


# Function to get email content part i.e its body part
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


# Function to search for a key value pair
def search(conn, sender, word):
    date_formatted = (date.today() - timedelta(1)).strftime("%d-%b-%Y")
    result, mail_data = conn.search(
        None,
        f'(SENTSINCE {date_formatted})',
        f'FROM {sender.strip()}',
        f'BODY {word.strip()}'
    )
    return mail_data


# Function to get the list of emails under this label
def get_emails(result_bytes):
    msgs = []  # all the email data are pushed inside an array
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, "(UID BODY[TEXT])")
        msgs.append(data)

    return msgs


def log_email(emails: list):
    for msg in emails[::-1]:
        for sent in msg:
            if type(sent) is tuple:
                # encoding set as utf-8
                content = str(sent[1], 'utf-8')
                data = str(content)
                email_message = email.message_from_string(content)
                logger.info(email_message)
                # Handling errors related to unicodenecode
                try:
                    indexstart = data.find("ltr")
                    data2 = data[indexstart + 5: len(data)]
                    indexend1 = data2.find("<!DOCTYPE html>")
                    indexend2 = data2.find("</html>")

                    # logging the required content which we need
                    # to extract from our email i.e our body
                    soup = BeautifulSoup(data2[indexend1:indexend2 + 7], "lxml")
                    text = soup.get_text()
                    text = text.strip()\
                        .replace("=E0", "à") \
                        .replace("=\r\n", "")\
                        .replace("=EA", "ê")\
                        .replace("=A0", " ")\
                        .replace("=C3=A7", "ç")\
                        .replace("=E2=82=AC", "€")\
                        .replace("=E9", "é")

                    logger.info(f"Data : {text}")  # get until last ">"

                except UnicodeEncodeError as e:
                    pass


# this is done to make SSL connection with GMAIL
con = imaplib.IMAP4_SSL(imap_url)

# logging the user in
con.login(user, password)

# calling function to check for email under this label
readonly = True
con.select('Inbox', readonly)

# fetching emails from this user "tu**h*****1@gmail.com"
msgs = get_emails(search(con, 'no-reply@spotify.com', 'Total'))

# Uncomment this to see what actually comes as data
# logger.info(msgs)

# Finding the required content from our msgs
# User can make custom changes in this part to
# fetch the required content he / she needs

# logging them by the order they are displayed in your gmail
log_email(msgs)
