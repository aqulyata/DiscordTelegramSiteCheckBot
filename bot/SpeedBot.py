import discord
import yaml
from bot.Checker import Checker
from bot.DbManager import DbConnectionManager
from bot.command.Add import Add
from bot.command.Delete import Delete
# from bot.command.Help import Help
from bot.command.Info import Info
from bot.command.Start import Start
from bot.command.Stop import Stop
from bot.command.base.Command import Command


class DiscordChecker(discord.Client):
    def __init__(self, prefix: str):
        super().__init__()
        self.commands = {}
        self.prefix = prefix
        self.embed = discord.Embed()

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        self.embed.add_field(name="developed by aqulasoft.com", value="https://github.com/aqulasoft/DisYam",
                             inline=False)
        text = message.content

        if not text.startswith(self.prefix):
            return
        text = text[len(self.prefix):]
        splited_args = text.split()
        cmd = text.split()[0]
        if cmd == 'help':
            await message.channel.send(embed=self.embed)

        if cmd not in self.commands:
            return
        if len(splited_args) > 1:
            args = splited_args[1:]
        else:
            args = []
        await self.commands[cmd].execute(lambda msg: message.channel.send(msg), args)
        # async def execute_thread(self, executor, send_func):
        #     loop = asyncio.get_event_loop()
        #     await loop.run_in_executor(executor, self.check(send_func), loop)

    def register_command(self, command: Command):
        self.commands[command.get_name()] = command


if __name__ == '__main__':
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        prefix = data['prefix']
        token = data['token']

    db_manager = DbConnectionManager()
    checker = Checker(db_manager.get_url_repository())
    bot = DiscordChecker(prefix)
    bot.register_command(Delete(db_manager.get_url_repository(), prefix))
    bot.register_command(Add(db_manager.get_url_repository(), prefix))
    bot.register_command(Info(db_manager.get_url_repository(), prefix))
    # bot.register_command(Help())
    bot.register_command(Start(db_manager.get_url_repository(), checker, prefix))
    bot.register_command(Stop(db_manager.get_url_repository(), prefix))

    bot.run(token)
# todo проверка на наличиче префикса и наличиче самого файла yaml
