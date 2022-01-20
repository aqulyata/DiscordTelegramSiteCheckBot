from service.Checker import Checker
from service.DbManager import UrlsBdRepository
from command.base.Command import Command


class Start(Command): # класс запуска проверки
    DEFAULT_SLEEP_TIME = 600 # время проверки по стандарту

    def __init__(self, url_repo: UrlsBdRepository, checker: Checker, prefix) -> None: # конструктор
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo # база данных
        self.checker: Checker = checker # сервис проверки
        self.prefix = prefix # префикс

    def execute(self, send_func, args: [str]):
        result = [] # массив результата

        if len(args) == 0: # проверка на наличие аргумента

            result.append('You forgot give argument time now its 10 min') # добавление информации в результат
            time_of_checking = self.DEFAULT_SLEEP_TIME # время проверки
        else:
            time_of_checking = args[0] # запись времени проверки
        self.url_repo.changing_state(True) # смена статуса
        if self.checker.start(time_of_checking): # запуск проверки
            print("start")
            result.append('you have start the verification process!')
            # добавление информации в результат
        else:
            print('started')
            result.append('Already launched!')
            # добалвение информации в результат
        if len(result) != 0: # проверка на содержание результата
            results = '\n'.join(result) # форматирование результата
            send_func(f'```{results}```') # отправление результата

    def get_name(self): # получение названия команды
        return 'start'

    def get_help(self): # получние информации о команде
        return ("Start process of checking with time\n" +
                "Usage:`" + self.prefix + self.get_name() + ' ' + "<time of checking>`")
