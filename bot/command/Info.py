from bot.command.base.Command import Command
from bot.DbManager import UrlsBdRepository
import requests
import time

from bot.command.enums.SiteState import SiteState
from bot.command.utils.EncodingTime import EncoderTime


class Info(Command):
    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.encoder = EncoderTime()
        # self.result = []

    async def execute(self, send_func, args: [str]):
        for resource in self.url_repo.all_info():
            url = resource[0]
            old_status = resource[1]
            last_time = resource[2]
            result = []
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
                # await send_func(f'```{url} WORK  IN SEC {time_of}```')
                result.append(f'{url} WORK IN {self.encoder.encod(time_of)}')
            else:
                # await send_func(f'```{url} FALL, TIME = {time_of} ERROR = {status_code}```')
                result.append(f'{url} FALL IN {self.encoder.encod(time_of)} ERROR = {status_code}')

            if len(result) != 0:
                result = '\n'.join(result)
                await send_func(f'``` {result}```')

    def get_name(self):
        return 'info'
