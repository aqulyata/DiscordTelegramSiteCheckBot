import discord

from bot.Checker import Checker
from bot.DbManager import DbConnectionManager
from bot.command.Add import Add
from bot.command.Delete import Delete
from bot.command.Help import Help
from bot.command.Info import Info
from bot.command.Start import Start
from bot.command.Stop import Stop
from bot.command.base.Command import Command
from config import settings

prefix = (settings['prefix'])


class DiscordChecker(discord.Client):
    def __init__(self):
        super().__init__()
        self.commands = {}

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        text = message.content

        if not text.startswith(prefix):
            return
        text = text[len(prefix):]
        splited_args = text.split()
        cmd = text.split()[0]

        if cmd not in self.commands:
            return
        if len(splited_args) > 1:
            args = splited_args[1:]
        else:
            args = []

        await self.commands[cmd].execute(lambda msg: message.channel.send(msg), args)

    def register_command(self, command: Command):
        self.commands[command.get_name()] = command


db_manager = DbConnectionManager()
checker = Checker(db_manager.get_url_repository())
bot = DiscordChecker()

bot.register_command(Delete(db_manager.get_url_repository()))
bot.register_command(Add(db_manager.get_url_repository()))
bot.register_command(Info(db_manager.get_url_repository()))
bot.register_command(Help())
bot.register_command(Start(db_manager.get_url_repository(), checker))
bot.register_command(Stop(db_manager.get_url_repository()))

bot.run(settings['token'])


