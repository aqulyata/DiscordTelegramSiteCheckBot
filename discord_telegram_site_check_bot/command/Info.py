from discord_telegram_site_check_bot.Checker import Checker
from discord_telegram_site_check_bot.DbManager import UrlsBdRepository
from discord_telegram_site_check_bot.command.base.Command import Command


class Info(Command):
    def __init__(self, url_repo: UrlsBdRepository, prefix) -> None:
        super().__init__()
        self.prefix = prefix
        self.result = []
        self.chekcer = Checker(url_repo)

    def execute(self, send_func, args: [str]):
        send_func(f'```{self.chekcer.fast_check()}```')

    def get_name(self):
        return 'info'

    def get_help(self):
        return ("Show all url and states\n" +
                "Usage: `" + self.prefix + self.get_name() + "`")
