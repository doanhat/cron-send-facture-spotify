FROM python:3.8

RUN apt-get update

WORKDIR /usr/src
COPY ./requirements.txt ./requirements.txt
COPY ./app ./app
COPY ./env ./env

# Set up and activate virtual environment
ENV PORT "8080"
ENV VIRTUAL_ENV "/usr/src/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"
RUN . $VIRTUAL_ENV/bin/activate && pip install --no-cache-dir -r requirements.txt
RUN chmod +x app/main/cron/send-facture-spotify.sh

CMD ["./app/main/cron/send-facture-spotify.sh"]
