class Command:

    def execute(self, send_func, args: [str]):
        ...

    def get_name(self):
        ...

    def get_help(self):
        ...
