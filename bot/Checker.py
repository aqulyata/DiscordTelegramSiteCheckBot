import threading
import time

from bot.DbManager import UrlsBdRepository
from bot.command.utils.MonitoringUtils import MonitoringUrl
from bot.command.utils.EncodingTime import EncoderTime


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

        while self.url_repo.get_state():
            for resource in self.url_repo.all_info():
                url = resource[0]
                status = resource[1]
                # send_func(f'```{self.monitoring_urls.check()}```')
                for elements in self.monitoring_urls.check():
                    element = elements.split()
                    if element[2] == '🟢':
                        state = 1
                    else:
                        state = 0
                    # elif element[2] == '🔴':
                    #     state = 0
                    if status != state:
                        if status == 1:
                            element.pop(1)
                            print(f'```🟢{self.monitoring_urls.check()}🟢```')
                        else:
                            element.pop(1)
                            print(f'```🔴{self.monitoring_urls.check()}🔴```')
            # for i in self.monitoring_urls.check():
                # splites
        #     splites_res = i.split()
        #     data = splites_res.pop(2)
        #     time_of = self.encoder.encod(float(data))
        #     splites_res.append(time_of)