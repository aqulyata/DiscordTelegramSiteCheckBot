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

        elements = self.monitoring_urls.check()
        if elements[1].value != elements[5]:
            self.url_repo.update_status(elements[3], elements[1].value, elements[0])
        time_of = elements[0] - elements[4]
        if elements[1] == SiteState.READY:
            msg = (f'```🟢{elements[3]}  {self.encoder.encod(time_of)}🟢 ```')
            self.result.append(msg)
        else:
            msg = (f'```🔴 {elements[3]} {self.encoder.encod(time_of)} ERROR = {elements[2]}🔴```')
            self.result.append(msg)
        if len(self.result) != 0:
            result = '\n'.join(self.result)
            await send_func(result)

    def get_name(self):
        return 'info'

    def get_help(self):
        return ("Show all url and states\n" +
                "Usage: `" + self.prefix + self.get_name() + "`")
