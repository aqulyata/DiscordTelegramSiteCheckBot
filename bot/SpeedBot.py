import asyncio
import os

import discord
import yaml

from bot.Checker import Checker
from bot.DbManager import DbConnectionManager
from bot.command.Add import Add
from bot.command.Delete import Delete
from bot.command.Help import Help
from bot.command.Info import Info
from bot.command.Start import Start
from bot.command.Stop import Stop
from bot.command.base.Command import Command


class DiscordChecker(discord.Client):
    def __init__(self, prefix: str):
        super().__init__()
        self.commands = {}
        self.prefix = prefix
        # self.embed = discord.Embed(colour=discord.Colour.from_rgb(106, 192, 245))

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
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

        async def test(msg, embed=None):
            await message.channel.send(msg, embed=embed)

        if self.commands[cmd].execute is not None:
            await self.commands[cmd].execute(test, args)

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
    else:
        raise Exception("File is empty")
    db_manager = DbConnectionManager()
    bot = DiscordChecker(prefix)
    checker = Checker(db_manager.get_url_repository(), bot)
    bot.register_command(Delete(db_manager.get_url_repository(), prefix))
    bot.register_command(Add(db_manager.get_url_repository(), prefix))
    bot.register_command(Info(db_manager.get_url_repository(), prefix))
    bot.register_command(Start(db_manager.get_url_repository(), checker, prefix))
    bot.register_command(Stop(db_manager.get_url_repository(), prefix))
    bot.register_command(Help(bot.get_tuple(), prefix))
    bot.run(token)
