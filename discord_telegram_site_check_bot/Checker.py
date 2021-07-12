import asyncio
import threading
import time

from discord_telegram_site_check_bot.DbManager import UrlsBdRepository
from discord_telegram_site_check_bot.command.enums.SiteState import SiteState
from discord_telegram_site_check_bot.command.utils.EncodingTime import EncoderTime

class Checker:

    def __init__(self, url_repo: UrlsBdRepository, bot) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.t1 = None
        self.encoder = EncoderTime()
        self.bot = bot

    def start(self, time_of_checking):
        if self.t1 is not None and self.t1.is_alive():
            return False
        loop = asyncio.get_running_loop()

        self.t1 = threading.Thread(target=lambda: loop.create_task(self.check(time_of_checking)), args=())
        self.t1.start()
        return True

    async def check(self, time_of_checking):
        print("ITS COMMAND check")
        category = self.bot.get_channel(859892547534585888)
        while self.url_repo.get_state():
            print("CHECKING")
            channels = []
            guild = self.bot.get_guild(804421990508134430)
            for channel in guild.channels:
                print(channel)
                channels.append(channel.id)
            elements = self.bot.update()
            for check in elements:
                if check.chnl_id not in channels:
                    # if check.category not in channels:
                    #     category = await guild.create_category("HandWriter", overwrites=None)
                    #     self.url_repo.update_category(category.id)
                    # else:
                    #     category = self.discord_telegram_site_checker_bot.get_channel(check.category)
                    chnl = await guild.create_text_channel(check.chnl_name, category=category)
                    chnl_id = chnl.id
                    self.url_repo.update_channel_id(chnl_id, check.chnl_name)
                else:
                    if check.new_status.value != check.old_status:
                        self.url_repo.update_status(check.url, check.new_status.value, int(check.data))
                        if check.new_status == SiteState.READY:
                            time_of = check.data - check.last_time
                            chanel = self.bot.get_channel(check.chnl_id)
                            new_name = ('🟢' + check.chnl_name.upper() + '🟢')
                            await chanel.edit(name=new_name)
                            await chanel.send(f'```🟢{check.url} {self.encoder.encod(time_of)}🟢```')
                            print(f'```🟢{check.url} {self.encoder.encod(time_of)}🟢```')
                            continue

                        elif check.new_status == SiteState.NOT_READY:
                            chanel = self.bot.get_channel(check.chnl_id)
                            emoji = '🟠' if check.status_code == -1 else '🔴'
                            new_name = (emoji + check.chnl_name.upper() + emoji)
                            await chanel.edit(name=new_name)
                            time_of = check.data - check.last_time
                            await chanel.send(
                                f'```{emoji}{check.url} {self.encoder.encod(time_of)} ERROR = {check.status_code}{emoji}```')
                            print(
                                f'```🔴{check.url} {self.encoder.encod(time_of)} ERROR = {check.status_code}🔴```')
            print("ITS END OF COMMAND CHECK")
            time.sleep(int(time_of_checking))
