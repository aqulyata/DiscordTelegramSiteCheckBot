from bot.Checker import Checker
from bot.command.base.Command import Command
from bot.DbManager import UrlsBdRepository


class Info(Command):
    def __init__(self, url_repo: UrlsBdRepository, prefix) -> None:
        super().__init__(prefix)
        self.chekcer = Checker(url_repo)
        self.result = []

    def execute(self, send_func, args: [str]):
        send_func(f'{self.chekcer.fast_check()}')

    def get_name(self):
        return 'info'
