import asyncio

import discord

from Observer import Observer
from discord_telegram_site_check_bot.command.base.Command import Command


class DiscordChecker(discord.Client, Observer):
    def __init__(self, prefix: str, white_list: [str]):
        super().__init__()
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
        print(check_res)
        # category = self.get_channel(859892547534585888)
        # channels = []
        # guild = self.get_guild(804421990508134430)
        # for channel in guild.channels:
        #     print(channel)
        #     channels.append(channel.id)
        # for check in check_res:
        #     if check.chnl_id not in channels:
        #         # if check.category not in channels:
        #         #     category = await guild.create_category("HandWriter", overwrites=None)
        #         #     self.url_repo.update_category(category.id)
        #         # else:
        #         #     category = self.discord_telegram_site_checker_bot.get_channel(check.category)
        #         chnl = await guild.create_text_channel(check.chnl_name, category=category)
        #         chnl_id = chnl.id
        #         self.url_repo.update_channel_id(chnl_id, check.chnl_name)
        #     else:
        #         if check.new_status.value != check.old_status:
        #             self.url_repo.update_status(check.url, check.new_status.value, int(check.data))
        #             if check.new_status == SiteState.READY:
        #                 time_of = check.data - check.last_time
        #                 chanel = self.bot.get_channel(check.chnl_id)
        #                 new_name = ('🟢' + check.chnl_name.upper() + '🟢')
        #                 await chanel.edit(name=new_name)
        #                 await chanel.send(f'```🟢{check.url} {self.encoder.encod(time_of)}🟢```')
        #                 print(f'```🟢{check.url} {self.encoder.encod(time_of)}🟢```')
        #                 continue
        #
        #             elif check.new_status == SiteState.NOT_READY:
        #                 chanel = self.bot.get_channel(check.chnl_id)
        #                 emoji = '🟠' if check.status_code == -1 else '🔴'
        #                 new_name = (emoji + check.chnl_name.upper() + emoji)
        #                 await chanel.edit(name=new_name)
        #                 time_of = check.data - check.last_time
        #                 await chanel.send(
        #                     f'```{emoji}{check.url} {self.encoder.encod(time_of)} ERROR = {check.status_code}{emoji}```')
        #                 print(
        #                     f'```🔴{check.url} {self.encoder.encod(time_of)} ERROR = {check.status_code}🔴```')

    def get_tuple(self):
        return self.commands

    def register_command(self, command: Command):
        self.commands[command.get_name()] = command
