FROM python:3.8-slim-buster

RUN mkdir -p /DiscordTelegramSiteCheckBot
WORKDIR /DiscordTelegramSiteCheckBot
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY config.yaml .

COPY . .

CMD [ "python3", "-m" , "DiscordTelegramSiteCheckBot"]