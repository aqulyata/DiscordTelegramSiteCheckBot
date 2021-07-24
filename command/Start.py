from service.Checker import Checker
from service.DbManager import UrlsBdRepository
from command.base.Command import Command


class Start(Command):
    DEFAULT_SLEEP_TIME = 600

    def __init__(self, url_repo: UrlsBdRepository, checker: Checker, prefix) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.checker: Checker = checker
        self.prefix = prefix

    def execute(self, send_func, args: [str]):
        result = []

        if len(args) == 0:

            result.append('You forgot give argument time now its 10 min')
            time_of_checking = self.DEFAULT_SLEEP_TIME
        else:
            time_of_checking = args[0]
        self.url_repo.changing_state(True)
        if self.checker.start(time_of_checking):
            print("start")
            result.append('you have start the verification process!')
        else:
            print('started')
            result.append('Already launched!')
        if len(result) != 0:
            results = '\n'.join(result)
            send_func(f'```{results}```')

    def get_name(self):
        return 'start'

    def get_help(self):
        return ("Start process of checking with time\n" +
                "Usage:`" + self.prefix + self.get_name() + ' ' + "<time of checking>`")
