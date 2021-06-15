class Command:

    async def execute(self, send_func, args: [str]):
        ...

    def get_name(self):
        ...
