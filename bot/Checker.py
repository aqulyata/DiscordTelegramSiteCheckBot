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

    def check(self, send_func):
        while True:
            elements = self.monitoring_urls.check()
            for result in elements:
                if result[1].value != result[5]:
                    self.url_repo.update_status(result[3], result[1].value, int(result[0]))
                    if result[1] == SiteState.READY:
                        time_of = result[0] - result[4]
                        print(f'```🟢{result[3]} {self.encoder.encod(time_of)}🟢```')

                    if result[1] == SiteState.NOT_READY:
                        time_of = result[0] - result[4]
                        print(f'```🔴{result[3]} {self.encoder.encod(time_of)} ERROR = {result[2]}🔴```')
