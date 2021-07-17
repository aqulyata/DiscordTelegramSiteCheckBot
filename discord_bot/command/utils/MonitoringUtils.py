import time
from typing import List

import requests

from discord_bot.DbManager import UrlsBdRepository
from discord_bot.command.enums.SiteState import SiteState
from discord_bot.command.utils.dataclasses.CheckResult import CheckResult
from Publisher import Observer
from Publisher import Publisher


class MonitoringUrl(Publisher):

    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo

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

    def check(self):
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
                    check_res = CheckResult(url, time_of, status_code, new_status, old_status, chnl_id, chnl_name,category)
                    self.notify(check_res)
                elif new_status == SiteState.NOT_READY:
                    time_of = data - last_time
                    check_res = CheckResult(url, time_of, status_code, new_status, old_status, chnl_id, chnl_name, category)
                    self.notify(check_res)
