from bot.command.base.Command import Command


class Help(Command):
    async def execute(self, send_func, args: [str]):
        await send_func(f'**```1) Command Add: insert $add + url \n '
                        f'2)Command delete: insert $delete(shows all url), insert $delete (nunmber of resource) \n '
                        f'3) Command info: shows all urls , their status and time of status \n'
                        f'4)Command start: starting auto process of checking resources\n'
                        f'5)Command stop: stopped process of checking resources```** ')

    def get_name(self):
        return 'help'
