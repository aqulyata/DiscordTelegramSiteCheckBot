import threading
import time

import discord
import requests

from bot.DbManager import UrlsBdRepository
from bot.command.utils.MonitoringUtils import MonitoringUrl
from bot.command.utils.EncodingTime import EncoderTime


class Checker:
    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.t1 = None
        self.encoder = EncoderTime()
        self.monitoring_urls = MonitoringUrl(url_repo)
        self.bot = None
        self.guild = None
        self.chnls = {}

    #
    # def start(self, send_func):
    #     if self.t1 is not None and self.t1.is_alive():
    #         return False
    #     self.t1 = threading.Thread(target=lambda: self.check(send_func), args=())
    #     self.t1.start()
    #     return True

    # async def recreate_channel(self):
    #     for resource in self.url_repo.all_info():
    #         chnl_name = resource[1]
    #         url = resource[0]
    #         if not chnl_name in self.guild.channels:
    #             self.chnls[url] = await self.guild.create_text_channel(chnl_name)

    async def check(self):
        for resource in self.url_repo.all_info():
            chnl_name = resource[3]
            url = resource[0]
            if not chnl_name in self.guild.channels:
                self.chnls[url] = await self.guild.create_text_channel(chnl_name)
        while self.url_repo.get_state():
            # guild.id = 804421990508134430
            guild = self.bot.get_guild(804421990508134430)

            for resource in self.url_repo.all_info():
                # print(f"{resource[0]} {resource[3]}")
                url = resource[0]
                chnl_name = resource[3]
                state = resource[1]
                last_time = resource[2]
                channel = discord.TextChannel
                if chnl_name in self.chnls:
                    try:
                        r = requests.head(url, timeout=2)
                        status_code = r.status_code
                    except Exception:
                        status_code = -1

                    uptime = resource[4]
                    new_state = 1 if r.status_code == 200 else 0
                    if new_state != state:
                        # downtime = resource[4]
                        # print(uptime - downtime)
                        self.url_repo.update_status(new_state, url)
                        data = time.time()
                        if new_state == 1:

                            time_of = data - last_time
                            print(f"TRUE  {url} ")
                            new_name = (f'🟢{chnl_name}🟢')
                            await channel.edit(name=new_name)
                            self.url_repo.update_chnl_name(new_name, url)
                            await channel.send(f'*``` {self.encoder.encod(time_of)} ```*')

                        else:
                            time_of = data - last_time
                            print(f"NONE  {url} ")
                            new_name = (f'🔴{chnl_name}🔴')
                            await channel.edit(name=new_name)
                            self.url_repo.update_chnl_name(new_name,url)
                            await channel.send(f'*``` {self.encoder.encod(time_of)} ```*')

                            # state = str(status_code)
                            # await channel.send(f'*```{url} FALL, TIME = {time_of_work} ERROR = {state}```*')
        pass

    # def check(self, send_func):
    #
    #     while self.url_repo.get_state():
    # for resource in self.url_repo.all_info():
    #     url = resource[0]
    #     status = resource[1]
    #     # send_func(f'```{self.monitoring_urls.check()}```')
    #     for elements in self.monitoring_urls.check():
    #         element = elements.split()
    #         if element[2] == '🟢':
    #             state = 1
    #         else:
    #             state = 0
    #         # elif element[2] == '🔴':
    #         #     state = 0
    #         if status != state:
    #             if status == 1:
    #                 element.pop(1)
    #                 print(f'```🟢{self.monitoring_urls.check()}🟢```')
    #             else:
    #                 element.pop(1)
    #                 print(f'```🔴{self.monitoring_urls.check()}🔴```')
    # for i in self.monitoring_urls.check():
    # splites
    #     splites_res = i.split()
    #     data = splites_res.pop(2)
    #     time_of = self.encoder.encod(float(data))
    #     splites_res.append(time_of)
