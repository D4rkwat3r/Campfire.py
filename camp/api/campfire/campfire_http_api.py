from ujson import loads
from httpx import AsyncClient
from httpx import RemoteProtocolError
from httpx import Timeout
from typing import Optional
from ..exception import find_exception
from ..exception import BadResponse
from .campfire_api import CampfireAPI


class CampfireHTTPAPI(CampfireAPI):

    def __init__(self, proxy: Optional[str] = None):
        super().__init__()
        self._token = None
        self.language_id = 1
        self.proxy = proxy
        self._timeout = Timeout(15.0, connect=15.0)
        self._http_api = f"http://{self.SERVER_HOST}:{self.SERVER_PLAINTEXT_PORT}"

    def set_language(self, language_id: int):
        self.language_id = language_id

    async def send(self, request) -> dict:
        request.language_id(self.language_id)
        if self._token is not None: request.token(self._token)
        try:
            async with AsyncClient(proxies=self.proxy, timeout=self._timeout) as client:
                response = await client.post(self._http_api, content=request.as_json())
        except RemoteProtocolError as e:
            raise BadResponse(e)
        try: data = loads(response.text)
        except ValueError as e: raise BadResponse(e)
        response_data = data["J_RESPONSE"]
        if data["J_STATUS"] != "J_STATUS_OK":
            find_exception(
                response_data["code"],
                response_data["messageError"],
                response_data["params"]
            )
        if "J_API_ACCESS_TOKEN" in data:
            self._token = data["J_API_ACCESS_TOKEN"]
        return response_data
