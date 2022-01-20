from service.DbManager import UrlsBdRepository
from command.base.Command import Command


# импорт зависимотсей

class Delete(Command):  # описания класса удаляющий элемент

    def __init__(self, url_repo, prefix, bot) -> None:  # конструктор
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo  # получение экземпляра класса для работы с бд
        self.prefix = prefix  # префикс
        self.result = []  # массив результата
        self.t2 = None # создание пустого потока
        self.bot = bot # тип бота

    def execute(self, send_func, args: [str]):
        result = [] # динамиеский массив резултатов
        if len(args) == 1: # проверка на количестово аргументов
            number_1 = int(args[0]) # получение позиции удаляемого элемента
            number = number_1 - 1 # получние индекса
            # channel = self.bot.get_channel(self.url_repo.get_certain_record(number))
            # await channel.delete()
            if self.url_repo.delete_element_in_db(number): # удаление элемента из бд
                send_func('```Deleted!```')
            else:
                send_func('```There is no such element```')
        else:
            for element in self.url_repo.all_urls(): # проход каждого элемента из бд
                result.append(str(element)) # добавление элемента в  массив
            if len(result) != 0: # проверка на ненулевой результат
                result = '\n'.join(result) # форматирование результата
                send_func(f'```{result}```') # отправка результата

    def get_name(self): # получение названия комнады
        return 'delete'

    def get_help(self): # получение информации о команде
        return ("Delete url\n" +
                "Usage: `" + self.prefix + self.get_name() + " <url>`")
