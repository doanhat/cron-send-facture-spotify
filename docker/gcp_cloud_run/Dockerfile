FROM python:3.8

RUN apt-get update

WORKDIR /usr/src
COPY ./requirements.txt ./requirements.txt
COPY ./app ./app

# Set up and activate virtual environment
ENV VIRTUAL_ENV "/usr/src/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"
RUN . $VIRTUAL_ENV/bin/activate && pip install --no-cache-dir -r requirements.txt
RUN chmod +x app/main/script/run-app.sh

