from bot.DbManager import UrlsBdRepository
from bot.command.base.Command import Command


class Stop(Command):
    def __init__(self, url_repo: UrlsBdRepository, prefix) -> None:
        super().__init__(prefix)
        self.url_repo: UrlsBdRepository = url_repo

    def execute(self, send_func, split_msg):
        self.url_repo.changing_state(False)
        send_func('Вы остановили процесс проверки!')

    def get_name(self):
        return 'stop'
