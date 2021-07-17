from DbManager import UrlsBdRepository
from command.enums.SiteState import SiteState
from command.base.Command import Command
import requests


class Stats(Command):
    def __init__(self, url_repo: UrlsBdRepository) -> None:
        super().__init__()
        self.url_repo: UrlsBdRepository = url_repo

    def execute(self, send_func, split_msg):

        for i in self.url_repo.all_info():
            current_url = i[0]
            r = requests.get(current_url)
            new_state = SiteState.READY if r.status_code == 200 else SiteState.NOT_READY
            if new_state == SiteState.READY:
                send_func(f'{current_url} WORK ')
            else:
                status = str(r.status_code)
                send_func(f'{current_url} FALL,  ERROR = {status}')

    def get_name(self):
        return 'stat'