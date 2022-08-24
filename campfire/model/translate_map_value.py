from dataclasses import dataclass
from dataclasses_json import dataclass_json
from dataclasses_json import LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TranslateMapValue:
    project_key: str
    hint: str
    language_id: int
    text: str
    key: str
