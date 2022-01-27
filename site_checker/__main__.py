import asyncio
import os
import threading
import yaml
from telebot.types import Message

from discord_bot.DiscordBot import DiscordBot
from service.Checker import Checker
from service.DbManager import DbConnectionManager
from telegramm_bot.telegramm_bot import TelegramBot

if __name__ == '__main__':

    if os.stat("config.yaml").st_size != 0:
        with open('config.yaml') as f:  # открытие  yaml файла с входными данными
            data = yaml.load(f, Loader=yaml.FullLoader) # загрузка yaml файла
            prefix = data['prefix'] # получение префикса
            discord_white_list = data['discord_white_list'] # получение белого листа для дискорда
            telegramm_bot_white_list = data['telegramm_white_list'] # получение белого листа для телеграма
            tg_token = data['tg_token'] # получение токена для телеграма
            dis_token = data['discord_token'] # получение токена для дискорда
    else:
        raise Exception("File is empty")
    db_manager = DbConnectionManager() # создание экземпляра класса для работы с базой данных
    url_repo = db_manager.get_url_repository() # подключение к базе данных
    checker = Checker(url_repo) # создание publisher'a
    telegram_bot = TelegramBot(checker, tg_token, url_repo, prefix, telegramm_bot_white_list) # создание телеграм бота
    dis_bot = DiscordBot(prefix, discord_white_list, db_manager.get_url_repository(), checker)# создание дискорд бота
    checker.attach(dis_bot) # подписка на publisher'a для дискорд бота
    checker.attach(telegram_bot) # подписка на publisher'a для телеграм бота


    @telegram_bot.message_handler(func=lambda m: True) # параматер вытаскивания информации из сообщения
    def on_message(message: Message): # метод получения информации из сообщения
        if message.chat.id in telegramm_bot_white_list: # проверка на наличие пользователя в белом листе
            text = message.text # получение текста сообщения
            if not text.startswith(prefix): # проверка на наличия префикса в сообщении
                return
            text = text[len(prefix):] # перевод текста в удобную структуру данных
            splited_args = text.split()

            cmd = splited_args[0] # получение названия команды
            if cmd not in telegram_bot.commands: # проверка на наличие команды у бота
                return
            if len(splited_args) > 1: # проверка на непустое сообщение
                args = splited_args[1:] # удобное хранение информации из сообщения
            else:
                args = [] # иначе пустые аргументы
            telegram_bot.commands[cmd].execute(lambda msg: telegram_bot.send_message(message.chat.id, msg), args)
            # инициализация команд у телеграм бота
    on_message.__doc__ = 'принимает на вход сообщение и выполняет команду, указанную в тексте'
    # t2 = threading.Thread(target=lambda: )
    telegram_bot.polling(none_stop=True, interval=0, timeout=0)
    # t2.start()$
    # loop = asyncio.get_event_loop()
    # t1 = loop.create_task(dis_bot.run(dis_token))
    # loop.run_until_complete(t1)