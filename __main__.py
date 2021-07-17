import os

import yaml

from Checker import Checker
from DbManager import DbConnectionManager
from discord_bot.DiscordBot import DiscordBot
from telegramm_bot.telegramm_bot import TelegramBot

if __name__ == '__main__':
    if os.stat("config.yaml").st_size != 0:
        with open('config.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            prefix = data['prefix']
            dis_token = data['token'][:-1]
            white_list = data['white_list']
            tg_token = data['tg_token']
    else:
        raise Exception("File is empty")
    db_manager = DbConnectionManager()
    url_repo = db_manager.get_url_repository()
    checker = Checker(url_repo)
    telegram_bot = TelegramBot(checker, tg_token, url_repo, prefix)
    dis_bot = DiscordBot(prefix, white_list, db_manager.get_url_repository(), checker)
    checker.attach(dis_bot)
    dis_bot.run(dis_token)
