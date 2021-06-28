import time

import requests

from discord_telegram_site_check_bot.DbManager import UrlsBdRepository
from discord_telegram_site_check_bot.command.enums.SiteState import SiteState
from discord_telegram_site_check_bot.command.utils.EncodingTime import EncoderTime
from discord_telegram_site_check_bot.command.utils.dataclasses.CheckResult import CheckResult


class MonitoringUrl():

    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.encoder = EncoderTime()

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
