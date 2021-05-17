FROM python:3-alpine

LABEL name="hqtrackbot"
LABEL repository="https://github.com/ScottBrenner/hqtrackbot"
LABEL homepage="https://github.com/ScottBrenner/hqtrackbot"
LABEL org.opencontainers.image.source="https://github.com/ScottBrenner/hqtrackbot"

LABEL "maintainer"="Scott Brenner <scott@scottbrenner.me>"

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY hqtrackbot.py ./
COPY youtube.py ./

CMD [ "python", "-u", "./hqtrackbot.py" ]