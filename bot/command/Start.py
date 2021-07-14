from bot.Checker import Checker
from bot.DbManager import UrlsBdRepository
from bot.command.base.Command import Command


class Start(Command):
    def __init__(self, url_repo: UrlsBdRepository, checker: Checker, prefix) -> None:
        super().__init__(prefix)
        self.url_repo: UrlsBdRepository = url_repo
        self.checker: Checker = checker

    def execute(self, send_func, split_msg):
        self.url_repo.changing_state(True)
        if self.checker.start(send_func):
            send_func('Вы запустили процесс проверки!')
        else:
            send_func('Уже запущено!')

    def get_name(self):
        return 'start'

