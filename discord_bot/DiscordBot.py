import asyncio

import discord

from service.Observer import Observer
from service.DbManager import UrlsBdRepository
from command.Add import Add
from command.Delete import Delete
from command.Help import Help
from command.Info import Info
from command.Start import Start
from command.Stop import Stop
from command.base.Command import Command


#  импортирование зависимостей

class DiscordBot(discord.Client, Observer):  # описание класс дискорд бота
    def __init__(self, prefix: str, white_list: [str], url_repo: UrlsBdRepository, checker):  # конструктор
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo  # экзепмляр класса для работы с базой данных
        self.white_list = white_list  # белый лист
        self.commands = {}  # словарь с командами
        self.prefix = prefix  # префикс
        self.guid = None  # уникальный id гильдии
        self.t2 = None  # уникальный поток
        self.checker = checker  # сервис
        self.register_command(Info(url_repo, prefix))
        self.register_command(Delete(url_repo, prefix, self))
        self.register_command(Add(url_repo, prefix))
        self.register_command(Start(url_repo, self.checker, prefix))
        self.register_command(Stop(url_repo, prefix))
        self.register_command(Help(self.commands, prefix))
        # регистрация команд

    async def on_ready(self):  # стратовый метод
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):  # метод получения сообщения
        if message.author == self.user:  # проверка на авторство от бота
            return
        if message.author.id in self.white_list:  # проверка на наличие пользователя в белом листе

            text = message.content  # получение текста сообщения
            self.guild = message.guild  # получение гильдии
            if not text.startswith(self.prefix):  # проверка на наличие префикса в сообщении
                return
            text = text[len(self.prefix):]  # получение аргументов из сообщения
            splited_args = text.split()  # перенос данных в другую структуру
            cmd = text.split()[0]  # получение названия команды

            if cmd not in self.commands:  # проверка на наличие команды в словаре
                return
            if len(splited_args) > 1:  # проверка на наличие аргументов
                args = splited_args[1:]
            else:
                args = []
            loop = asyncio.get_event_loop()  # поулчение loop'a

            def test(msg, embed=None):
                loop.create_task(message.channel.send(msg, embed=embed))  # создание таски

            if self.commands[cmd].execute is not None:  # 2 проверка на наличие команды в словаре
                self.commands[cmd].execute(test, args)  # исполнение команды

    def update(self, check_res, loop):  # обновление или создание нового потока
        if self.t2 is not None and self.t2.is_alive():  # проверка на наличие потока
            return
        loop.create_task(self.change_send_channels(check_res))  # создание таски

    async def change_send_channels(self, check_res):  # изменения информации при смене состояния
        name_of_category = "HandWriter"  # название категории в дискорде
        channels = []  # массив кканаплов
        result = []  # массив отправляемых данных
        channels_name = []  # массив названий каналов
        result.append(check_res)  # добавление информации в массив рещультата
        for channel in self.guild.channels:  # получение каждого канала на дискорд серве
            channels.append(channel.id)  # добавлнение id канала в  массив каналов
            channels_name.append(channel.name)  # добавление названия канала в массив с названиями каналов

        if name_of_category not in channels_name:  # проверка на наличие категории в гильдии

            category = await self.guild.create_category(name_of_category)  # создание новой категории
        else:
            category_obj = discord.utils.get(self.guild.channels, name=name_of_category)  # получение категории
            category = self.get_channel(category_obj.id)  # получение опредленного канала в категории
        for check in result:  # проход по кажому элементу в результате
            if check.chnl_id not in channels: # проверка на налиичие искомого канала на сервере
                chnl = await self.guild.create_text_channel(check.chnl_name, category=category) # создание нового текстового канала
                chanel = self.get_channel(chnl.id) # получение нового канала
                self.url_repo.update_channel_id(chnl.id, check.chnl_name) # обновление записей в базе данных о канале
            else:
                chanel = self.get_channel(check.chnl_id) # получение канал соответсвующий опредленному ресурсу

            new_name = ('🟢' + check.chnl_name.upper()) if check.status_code == 200 else (
                    '🔴' + check.chnl_name.upper()) # новое имя канала
            await chanel.edit(name=new_name) # изменение названия канала
            await chanel.send(f'```🟢{check.url} {check.time_of}🟢```') if check.status_code == 200 else (
                f'```🔴{check.url} {check.time_of} ERROR = {check.status_code}🔴```') # отправление информации о ресурсе на опрделенный  канала
            print(f'```🟢{check.url} {check.time_of}🟢```') # консольный вывод информации о ресурсе

    def get_tuple(self): # получении словаря с командами
        return self.commands # возврат словаря с командами

    def register_command(self, command: Command): # регистрация команд
        self.commands[command.get_name()] = command # занесение названия команды в словарь
