import os

import yaml

from discord_bot.Checker import Checker
from discord_bot.DbManager import DbConnectionManager
from discord_bot.DiscordBot import DiscordBot

if __name__ == '__main__':
    if os.stat("config.yaml").st_size != 0:
        with open('config.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            prefix = data['prefix']
            token = data['token'][:-1]
            white_list = data['white_list']
    else:
        raise Exception("File is empty")
    db_manager = DbConnectionManager()
    url_repo = db_manager.get_url_repository()
    checker = Checker(url_repo)
    discord_bot = DiscordBot(prefix, white_list, db_manager.get_url_repository(), checker)
    checker.attach(discord_bot)
    discord_bot.run(token)
