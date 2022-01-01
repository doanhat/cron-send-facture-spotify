import os
from datetime import datetime, timedelta

from flask import Flask, request

from app.main.helper.logger import logger
from app.main.task.get_gmail_content import get_mail_contents, get_google_service
from app.main.task.send_message_fb import send_msg_to_thread

app = Flask(__name__)


@app.route("/")
def send_receipt():
    args = request.args.to_dict(flat=False)
    logger.info("Begin app")
    logger.info(args)
    tomorrow_timestamp = datetime.today() - timedelta(hours=1) + timedelta(days=1)
    logger.info(f"Tomorrow : {tomorrow_timestamp}")
    if tomorrow_timestamp.day == 1:
        data = \
            get_mail_contents(get_google_service(), args.get('sender'), args.get('subject'), args.get('key_words'))
        logger.info(data)
        if data:
            data = data[0]
            message = f"Message automatique : " \
                      f"{data.subject} à {data.received_date} : " \
                      f"{data.sender} : " \
                      f"{data.content}"
            send_msg_to_thread(message)
            return message
        else:
            message = "No receipt"
            logger.info(message)
            return message
    else:
        message = "Tomorrow is not 1"
        logger.info(message)
        return message


if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
