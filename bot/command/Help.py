from bot.command.base.Command import Command


class Help(Command):
    def execute(self, send_func, bot):
        send_func(
                        'Привет! Все команды которые есть: \n\n' +
                        'Info - по этой команде выводится список элементов + их статус и время работы.\n' +
                        'Add - добавление вашего url в список. \n' +
                        'Delete - удаление вашего url из списка.\n' +
                        'Start - по этой команде запускается непрерывная проверка url из списка и при смене статуса происходит рассылка.\n' +
                        'Stop - с помощью этой команды вы остановите непрерывную проверку url из списка.'
                )

    def get_name(self):
        return 'help'
