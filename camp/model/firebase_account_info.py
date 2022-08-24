from dataclasses import dataclass
from dataclasses_json import dataclass_json
from dataclasses_json import LetterCase
from typing import Optional


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FirebaseAccountInfo:
    id_token: str
    email: str
    refresh_token: str
    expires_in: str
    local_id: str
    kind: Optional[str] = None
