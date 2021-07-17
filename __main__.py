import os

import yaml

from discord_site_check_bot.Checker import Checker
from discord_site_check_bot.DbManager import DbConnectionManager
from discord_site_check_bot.DiscordChecker import DiscordChecker

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
    bot = DiscordChecker(prefix, white_list, db_manager.get_url_repository())
    checker = Checker(url_repo)
    checker.attach(bot)
    bot.run(token)
