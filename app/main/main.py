import os
from datetime import datetime, timedelta

from app.main.helper.logger import logger
from app.main.task.get_gmail_content import get_first_mail_content, get_google_service
from app.main.task.send_message_fb import send_msg_to_thread
from flask import Flask

app = Flask(__name__)


@app.route("/")
def send_receipt():
    tomorrow_timestamp = datetime.today() - timedelta(hours=1) + timedelta(days=1)
    logger.debug(tomorrow_timestamp)
    if tomorrow_timestamp.day:
        content = get_first_mail_content(get_google_service(), 'no-reply@spotify.com', 'reçu', ['TVA', 'Total', 'reçu'])
        if content:
            message = f"Facture Spotify : {content} - Message automatique"
            send_msg_to_thread(message)
            return message
        else:
            return "No receipt"
    else:
        return "Not until 01 !"


if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
