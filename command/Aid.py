from command.base.Command import Command


class Aid(Command):

    def __init__(self, prefix) -> None:
        super().__init__()
        self.prefix = prefix

    def execute(self, send_func, args: [str]):
        send_func()

    def get_help(self):
        return ("Show all commands\n" +
                "Usage: `" + self.prefix + self.get_name() + "`")

    def get_name(self):
        return 'aid'
