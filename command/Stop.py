from service.Checker import Checker
from service.DbManager import UrlsBdRepository
from command.base.Command import Command


class Stop(Command): # описание команды остановки процесса
    def __init__(self, url_repo: UrlsBdRepository, prefix: str) -> None: # конструктор
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo # экземпляр класса для работы в базе данных
        self.prefix = prefix

    def execute(self, send_func, split_msg):
        self.url_repo.changing_state(False) # смена статуса
        print('stopped')
        send_func('```you have stopped the verification process!```')
        # отправка информации

    def get_name(self): # получение названия команды
        return 'stop'

    def get_help(self): # описание информации о команде
        return ("Stop process of checking\n" +
                "Usage: `" + self.prefix + self.get_name() + "`")
