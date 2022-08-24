from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json
from dataclasses_json import LetterCase
from dataclasses_json import config


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ChatMessageBody:
    type: int = field(metadata=config(field_name="J_TYPE"))
    chat_type: int
    quote_id: int
    quote_text: str
    quote_images: list[int]
    quote_images_pwd: list[str]
    quote_sticker_id: int
    quote_sticker_image_id: int
    quote_creator_name: str
    changed: bool
    random_tag: int
    answer_name: str
    text: str = field(metadata=config(field_name="J_TEXT"))
    resource_id: int = field(metadata=config(field_name="J_RESOURCE_ID"))
    gif_id: int
    image_w: int = field(metadata=config(field_name="J_IMAGE_W"))
    image_h: int = field(metadata=config(field_name="J_IMAGE_H"))
    image_pwd: str
    system_type: int
    system_owner_id: int
    system_owner_sex: int
    system_owner_name: str
    system_target_id: int
    system_target_name: str
    system_comment: str
    system_tag: int
    block_moderation_event_id: int
    block_date: int
    image_id_array: list[int]
    image_w_array: list[int]
    image_h_array: list[int]
    image_pwd_array: list[str]
    voice_resource_id: int
    voice_ms: int
    voice_mask: list[int]
    sticker_id: int
    sticker_image_id: int
    sticker_gif_id: int
