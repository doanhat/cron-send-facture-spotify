from datetime import datetime
import os

from app.main.helper.logger import logger


def write_file(filename, data):
    if os.path.isfile(filename):
        with open(filename, 'a') as f:
            f.write('\n' + data)
    else:
        with open(filename, 'w') as f:
            f.write(data)


def print_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    data = "Current Time = " + current_time
    logger.info(f"Current Time = {current_time}")
    return data


write_file('app/test/cron/test.txt', print_time())
