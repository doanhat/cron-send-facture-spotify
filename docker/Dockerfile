FROM python:3.7.2

WORKDIR /usr/src

RUN apt-get update

RUN apt-get install -y --no-install-recommends python3-dev gcc libldap2-dev libssl-dev libsasl2-dev

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

ENV PYTHONPATH "${PYTHONPATH}:`pwd`"

#RUN chmod +x app/test/cron/test-cron.sh
RUN chmod +x app/main/cron/send-facture-spotify.sh

#CMD ["./app/test/cron/test-cron.sh"]
CMD ["python","app/main/send_facture.py"]
