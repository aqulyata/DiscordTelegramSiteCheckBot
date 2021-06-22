import asyncio
import threading
import time

from bot.DbManager import UrlsBdRepository
from bot.command.enums.SiteState import SiteState
from bot.command.utils.EncodingTime import EncoderTime
from bot.command.utils.MonitoringUtils import MonitoringUrl


class Checker:
    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.t1 = None
        self.encoder = EncoderTime()
        self.monitoring_urls = MonitoringUrl(url_repo)

    def start(self, send_func):
        if self.t1 is not None and self.t1.is_alive():
            return

        loop = asyncio.get_running_loop()

        self.t1 = threading.Thread(target=lambda: loop.create_task(self.check(send_func)), args=())
        self.t1.start()
        return True

    async def check(self, send_func):
        while self.url_repo.get_state():
            elements = self.monitoring_urls.check()
            for check in elements:
                if check.new_status.value != check.old_status:
                    self.url_repo.update_status(check.url, check.new_status.value, int(check.data))
                    if check.new_status == SiteState.READY:
                        time_of = check.data - check.last_time
                        await send_func(f'```🟢{check.url} {self.encoder.encod(time_of)}🟢```')
                        print(f'```🟢{check.url} {self.encoder.encod(time_of)}🟢```')

                    else:
                        time_of = check.data - check.last_time
                        await send_func(f'```🟢{check.url} {self.encoder.encod(time_of)}🟢```')
                        print(f'```🔴{check.url} {self.encoder.encod(time_of)} ERROR = {check.status_code}🔴```')
            time.sleep(300)
