from dataclasses import dataclass

from DiscordTelegramSiteCheckBot.command.enums.SiteState import SiteState


@dataclass
class CheckResult():
    url: str

    data: float
    last_time: int

    status_code: int
    new_status: SiteState
    old_status: SiteState
