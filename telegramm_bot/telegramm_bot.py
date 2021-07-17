from telebot import AsyncTeleBot
from bot.Checker import Checker
from bot.command.base.Command import Command
from Observer import Observer


class TelegramBot(AsyncTeleBot, Observer):

    def __init__(self, checker: Checker, token: str):
        super().__init__(token=token)
        self.commands = {}
        self.checker = checker

    def register_command(self, command: Command):
        self.commands[command.get_name()] = command

    def update(self, check_res):
        ...