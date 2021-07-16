import os

import yaml

from discord_telegram_site_check_bot.Checker import Checker
from discord_telegram_site_check_bot.DbManager import DbConnectionManager
from discord_telegram_site_check_bot.SpeedBot import DiscordChecker
from discord_telegram_site_check_bot.command.Add import Add
from discord_telegram_site_check_bot.command.Delete import Delete
from discord_telegram_site_check_bot.command.Help import Help
from discord_telegram_site_check_bot.command.Info import Info
from discord_telegram_site_check_bot.command.Start import Start
from discord_telegram_site_check_bot.command.Stop import Stop
from discord_telegram_site_check_bot.publisher import Publisher

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
    bot = DiscordChecker(prefix, white_list , db_manager.get_url_repository())
    checker = Checker(db_manager.get_url_repository())
    checker.attach(bot)
    bot.register_command(Delete(db_manager.get_url_repository(), prefix, bot))
    bot.register_command(Add(db_manager.get_url_repository(), prefix))
    bot.register_command(Info(db_manager.get_url_repository(), prefix))
    bot.register_command(Start(db_manager.get_url_repository(), checker, prefix))
    bot.register_command(Stop(db_manager.get_url_repository(), checker, prefix))
    bot.register_command(Help(bot.get_tuple(), prefix))
    bot.run(token)
