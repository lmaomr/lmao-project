from dataclasses import dataclass, field
from typing import List

@dataclass
class Ticket:
    from_station : str = ""
    to_station : str = ""
    travel_date : str = ""
    train_types: List[str] = field(default_factory=list)
    allow_transfer : bool = False