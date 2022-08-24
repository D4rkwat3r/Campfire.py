from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json
from dataclasses_json import config
from dataclasses_json import LetterCase
from .account_settings import AccountSettings
from .translate_map_value import TranslateMapValue


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AccountEffect:
    id: int
    accountId: int
    dateCreate: int
    dateEnd: int
    comment: str
    effectIndex: int
    tag: int
    commentTag: int
    fromAccountName: str
