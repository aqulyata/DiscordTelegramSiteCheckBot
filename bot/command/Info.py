from bot.command.base.Command import Command
from bot.DbManager import UrlsBdRepository
from bot.command.enums.SiteState import SiteState

from bot.command.utils.EncodingTime import EncoderTime
from bot.command.utils.MonitoringUtils import MonitoringUrl


class Info(Command):
    def __init__(self, url_repo: UrlsBdRepository, prefix) -> None:
        super().__init__(prefix)
        self.url_repo: UrlsBdRepository = url_repo
        self.encoder = EncoderTime()
        self.monitoring_urls = MonitoringUrl(url_repo)
        self.result = []

    def execute(self, send_func, args: [str]):
        results = []
        elements = self.monitoring_urls.check()
        for check in elements:
            if check.new_status != check.old_status:
                self.url_repo.update_status(check.url, check.new_status.value, int(check.data))
            time_of = check.data - check.last_time
            if check.new_status == SiteState.READY:
                results.append(f'🟢{check.url} {self.encoder.encod(time_of)}🟢')
            elif check.new_status == SiteState.NOT_READY:
                results.append(f'🔴{check.url} {self.encoder.encod(time_of)} ERROR = {check.status_code}🔴')
        if len(results) != 0:
            results = '\n'.join(results)
            send_func(f'{results}')

    def get_name(self):
        return 'info'
