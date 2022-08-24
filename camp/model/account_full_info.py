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
class AccountFullInfo:
    settings: AccountSettings
    translate_language_id: int
    translate_map_hash: int
    translate_map_value: list[TranslateMapValue] = field(metadata=config(field_name="translate_map_v"))
    translate_map_keys: list[str] = field(metadata=config(field_name="translate_map_k"))
    translate_map_eng_value: list[TranslateMapValue] = field(metadata=config(field_name="translate_map_eng_v"))
    translate_map_eng_keys: list[str] = field(metadata=config(field_name="translate_map_eng_k"))
    has_subscribers: bool
    protoadmins: list[int]
    version: str
    supported: str
    supported_version: list[str]
    server_time: int
    account: Account
