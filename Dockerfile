FROM python:slim
RUN useradd parking
WORKDIR /parking


COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY parking.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP parking.py

RUN chown -R parking:parking ./
USER parking

ENTRYPOINT ["./boot.sh"]
