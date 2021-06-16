import asyncio
import concurrent.futures

from bot.command.base.Command import Command
from bot.DbManager import UrlsBdRepository
from bot.command.utils.MonitoringUtils import MonitoringUrl
from bot.command.utils.EncodingTime import EncoderTime


class Info(Command):
    def __init__(self, url_repo: UrlsBdRepository, prefix) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.encoder = EncoderTime()
        self.monitoring_urls = MonitoringUrl(url_repo)
        self.prefix = prefix

    async def execute(self, send_func, args: [str]):
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(
                pool, self.monitoring_urls.check)
            # for i in result:
            #     splites_res = i.split()
            #     data = splites_res.pop(2)
            #     time_of = self.encoder.encod(float(data))
            #     splites_res.append(time_of)
            if len(result) != 0:

                result = '\n'.join(result)
                await send_func(f'```{result}```')

    def get_name(self):
        return 'info'

    def get_help(self):
        return ("Show all url and states\n" +
                "Usage: `" + self.prefix + self.get_name() + "`")
