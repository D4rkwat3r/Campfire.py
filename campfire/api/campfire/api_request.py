from ujson import dumps
from time import time_ns as nanotime
from random import randint
from .campfire_api import CampfireAPI


class APIRequest:

    TRANSLATE_GET_MAP = "RTranslateGetMap"
    ACCOUNTS_GET_INFO = "RAccountsGetInfo"
    ACCOUNTS_LOGIN = "RAccountsLogin"
    ACCOUNTS_FIREBASE_ADD = "RAccountsFirebaseAdd"
    ACCOUNTS_CHANGE_NAME = "RAccountsChangeName"
    ACCOUNTS_SET_SEX = "RAccountsBioSetSex"
    ACCOUNTS_SET_SETTINGS = "RAccountSetSettings"
    CHAT_MESSAGE_CREATE = "RChatMessageCreate"
    CHAT_MESSAGE_GET = "RChatMessageGet"
    CHAT_MESSAGES_GET = "RChatMessageGetAll"

    def __init__(self,
                 name: str,
                 date: int = None,
                 token: str = None,
                 login_token: str = None,
                 api_version: str = None,
                 data_output: list = None,
                 data_output_base64: list = None,
                 project_key_id: str = None,
                 language_id: int = None):
        self._name = name
        self._date = date
        self._token = token
        self._login_token = login_token
        self._api_version = api_version
        self._data_output = data_output
        self._data_output_base64 = data_output_base64
        self._project_key_id = project_key_id
        self._language_id = language_id
        self._data = {}

    def __call__(self, api: CampfireAPI, *args, **kwargs):
        return self.send(api)

    def __getattr__(self, item):
        return lambda v: self.field(item, v)

    def name(self, name: str): self._name = name; return self
    def date(self, date: int): self._date = date; return self
    def token(self, token: str): self._token = token; return self
    def login_token(self, token: str): self._login_token = token; return self
    def email2_token(self, token: str): self._login_token = f"Email2 - {token}"; return self
    def api_version(self, api_version: str): self._api_version = api_version; return self
    def data_output(self, data_output: list): self._data_output = data_output; return self
    def data_output_add(self, value: int): self._data_output.append(value); return self
    def language_id(self, language_id: int): self._language_id = language_id; return self
    def field(self, key: str, value): self._data[key] = value; return self

    def as_json(self) -> str:
        json = {
            "J_REQUEST_NAME": self._name,
            "J_REQUEST_DATE": self._date or nanotime(),
            "requestProjectKey": self._project_key_id or CampfireAPI.CAMPFIRE,
            "requestApiVersion": self._api_version or CampfireAPI.API_VERSION,
            "dataOutput": self._data_output if self._data_output is not None else [],
            "dataOutputBase64": self._data_output_base64 if self._data_output_base64 is not None else []
        }
        if self._language_id is not None: json["languageId"] = self._language_id
        if self._token is not None: json["J_API_ACCESS_TOKEN"] = self._token
        if self._login_token is not None: json["J_API_LOGIN_TOKEN"] = self._login_token
        for key in self._data: json[key] = self._data[key]
        return dumps(json)

    async def send(self, api: CampfireAPI = None) -> dict: return await api.send(self)
