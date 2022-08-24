from dataclasses import dataclass
from dataclasses_json import dataclass_json
from dataclasses_json import LetterCase
from .chat_tag import ChatTag


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AccountInfo:
    karma_counts: list[int]
    fandoms_ids: list[int]
    languages_ids: list[int]
    # notifications: list[Notification]
    chat_messages_count_tags: list[ChatTag]
    viceroy_fandoms_ids: list[int]
    viceroy_languages_ids: list[int]
    # empty apiInfo: ApiInfo
    activities_count = int
