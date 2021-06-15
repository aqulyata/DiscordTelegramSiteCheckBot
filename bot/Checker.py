import threading
import time

import requests
from bot.DbManager import UrlsBdRepository
from bot.command.enums.SiteState import SiteState
from bot.command.utils.EncodingTime import EncoderTime


class Checker:
    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.t1 = None
        self.encoder = EncoderTime()

    def start(self, send_func):
        if self.t1 is not None and self.t1.is_alive():
            return
        self.t1 = threading.Thread(target=lambda: self.check(send_func), args=())
        self.t1.start()

    def check(self, send_func):
        while self.url_repo.get_state():
            print('start checking')
            for resource in self.url_repo.all_info():
                url = resource[0]
                old_status = resource[1]
                last_time = resource[2]
                try:
                    r = requests.head(url, timeout=2)
                    status_code = r.status_code
                except Exception:
                    status_code = -1
                new_status = SiteState.READY if status_code == 200 else SiteState.NOT_READY

                data = time.time()
                if new_status.value != old_status:
                    self.url_repo.update_status(url, new_status.value, int(data))

                    time_of = data - last_time
                    if new_status == SiteState.READY:
                        send_func(f'```{url} WORK IN  {self.encoder.encod(time_of)}```')
                    else:
                        send_func(f'```{url} FALL IN {self.encoder.encod(time_of)} ERROR = {status_code}```')
            time.sleep(1)
        print('stop checking')
