from bot.DbManager import UrlsBdRepository
from bot.command.base.Command import Command
from bot.command.enums.SiteState import SiteState
from bot.command.utils.EncodingTime import EncoderTime
from bot.command.utils.MonitoringUtils import MonitoringUrl


class Info(Command):
    def __init__(self, url_repo: UrlsBdRepository, prefix) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.encoder = EncoderTime()
        self.monitoring_urls = MonitoringUrl(url_repo)
        self.prefix = prefix
        self.result = []

    async def execute(self, send_func, args: [str]):
        results = []
        elements = self.monitoring_urls.check()
        for result in elements:
            if result[1].value != result[5]:
                self.url_repo.update_status(result[3], result[1].value, int(result[0]))
            if result[1] == SiteState.READY:
                time_of = result[0] - result[4]
                results.append(f'🟢{result[3]} {self.encoder.encod(time_of)}🟢')
            if result[1] == SiteState.NOT_READY:
                time_of = result[0] - result[4]
                results.append(f'🔴{result[3]} {self.encoder.encod(time_of)} ERROR = {result[2]}🔴')
        if len(results) != 0:
            results = '\n'.join(results)
            await send_func(f'```{results}```')

    def get_name(self):
        return 'info'

    def get_help(self):
        return ("Show all url and states\n" +
                "Usage: `" + self.prefix + self.get_name() + "`")
