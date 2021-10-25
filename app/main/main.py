import sys

path_list = [
    '/Users/ndoan/PersoProj/automatically-send-facture-spotify/app',
    '/Users/ndoan/PersoProj/automatically-send-facture-spotify',
    '/Applications/PyCharm.app/Contents/plugins/python/helpers/pycharm_matplotlib_backend',
    '/Applications/PyCharm.app/Contents/plugins/python/helpers/pycharm_display'
]

for p in path_list:
    if p not in sys.path:
        sys.path.append(p)

from app.main.get_gmail_content import get_first_mail_content, get_google_service
from app.main.send_message_fb import send_msg_to_group, get_client, thread_id, send_msg_to_user

content = get_first_mail_content(get_google_service(), 'no-reply@spotify.com', 'reçu', ['TVA', 'Total', 'reçu'])
message = f"Facture Spotify : {content} - Message automatique"
send_msg_to_group(get_client(), thread_id, message)
