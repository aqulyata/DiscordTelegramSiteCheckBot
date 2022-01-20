import time

from service.DbManager import UrlsBdRepository
from command.base.Command import Command
from command.enums.SiteState import SiteState


# имопрт зависимотсей

class Add(Command): # описание класса команды на добавление

    def __init__(self, url_repo: UrlsBdRepository, prefix) -> None: # конструктор
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo # экземпляр класса для работы с бд
        self.prefix = prefix # префикс

    def execute(self, send_func, args: [str]): # основной метод отправки
        if len(args) == 2: # проверка на количество параметров в сообщение
            if self.url_repo.check_and_recording_url_in_db(args[0], SiteState.UNDEFINDED.value, time.time(), 0, args[1],0):
                # запись в базу данных
                send_func("```Added!```") # отправка сообщения об успешном добавлении
            else:
                send_func("```Already added```")
                # отправка сообщения об уже существующем в базе данных ресурсе

        elif len(args) == 0 or 1: # проверка на количество аргументов
            send_func('```Sorry, you forgot to specify the parameter```')
            # отправка сообщения о недостающем праметре
        else:
            send_func('```Sorry, you added an extra parameter```')
            # отправка сообщения о лишнем аргументе

    def get_name(self): # получение названия команды
        return 'add'

    def get_help(self): # получение информации о команде
        return ("Add url\n" +
                "Usage: `" + self.prefix + self.get_name() + " <url + channel_name>`")
