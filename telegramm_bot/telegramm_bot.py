from telebot import AsyncTeleBot

from service.DbManager import UrlsBdRepository
from service.Observer import Observer
from command.Add import Add
from command.Aid import Aid
from command.Delete import Delete
from command.Help import Help
from command.Info import Info
from command.Start import Start
from command.Stop import Stop
from command.base.Command import Command


# импорт зависимостей

class TelegramBot(AsyncTeleBot, Observer): # класс телеграм бота

    def __init__(self, checker, token: str, url_repo: UrlsBdRepository, prefix, white_list): # контсруктор
        super().__init__(token=token)
        self.commands = {} # словарь с наименованием команд
        self.checker = checker # сервис проверик
        self.prefix = prefix #  префикс
        self.white_list = white_list # белый лист
        self.register_command(Info(url_repo, prefix))
        self.register_command(Delete(url_repo, prefix, self))
        self.register_command(Add(url_repo, prefix))
        self.register_command(Start(url_repo, self.checker, prefix))
        self.register_command(Stop(url_repo, prefix))
        self.register_command(Help(url_repo, prefix))
        self.register_command(Aid(self.prefix, self.get_tuple()))
        # регистрация всех доступных команд

    def register_command(self, command: Command): # метод регистрации команд
        self.commands[command.get_name()] = command # добавление команд в словарь с командами

    def update(self, check_res, loop):
        print(check_res)

    def get_tuple(self): # получение команд
        return self.commands
