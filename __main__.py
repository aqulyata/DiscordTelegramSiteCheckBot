import os

import yaml
from telebot.types import Message

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
            discord_white_list = data['discord_white_list']
            telegramm_bot_white_list = data['telegramm_white_list']
            tg_token = data['tg_token']
    else:
        raise Exception("File is empty")
    db_manager = DbConnectionManager()
    url_repo = db_manager.get_url_repository()
    checker = Checker(url_repo)
    telegram_bot = TelegramBot(checker, tg_token, url_repo, prefix, telegramm_bot_white_list)
    dis_bot = DiscordBot(prefix, discord_white_list, db_manager.get_url_repository(), checker)
    checker.attach(dis_bot)
    checker.attach(telegram_bot)


    @telegram_bot.message_handler(func=lambda m: True)
    def on_message(message: Message):
        if message.chat.id in telegramm_bot_white_list:
            text = message.text
            if not text.startswith(prefix):
                return
            text = text[len(prefix):]

            splited_args = text.split()
            cmd = splited_args[0]
            if cmd not in telegram_bot.commands:
                return
            if len(splited_args) > 1:
                args = splited_args[1:]
            else:
                args = []
            telegram_bot.commands[cmd].execute(lambda msg: telegram_bot.send_message(message.chat.id, msg), args)


    dis_bot.run(dis_token)
    telegram_bot.polling(none_stop=True, interval=0, timeout=0)
