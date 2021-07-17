from dataclasses import dataclass

from command.enums.SiteState import SiteState


@dataclass
class CheckResult():
    url: str

    time_of: int

    status_code: int
    new_status: SiteState
    old_status: SiteState

    chnl_id: int
    chnl_name: str
    category: int
