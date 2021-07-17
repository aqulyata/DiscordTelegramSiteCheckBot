import time

from DbManager import UrlsBdRepository
from command.base.Command import Command
from command.enums.SiteState import SiteState


class Add(Command):

    def __init__(self, url_repo: UrlsBdRepository, prefix) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.prefix = prefix

    def execute(self, send_func, args: [str]):
        if len(args) == 2:
            if self.url_repo.check_and_recording_url_in_db(args[0], SiteState.UNDEFINDED.value, time.time(), 0, args[1],
                                                           0):
                send_func("```Добавлено!```")
            else:
                send_func("```Уже добавлено```")

        elif len(args) == 0 or 1:
            send_func('```Вы забыли указать параметр```')
        else:
            send_func('```Извините, вы указали лишний  параметр```')

    def get_name(self):
        return 'add'

    def get_help(self):
        return ("Add url\n" +
                "Usage: `" + self.prefix + self.get_name() + " <url + channel_name>`")
