from discord_telegram_site_check_bot.Checker import Checker
from discord_telegram_site_check_bot.DbManager import UrlsBdRepository
from discord_telegram_site_check_bot.command.base.Command import Command


class Start(Command):

    DEFAULT_SLEEP_TIME = 600

    def __init__(self, url_repo: UrlsBdRepository, checker: Checker, prefix) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.checker: Checker = checker
        self.prefix = prefix

    def execute(self, send_func, args: [str]):
        if len(args) == 0:
            send_func('``` You forgot give argument time now its 10 min ```')
            time_of_checking = self.DEFAULT_SLEEP_TIME
        else:
            time_of_checking = args[0]
        self.url_repo.changing_state(True)
        if self.checker.start(send_func, time_of_checking):
            send_func('```Вы запустили процесс проверки!```')
        else:
            send_func('```Уже запущено!```')

    def get_name(self):
        return 'start'

    def get_help(self):
        return ("Start process of checking with time\n" +
                "Usage: `" + self.prefix + self.get_name() + "<time of checking>")
