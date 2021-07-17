import asyncio

import discord_bot

from discord_bot.command.base.Command import Command


class Help(Command):

    def __init__(self, commands, prefix) -> None:
        super().__init__()
        self.commands = commands
        self.prefix = prefix

    def execute(self, send_func, args: [str]):
        embed = discord_bot.Embed(colour=discord_bot.Colour.from_rgb(106, 192, 245))
        embed.add_field(name="developed by aqulasoft.com",
                        value="https://github.com/aqulyata/DiscordTelegramSiteCheckBot",
                        inline=False, )
        for key in self.commands:
            embed.add_field(name=self.commands[key].get_name(), value=self.commands[key].get_help(),
                            inline=False)
        embed.description = "test"

        send_func(None, embed)

    def get_name(self):
        return 'help'

    def get_help(self):
        return ("Show all commands\n" +
                "Usage: `" + self.prefix + self.get_name() + "`")
