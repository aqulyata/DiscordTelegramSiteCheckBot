import discord

from command.base.Command import Command


class Help(Command): # класс описания всех команд

    def __init__(self, commands, prefix) -> None: # конструктор
        super().__init__()
        self.commands = commands # словарь команд
        self.prefix = prefix # префикс

    def execute(self, send_func, args: [str]):
        embed = discord.Embed(colour=discord.Colour.from_rgb(106, 192, 245)) # инициализация embed
        embed.add_field(name="developed by aqulasoft.com",
                        value="https://github.com/aqulyata/DiscordTelegramSiteCheckBot",
                        inline=False, ) # заполнение заголовка embed'a
        for key in self.commands: # проход по элементу в словаре
            embed.add_field(name=self.commands[key].get_name(), value=self.commands[key].get_help(),
                            inline=False) # заполнение основного тела embed'a
        embed.description = "Please, wait" # текст при ожидании загрузки embed'a

        send_func(None, embed) # отправка embed'a

    def get_name(self): # получение названия команды
        return 'help'

    def get_help(self): # получение информации о команде
        return ("Show all commands\n" +
                "Usage: `" + self.prefix + self.get_name() + "`")
