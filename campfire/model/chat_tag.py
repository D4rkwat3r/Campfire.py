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
class ChatTag:
    chat_type: int
    target_id: int
    target_sub_id: int
