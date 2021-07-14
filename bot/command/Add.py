import time
from bot.DbManager import UrlsBdRepository
from bot.command.base.Command import Command
from bot.command.enums.SiteState import SiteState


class Add(Command):

    def __init__(self, url_repo: UrlsBdRepository, prefix) -> None:
        super().__init__(prefix)
        self.url_repo: UrlsBdRepository = url_repo

    def execute(self, send_func, args: [str]):
        if len(args) == 1:
            if self.url_repo.check_and_recording_url_in_db(args[0], SiteState.UNDEFINDED.value, time.time()):
                send_func("Добавлено!")
            else:
                send_func("Уже добавлено.")

        elif len(args) != 1:
            send_func('Извините, вы неправильно указали параметры!')

    def get_name(self):
        return 'add'
