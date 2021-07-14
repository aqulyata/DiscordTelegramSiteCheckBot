class Command:

    def __init__(self, prefix: str) -> None:
        super().__init__()
        self.prefix = prefix

    def execute(self, send_func, args: [str]):
        ...

    def get_name(self):
        ...
