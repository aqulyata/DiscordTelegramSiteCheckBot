import os
import yaml
from telebot import AsyncTeleBot
from telebot.types import Message
from bot.Checker import Checker
from bot.DbManager import DbConnectionManager
from bot.command.Add import Add
from bot.command.Delete import Delete
from bot.command.Help import Help
from bot.command.Info import Info
from bot.command.Start import Start
from bot.command.Stop import Stop
from bot.command.base.Command import Command
from Observer import Observer
from bot.SpeedBot import TelegramBot

if __name__ == '__main__':
    if os.stat("users.yaml").st_size != 0:
        with open('users.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            prefix = data['prefix']
            token = data['token']
            users_id = data['white_list_ids']
    else:
        raise Exception("File is empty")

    db_manager = DbConnectionManager()

    checker = Checker(db_manager.get_url_repository())
    bot = TelegramBot(checker, token)
    bot.register_command(Delete(db_manager.get_url_repository(), prefix))
    bot.register_command(Add(db_manager.get_url_repository(), prefix))
    bot.register_command(Info(db_manager.get_url_repository(), prefix))
    bot.register_command(Help(prefix))
    bot.register_command(Start(db_manager.get_url_repository(), checker, prefix))
    bot.register_command(Stop(db_manager.get_url_repository(), prefix))


@bot.message_handler(func=lambda m: True)
def on_message(message: Message):
    if str(message.chat.id) in users_id:
        text = message.text
        if not text.startswith(prefix):
            return
        text = text[len(prefix):]

        splited_args = text.split()
        cmd = splited_args[0]
        if cmd not in bot.commands:
            return
        if len(splited_args) > 1:
            args = splited_args[1:]
        else:
            args = []
        bot.commands[cmd].execute(lambda msg: bot.send_message(message.chat.id, msg), args)

bot.polling(none_stop=True, interval=0, timeout=0)
