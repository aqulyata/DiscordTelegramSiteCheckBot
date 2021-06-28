from dataclasses import dataclass

from discord_telegram_site_check_bot.command.enums.SiteState import SiteState


@dataclass
class CheckResult():
    url: str

    data: float
    last_time: int

    status_code: int
    new_status: SiteState
    old_status: SiteState
