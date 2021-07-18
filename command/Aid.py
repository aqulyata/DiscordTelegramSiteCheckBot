from command.base.Command import Command


class Aid(Command):

    def __init__(self, prefix, commands) -> None:
        super().__init__()
        self.prefix = prefix
        self.commands = commands

    def execute(self, send_func, args: [str]):
        result = []
        self.commands.get_help()
        send_func(result)


    def get_help(self):
        return ("Show all commands\n" +
                "Usage: `" + self.prefix + self.get_name() + "`")

    def get_name(self):
        return 'aid'
