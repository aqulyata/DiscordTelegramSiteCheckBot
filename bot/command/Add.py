import time

from bot.DbManager import UrlsBdRepository
from bot.command.base.Command import Command
from bot.command.enums.SiteState import SiteState


class Add(Command):

    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo

    async def execute(self, send_func, args:[str]):
        if len(args) == 1:
            url = args[0]
            status = SiteState.UNDEFINDED.value
            data = time.time()
            if self.url_repo.check_and_recording_url_in_db(url, status, data):
                await send_func("```Добавлено!```")
            else:
                await send_func("```Уже добавлено```")

        else:
            await send_func('```Вы забыли указать параметр```')

    def get_name(self):
        return 'add'