import time
import requests
from bot.DbManager import UrlsBdRepository
from bot.command.enums.SiteState import SiteState
from bot.command.utils.EncodingTime import EncoderTime


class MonitoringUrl():

    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.encoder = EncoderTime()
        self.result = []

    def check(self):
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
                msg = (f'{url} 🟢 {self.encoder.encod(time_of)} ')
                self.result.append(msg)
                continue
            elif new_status == SiteState.NOT_READY:
                resultat = (f'{url} 🔴 {self.encoder.encod(time_of)} ERROR = {status_code}')
                self.result.append(resultat)

            return (self.result)
            # if len(self.result) != 0:
            #     result = '\n'.join(self.result)
            #     return result
