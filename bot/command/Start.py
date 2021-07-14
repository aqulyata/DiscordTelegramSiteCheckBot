from bot.Checker import Checker
from bot.DbManager import UrlsBdRepository
from bot.command.base.Command import Command


class Start(Command):
    DEFAULT_SLEEP_TIME = 300

    def __init__(self, url_repo: UrlsBdRepository, checker: Checker, prefix) -> None:
        super().__init__(prefix)
        self.url_repo: UrlsBdRepository = url_repo
        self.checker: Checker = checker
        self.prefix = prefix

    def execute(self, send_func, args: [str]):
        result = []
        if len(args) == 0:
            result.append('вы забыли указать время, будет стоять 5 минут')
            time_of_checking = self.DEFAULT_SLEEP_TIME
        else:
            time_of_checking = args[0]
        self.url_repo.changing_state(True)
        if self.checker.start(time_of_checking):
            result.append('Вы запустили процесс проверки!')
        else:
            result.append('Уже запущено!')
        if len(result) != 0:
            results = '\n'.join(result)
            send_func(f'{results}')

    def get_name(self):
        return 'start'

