from hashlib import sha512
from typing import Optional
from re import search
from .api import APIRequest
from .api import CampfireAPI
from .api import CampfireSocketAPI
from .api import FirebaseClient
from .api import BadResponse
from .model import TranslateMap
from .model import FirebaseAccountInfo
from .model import FirebaseTokenInfo
from .model import AccountSettings
from .model import AccountFullInfo
from .model import AccountInfo
from .model import ChatTag
from .model import ChatMessage


class Client:
    def __init__(self, api: CampfireAPI = CampfireSocketAPI(), firebase_proxy: Optional[str] = None):
        super().__init__()
        self.api = api
        self._firebase_client = FirebaseClient(firebase_proxy)

    async def get_translate_map(self, force_language: int = None) -> TranslateMap:
        request = APIRequest(name=APIRequest.TRANSLATE_GET_MAP)
        if force_language is not None: request.language_id(force_language)
        return TranslateMap.from_dict(await request(self.api))

    async def create_account(self, email: str, password: str) -> FirebaseAccountInfo:
        response = await self._firebase_client.signup_new_user(
            email,
            sha512(password.encode("utf-8")).hexdigest()
        )
        try: return FirebaseAccountInfo.from_dict(response)
        except Exception as e: raise BadResponse(e)

    async def get_access_token(self, refresh_token: str) -> FirebaseTokenInfo:
        response = await self._firebase_client.get_token_info(refresh_token)
        try: return FirebaseTokenInfo.from_dict(response)
        except Exception as e: raise BadResponse(e)

    async def send_verification_code(self, id_token: str) -> None:
        await self._firebase_client.send_oob_confirmation(id_token)

    async def verify_account(self, code: str) -> None:
        if code.startswith("http"):
            try: code = search(r"oobCode=([A-z0-9_\-]+)", code).groups(0)[0]
            except (IndexError, AttributeError): code = ""
        await self._firebase_client.verify_email(code)

    async def login_by_token(self, token: str) -> AccountFullInfo:
        translate = await self.get_translate_map()
        translate_eng = await self.get_translate_map(1)
        request = APIRequest(name=APIRequest.ACCOUNTS_LOGIN) \
            .email2_token(token) \
            .field("translateMapHashEng",translate_eng.translate_map_hash) \
            .field("translateMapHash", translate.translate_map_hash)
        return await request(self.api)

    async def login(self, email: str, password: str) -> AccountFullInfo:
        token = (await self._firebase_client.get_token_info(
            (await self._firebase_client.verify_password(
                    email,
                    sha512(password.encode("utf-8")).hexdigest()
            ))["refreshToken"]
        ))["access_token"]
        return await self.login_by_token(token)

    async def change_name(self, name: str) -> None:
        request = APIRequest(name=APIRequest.ACCOUNTS_CHANGE_NAME).field("name", name)
        await request(self.api)

    async def send_message(
            self,
            target_id: int,
            sub_id: int,
            chat_type: int,
            text: str,
            quote_message_id: int = 0,
            sticker_id: int = 0) -> dict:
        tag = ChatTag(chat_type, target_id, sub_id)
        request = APIRequest(name=APIRequest.CHAT_MESSAGE_CREATE).field("tag", tag.to_dict()) \
            .data_output([]) \
            .data_output_add(-1) \
            .data_output_add(-1) \
            .field("text", text) \
            .field("quoteMessageId", quote_message_id) \
            .field("stickerId", sticker_id)
        return await request(self.api)

    async def get_chat_messages(self,
                                target_id: int,
                                sub_id: int,
                                chat_type: int,
                                offset_date: int = 0,
                                message_id: int = 0) -> list[ChatMessage]:
        tag = ChatTag(chat_type, target_id, sub_id)
        request = APIRequest(name=APIRequest.CHAT_MESSAGES_GET) \
            .field("tag", tag.to_dict()) \
            .field("offsetDate", offset_date) \
            .field("old", False) \
            .field("messageId", message_id)
        return [
            ChatMessage.from_dict(message)
            for message in (await request(self.api))["units"]
        ]

    async def get_chat_message(self, target_id: int, sub_id: int, chat_type: int, message_id: int) -> ChatMessage:
        tag = ChatTag(chat_type, target_id, sub_id)
        request = APIRequest(name=APIRequest.CHAT_MESSAGE_GET) \
            .field("tag", tag.to_dict()) \
            .field("messageId", message_id)
        return ChatMessage.from_dict(await request(self.api))

    async def set_sex(self, sex: int) -> None:
        return await APIRequest(name=APIRequest.ACCOUNTS_SET_SEX).field("sex", sex)(self.api)

    async def set_account_settings(self, **kwargs) -> None:
        await APIRequest(name=APIRequest.ACCOUNTS_SET_SETTINGS) \
            .field("settings", AccountSettings(**kwargs).to_dict())(self.api)

    async def get_account_info(self) -> AccountInfo:
        request = APIRequest(name=APIRequest.ACCOUNTS_GET_INFO)
        return AccountInfo.from_dict(await request(self.api))
