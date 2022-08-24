from httpx import AsyncClient
from typing import Optional
from ..exception import BadResponse
from ..exception import find_exception


class FirebaseClient:
    def __init__(self, proxy: Optional[str] = None):
        self.api_base = "https://www.googleapis.com"
        self.api_tokens = "https://securetoken.googleapis.com"
        self.requests_headers = {
            "X-Android-Cert": "8AB61A2007F71CFF732FD08132E71C3AEA7A0B98",
            "X-Client-Version": "Android/Fallback/X20000004/FirebaseCore-Android",
            "X-Android-Package": "com.dzen.campfire",
            "Content-Type": "application/json",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/N2G48H)"
        }
        self.http_client = AsyncClient(proxies=proxy)

    async def _request(self, base: str, endpoint: str, key: str, **kwargs) -> dict:
        try:
            response = await self.http_client.post(
                f"{base}{endpoint}?key={key}",
                headers=self.requests_headers,
                json=kwargs,
            )
            json = response.json()
        except Exception as e:
            raise BadResponse(e)
        if response.status_code != 200:
            try: find_exception(json["error"]["code"], json["error"]["message"], [])
            except Exception as e: raise BadResponse(e)
        return json

    async def signup_new_user(self, email: str, password: str) -> dict:
        return await self._request(
            self.api_base,
            "/identitytoolkit/v3/relyingparty/signupNewUser",
            "AIzaSyACrbV2hnCsYZmdzAa7-8M5eaZUWYiXd5c",
            email=email,
            password=password
        )

    async def send_oob_confirmation(self, token: str, request_type: int = 4) -> dict:
        return await self._request(
            self.api_base,
            "/identitytoolkit/v3/relyingparty/getOobConfirmationCode",
            "AIzaSyACrbV2hnCsYZmdzAa7-8M5eaZUWYiXd5c",
            idToken=token,
            requestType=request_type
        )

    async def verify_email(self, oob_code: str) -> dict:
        return await self._request(
            self.api_base,
            "/identitytoolkit/v3/relyingparty/setAccountInfo",
            "AIzaSyCwgElH2DjRl1a0F6gb3LlNGEGeRNogIKA",
            oobCode=oob_code
        )

    async def get_token_info(self, token: str) -> dict:
        return await self._request(
            self.api_tokens,
            "/v1/token",
            "AIzaSyACrbV2hnCsYZmdzAa7-8M5eaZUWYiXd5c",
            grantType="refresh_token",
            refreshToken=token
        )

    async def verify_password(self, email: str, password: str) -> dict:
        return await self._request(
            self.api_base,
            "/identitytoolkit/v3/relyingparty/verifyPassword",
            "AIzaSyACrbV2hnCsYZmdzAa7-8M5eaZUWYiXd5c",
            email=email,
            password=password,
            returnSecureToken=True
        )
