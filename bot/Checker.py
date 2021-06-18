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
        self.t1 = threading.Thread(target=lambda: self.check(send_func), args=())
        self.t1.start()
        return True
        # loop = asyncio.get_running_loop()
        # with concurrent.futures.ThreadPoolExecutor() as pool:
        #     result = await loop.run_in_executor(
        #         pool, self.check)
        # result()

    def check(self, send_func):

        while self.url_repo.get_state():
            for resource in self.url_repo.all_info():
                url = resource[0]
                status = resource[1]
                last_time = resource[2]
                elements = self.monitoring_urls.check()
                if elements[1].value != status:
                    self.url_repo.update_status(url, elements[1].value, elements[0])
                    time_of = elements[0] - last_time
                    if elements[1] == SiteState.READY:
                        send_func(f'{url} 🟢 {self.encoder.encod(time_of)} ')

                    else:
                        send_func(f'{url} 🔴 {self.encoder.encod(time_of)} ERROR = {elements[2]}')
