import asyncio
import os

import discord
import yaml

from DiscordTelegramSiteCheckBot.Checker import Checker
from DiscordTelegramSiteCheckBot.DbManager import DbConnectionManager
from DiscordTelegramSiteCheckBot.command.Add import Add
from DiscordTelegramSiteCheckBot.command.Delete import Delete
from DiscordTelegramSiteCheckBot.command.Help import Help
from DiscordTelegramSiteCheckBot.command.Info import Info
from DiscordTelegramSiteCheckBot.command.Start import Start
from DiscordTelegramSiteCheckBot.command.Stop import Stop
from DiscordTelegramSiteCheckBot.command.base.Command import Command


class DiscordChecker(discord.Client):
    def __init__(self, prefix: str, checker: Checker, white_list: [str]):
        super().__init__()
        self.white_list = white_list
        self.commands = {}
        self.prefix = prefix
        # self.embed = discord.Embed(colour=discord.Colour.from_rgb(106, 192, 245))
        self.checker = checker

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if str(message.author.id) in self.white_list:

            text = message.content

            if not text.startswith(self.prefix):
                return
            text = text[len(self.prefix):]
            splited_args = text.split()
            cmd = text.split()[0]

            if cmd not in self.commands:
                return
            if len(splited_args) > 1:
                args = splited_args[1:]
            else:
                args = []
            loop = asyncio.get_event_loop()

            def test(msg, embed=None):
                loop.create_task(message.channel.send(msg, embed=embed))

            if self.commands[cmd].execute is not None:
                self.commands[cmd].execute(test, args)

    def get_tuple(self):
        return self.commands

    def register_command(self, command: Command):
        self.commands[command.get_name()] = command


if __name__ == '__main__':

    if os.stat("config.yaml").st_size != 0:
        with open('config.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            prefix = data['prefix']
            token = data['token']
            del token[-2]
            white_list = data['white_list'].split('+')
    else:
        raise Exception("File is empty")
    db_manager = DbConnectionManager()
    checker = Checker(db_manager.get_url_repository())
    bot = DiscordChecker(prefix, checker, white_list)
    bot.register_command(Delete(db_manager.get_url_repository(), prefix))
    bot.register_command(Add(db_manager.get_url_repository(), prefix))
    bot.register_command(Info(db_manager.get_url_repository(), prefix))
    bot.register_command(Start(db_manager.get_url_repository(), checker, prefix))
    bot.register_command(Stop(db_manager.get_url_repository(), checker, prefix))
    bot.register_command(Help(bot.get_tuple(), prefix))
    bot.run(token)


# todo white list
