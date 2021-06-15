from bot.command.base.Command import Command
from bot.DbManager import UrlsBdRepository
from bot.command.utils.MonitoringUtils import MonitoringUrl
from bot.command.utils.EncodingTime import EncoderTime


class Info(Command):
    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.encoder = EncoderTime()
        self.monitoring_urls = MonitoringUrl(url_repo)

    async def execute(self, send_func, args: [str]):
        await send_func(f'```{self.monitoring_urls.check()}```')

    def get_name(self):
        return 'info'