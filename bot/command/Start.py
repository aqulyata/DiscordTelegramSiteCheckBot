from bot.Checker import Checker
from bot.DbManager import UrlsBdRepository
from bot.command.base.Command import Command


class Start(Command):
    def __init__(self, url_repo: UrlsBdRepository, checker: Checker, prefix) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.checker: Checker = checker
        self.prefix = prefix

    async def execute(self, send_func, split_msg):
        self.url_repo.changing_state(True)
        await self.checker.check()
        await send_func('```Вы запустили процесс проверки!```')
        # else:
        #     await send_func('```Уже запущено!```')

    def get_name(self):
        return 'start'

    def get_help(self):
        return ("Start process of checking\n" +
                "Usage: `" + self.prefix + self.get_name() + "`")