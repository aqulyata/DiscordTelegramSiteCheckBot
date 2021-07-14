import time
import requests
from bot.DbManager import UrlsBdRepository
from bot.command.enums.SiteState import SiteState
from bot.command.utils.EncodingTime import EncoderTime
from bot.command.utils.dataclasses.CheckResult import CheckResult
from bot.Publisher import Publisher
from bot.Publisher import Observer
from typing import List

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
            observer.update()
            return check_res

    def check(self):
        result = []
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
            check_res = CheckResult(url, data, last_time, status_code, new_status, old_status)
            result.append(check_res)
        return result
