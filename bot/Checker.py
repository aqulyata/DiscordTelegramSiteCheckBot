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
        if self.t1 is not None and self.t1.is_alive() and not self.url_repo.get_state():
            return False
        self.t1 = threading.Thread(target=lambda: self.check(send_func), args=())
        self.t1.start()
        return True

    def check(self, send_func):
        while self.url_repo.get_state():
            elements = self.monitoring_urls.check()
            for check in elements:
                if check.new_status.value != check.old_status:
                    self.url_repo.update_status(check.url, check.new_status.value, int(check.data))
                    time_of = check.data - check.last_time
                    if check.new_status == SiteState.READY:
                        send_func(f'🟢{check.url} {self.encoder.encod(time_of)}🟢')
                    elif check.new_status == SiteState.NOT_READY:
                        send_func(f'🔴{check.url} {self.encoder.encod(time_of)} ERROR = {check.status_code}🔴')
            time.sleep(300)

    def fast_check(self):
            results = []
            for resource in self.url_repo.all_info():
                url = resource[0]
                old_status = resource[1]
                last_time = resource[2]
                try:
                    r = requests.get(url, timeout=2)
                    status_code = r.status_code
                except Exception:
                    status_code = -1
                new_status = SiteState.READY if status_code == 200 else SiteState.NOT_READY
                data = time.time()
                if new_status.value != old_status:
                    self.url_repo.update_status(url, new_status.value, int(data))
                if new_status == SiteState.READY:
                    time_of = data - last_time
                    results.append(f'🟢{url} {self.encoder.encod(time_of)}🟢')
                elif new_status == SiteState.NOT_READY:
                    time_of = data - last_time
                    emoji = '🟠' if status_code == -1 else '🔴'
                    results.append(f'{emoji}{url} {self.encoder.encod(time_of)} ERROR = {status_code}{emoji}')
                if len(results) != 0:
                    results = '\n'.join(results)
                    return results