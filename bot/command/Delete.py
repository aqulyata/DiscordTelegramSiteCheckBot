from bot.command.base.Command import Command
from bot.DbManager import UrlsBdRepository


class Delete(Command):

    def __init__(self, url_repo,prefix) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo
        self.prefix = prefix
    async def execute(self, send_func, args: [str]):
        if len(args) == 1:
            number_1 = int(args[0])
            number = number_1 - 1
            if self.url_repo.delete_element_in_db(number):
                await send_func('```Удалено!```')
            else:
                await send_func('```Такого элемента нет```')
        else:

            await send_func(f'```{self.url_repo.all_urls()}```')

    def get_name(self):
        return 'delete'

    def get_help(self):
        return ("Delete url\n" +
                "Usage: `" + self.prefix + self.get_name() + " <url>`")
