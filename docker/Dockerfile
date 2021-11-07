FROM python:3.8

RUN apt-get update
RUN apt-get install -y cron

WORKDIR /usr/src
COPY ./requirements.txt ./requirements.txt
COPY ./app ./app
COPY ./env ./env

# Set up and activate virtual environment
ENV VIRTUAL_ENV "/usr/src/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"
RUN . $VIRTUAL_ENV/bin/activate && pip install --no-cache-dir -r requirements.txt
RUN chmod +x app/main/cron/send-receipt-spotify.sh

# Copy cron file to the cron.d directory
COPY ./cronjob/cron-send-facture-spotify /etc/cron.d/cron-send-facture-spotify
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron-send-receipt-spotify
# Apply cron job
RUN crontab /etc/cron.d/cron-send-receipt-spotify
# Create the log file to be able to run tail
RUN touch /var/log/cron.log
# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
