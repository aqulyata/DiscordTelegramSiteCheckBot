from service.Checker import Checker
from service.DbManager import UrlsBdRepository
from command.base.Command import Command


class Info(Command):  # опсиание класса получения информации о ресурсе
    def __init__(self, url_repo: UrlsBdRepository, prefix) -> None:  # конструктора
        super().__init__()
        self.prefix = prefix  # префикс
        self.result = []  # массив резьултата
        self.chekcer = Checker(url_repo)  # сервис проверки

    def execute(self, send_func, args: [str]):
        send_func(f'```{self.chekcer.fast_check()}```')
        # отправление результата

    def get_name(self):  # получение названия команды
        return 'info'

    def get_help(self): # получение информации о команде
        return ("Show all url and states\n" +
                "Usage: `" + self.prefix + self.get_name() + "`")
