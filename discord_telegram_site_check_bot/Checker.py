import threading
import time
from typing import List

import requests

from Observer import Observer
from discord_telegram_site_check_bot.DbManager import UrlsBdRepository
from discord_telegram_site_check_bot.command.enums.SiteState import SiteState
from discord_telegram_site_check_bot.command.utils.EncodingTime import EncoderTime
from discord_telegram_site_check_bot.command.utils.dataclasses.CheckResult import CheckResult
from discord_telegram_site_check_bot.publisher import Publisher


class Checker(Publisher):

    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.t1 = None
        self.encoder = EncoderTime()

    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        print("SUBJECT attached on observer")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, check_res) -> None:
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(check_res)

    def start(self, time_of_checking):
        if self.t1 is not None and self.t1.is_alive():
            return False
        self.t1 = threading.Thread(target=lambda: (self.check(time_of_checking)), args=())
        self.t1.start()
        return True

    def check(self, time_of_checking: int):
        while self.url_repo.get_state():

            for resource in self.url_repo.all_info():
                url = resource[0]
                old_status = resource[1]
                last_time = resource[2]
                chnl_id = resource[3]
                chnl_name = resource[4]
                category = resource[5]
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
                        check_res = CheckResult(url, time_of, status_code, new_status, old_status, chnl_id, chnl_name,
                                                category)
                        self.notify(check_res)
                    elif new_status == SiteState.NOT_READY:
                        time_of = data - last_time
                        check_res = CheckResult(url, time_of, status_code, new_status, old_status, chnl_id, chnl_name,
                                                category)
                        self.notify(check_res)

        time.sleep(time_of_checking)

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
