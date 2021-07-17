from telebot import AsyncTeleBot

from DbManager import UrlsBdRepository
from Observer import Observer
from command.Add import Add
from command.Delete import Delete
from command.Help import Help
from command.Info import Info
from command.Start import Start
from command.Stop import Stop
from command.base.Command import Command



class TelegramBot(AsyncTeleBot, Observer):

    def __init__(self, checker, token: str, url_repo: UrlsBdRepository,prefix, white_list):
        super().__init__(token=token)
        self.commands = {}
        self.checker = checker
        self.checker = checker
        self.prefix = prefix
        self.white_list = white_list
        self.register_command(Info(url_repo, prefix))
        self.register_command(Delete(url_repo, prefix, self))
        self.register_command(Add(url_repo, prefix))
        self.register_command(Start(url_repo, self.checker, prefix))
        self.register_command(Stop(url_repo, self.checker, prefix))
        self.register_command(Help(url_repo, prefix))

    def register_command(self, command: Command):
        self.commands[command.get_name()] = command

    def update(self, check_res, loop = None):
        print(check_res)


