from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json
from dataclasses_json import config
from dataclasses_json import LetterCase
from .account import Account
from .chat_message_body import ChatMessageBody
from .fandom import Fandom


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ChatMessage:
    subUnits_count: int
    parent_unit_id: int
    fandom_image_id: int
    fandom_name: str
    creator_image_id: int
    language_id: int
    fandom_karma_cof: int
    fandom: Fandom
    reports_count: int
    category: int
    tag_6: int
    status: int
    unit_type: int
    tag_5: int
    id: int
    tag_7: int
    creator_id: int
    parent_unit_type: int
    creator_sex: int
    tag_3: int
    creator_lvl: int
    creator: Account
    creator_karma30: int
    tag_s_1: str
    tag_1: int
    my_karma: int
    important: int
    karma_count: int
    creator_last_online_time: int
    blacklisted: bool
    tag_2: int
    fandom_closed: bool
    fandom_id: int
    tag_4: int
    creator_name: str
    closed: bool
    date_create: int
    body: ChatMessageBody = field(metadata=config(field_name="jsonDB"))
