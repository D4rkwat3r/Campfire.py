from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json
from dataclasses_json import LetterCase
from dataclasses_json import config
from .account_effect import AccountEffect


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Account:
    sponsor: int
    level: int = field(metadata=config(field_name="J_LVL"))
    last_online_date: int = field(metadata=config(field_name="J_LAST_ONLINE_DATE"))
    id: int = field(metadata=config(field_name="J_ID"))
    sponsor_times: int
    name: str = field(metadata=config(field_name="J_NAME"))
    date_create: int = field(metadata=config(field_name="J_DATE_CREATE"))
    sex: int
    karma30: int
    image_id: int = field(metadata=config(field_name="J_IMAGE_ID"))
    account_effects: list[AccountEffect]
