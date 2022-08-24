from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json
from dataclasses_json import LetterCase
from dataclasses_json import config
from .translate_map_value import TranslateMapValue


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TranslateMap:
    translate_language_id: int
    translate_map_hash: int
    translate_map_value: list[TranslateMapValue] = field(metadata=config(field_name="translate_map_v"))
    translate_map_keys: list[str] = field(metadata=config(field_name="translate_map_k"))
