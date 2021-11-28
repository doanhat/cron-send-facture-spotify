import os

from app.main.task.get_gmail_content import get_first_mail_content, get_google_service
from app.main.task.send_message_fb import send_msg_to_thread

if os.getenv("PORT") == "8080":
    content = get_first_mail_content(get_google_service(), 'no-reply@spotify.com', 'reçu', ['TVA', 'Total', 'reçu'])
    if content:
        message = f"Facture Spotify : {content} - Message automatique"
        send_msg_to_thread(message)
