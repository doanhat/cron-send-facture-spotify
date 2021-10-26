from datetime import datetime
import os

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s',
                    datefmt='%d-%b-%Y %H:%M:%S')
logger = logging.getLogger()


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
    logging.info(f"Current Time = {current_time}")
    return data


write_file('app/test/cron/test.txt', print_time())
