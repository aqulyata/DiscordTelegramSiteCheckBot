import threading

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
            return False
        self.send_func = send_func
        self.t1 = threading.Thread(target=self.check, args=())
        self.t1.start()
        return True

    # async def execute_thread(self, executor, send_func):
    #     loop = asyncio.get_event_loop()
    #     await loop.run_in_executor(executor, self.check(send_func), loop)

    def check(self):
        while self.url_repo.get_state():
            elements = self.monitoring_urls.check()
            for check in elements:
                if check.new_status.value != check.old_status:
                    self.url_repo.update_status(check.url, check.new_status.value, int(check.data))
                    if check.new_status == SiteState.READY:
                        time_of = check.data - check.last_time
                        self.send_func(f'```🟢{check.url} {self.encoder.encod(time_of)}🟢```')
                        print(f'```🟢{check.url} {self.encoder.encod(time_of)}🟢```')

                    else:
                        time_of = check.data - check.last_time
                        self.send_func(f'```🟢{check.url} {self.encoder.encod(time_of)}🟢```')
                        print(f'```🔴{check.url} {self.encoder.encod(time_of)} ERROR = {check.status_code}🔴```')
