from bot.Checker import Checker
from bot.DbManager import UrlsBdRepository
from bot.command.base.Command import Command


class Start(Command):
    def __init__(self, url_repo: UrlsBdRepository, checker:Checker) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.checker: Checker = checker

    async def execute(self, send_func, split_msg):
        self.url_repo.changing_state(True)
        self.checker.start(send_func)
        await send_func('Вы запустили процесс проверки!')

    def get_name(self):
        return 'start'

