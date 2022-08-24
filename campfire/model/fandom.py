from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json
from dataclasses_json import config
from dataclasses_json import LetterCase
from .account_settings import AccountSettings
from .translate_map_value import TranslateMapValue
from .account import Account


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Fandom:
    image_id: int
    category: int
    status: int
    id: int
    karma_cof: int
    language_id: int
    name: str
    image_title_gif_id: int
    subscribes_count: int
    creator_id: int
    closed: bool
    image_title_id: int
    date_create: int
