import asyncio
import threading

import discord

from Observer import Observer
from discord_telegram_site_check_bot.DbManager import UrlsBdRepository
from discord_telegram_site_check_bot.command.base.Command import Command


class DiscordChecker(discord.Client, Observer):
    def __init__(self, prefix: str, white_list: [str], url_repo: UrlsBdRepository):
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.white_list = white_list
        self.commands = {}
        self.prefix = prefix

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if message.author.id in self.white_list:

            text = message.content

            if not text.startswith(self.prefix):
                return
            text = text[len(self.prefix):]
            splited_args = text.split()
            cmd = text.split()[0]

            if cmd not in self.commands:
                return
            if len(splited_args) > 1:
                args = splited_args[1:]
            else:
                args = []
            loop = asyncio.get_event_loop()

            def test(msg, embed=None):
                loop.create_task(message.channel.send(msg, embed=embed))

            if self.commands[cmd].execute is not None:
                self.commands[cmd].execute(test, args)

    def update(self, check_res):
        loop = asyncio.get_running_loop()
        self.t1 = threading.Thread(target=lambda: loop.create_task(self.checking(check_res)), args=())
        self.t1.start()
        print(check_res)

    async def checking(self, check_res):
        category = self.get_channel(859892547534585888)
        channels = []
        guild = self.get_guild(804421990508134430)
        for channel in guild.channels:
            print(channel)
            channels.append(channel.id)
        for check in check_res:
            if check.chnl_id not in channels:
                chnl = await guild.create_text_channel(check.chnl_name, category=category)
                self.url_repo.update_channel_id(chnl.id, check.chnl_name)
            else:
                chanel = self.get_channel(check.chnl_id)
                new_name = ('🟢' + check.chnl_name.upper() + '🟢') if check.status_code == 200 else (
                        '🔴' + check.chnl_name.upper() + '🔴')
                await chanel.edit(name=new_name)
                await chanel.send(f'```🟢{check.url} {check.time_of}🟢```') if check.status_code == 200 else (
                    f'```🔴{check.url} {check.time_of} ERROR = {check.status_code}🔴```')
                print(f'```🟢{check.url} {check.time_of}🟢```')

    def get_tuple(self):
        return self.commands

    def register_command(self, command: Command):
        self.commands[command.get_name()] = command
