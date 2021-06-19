import discord

from bot.command.base.Command import Command


class Help(Command):

    def __init__(self, commands, prefix) -> None:
        super().__init__()
        self.embed = discord.Embed(colour=discord.Colour.from_rgb(106, 192, 245))
        self.commands = commands
        self.prefix = prefix

    def execute(self, send_func, args: [str]):
        self.embed.add_field(name="developed by aqulasoft.com",
                             value="https://github.com/aqulyata/DiscordTelegramSiteCheckBot",
                             inline=False, )
        for key in self.commands:
            self.embed.add_field(name=self.commands[key].get_name(), value=self.commands[key].get_help(),
                                 inline=False)
        print(self.embed)
        send_func(None, self.embed)
        self.embed.clear_fields()

    def get_name(self):
        return 'help'

    def get_help(self):
        return ("Show all commands\n" +
                "Usage: `" + self.prefix + self.get_name() + "`")
