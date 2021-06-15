import threading
import time

from bot.DbManager import UrlsBdRepository
from bot.command.utils.AlwaysMonitornungUrls import AlwaysMonitoringUrl
from bot.command.utils.EncodingTime import EncoderTime


class Checker:
    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.t1 = None
        self.encoder = EncoderTime()
        self.always_monitoring_urls = AlwaysMonitoringUrl(url_repo)

    def start(self, send_func):
        if self.t1 is not None and self.t1.is_alive():
            return
        self.t1 = threading.Thread(target=lambda: self.check(send_func), args=())
        self.t1.start()

    def check(self, send_func):
        while self.url_repo.get_state():
            send_func(f'```{self.always_monitoring_urls.check()}```')
            print('start')
            time.sleep(10)