import threading
import time

from discord_telegram_site_check_bot.DbManager import UrlsBdRepository
from discord_telegram_site_check_bot.command.enums.SiteState import SiteState
from discord_telegram_site_check_bot.command.utils.EncodingTime import EncoderTime
from discord_telegram_site_check_bot.command.utils.MonitoringUtils import MonitoringUrl


class Checker:
    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.t1 = None
        self.encoder = EncoderTime()
        self.monitoring_urls = MonitoringUrl(url_repo)

    def start(self, send_func, time_of_checking:int):

        if self.t1 is not None and self.t1.is_alive():
            return False
        if self.url_repo.get_state():
            self.t1 = threading.Thread(target=lambda: self.check(send_func, time_of_checking), args=())
            self.t1.start()
            return True
        else:
            return False

    def check(self, send_func, time_of_checking):
        while self.url_repo.get_state():
            elements = self.monitoring_urls.check()
            for check in elements:
                if check.new_status.value != check.old_status:
                    self.url_repo.update_status(check.url, check.new_status.value, int(check.data))
                    time_of = check.data - check.last_time
                    if check.new_status == SiteState.READY:
                        send_func(f'🟢{check.url} {self.encoder.encod(time_of)}🟢')
                    else:
                        send_func(f'🔴{check.url} {self.encoder.encod(time_of)} ERROR = {check.status_code}🔴')

            time.sleep(time_of_checking)
