from asyncio import open_connection
from asyncio.streams import StreamReader
from asyncio.streams import StreamWriter
from ujson import dumps
from ujson import loads
from typing import Optional
from struct import pack
from struct import unpack
from struct import error as StructError
from ..exception import find_exception
from ..exception import BadResponse
from .campfire_api import CampfireAPI


class CampfireSocketAPI(CampfireAPI):

    def __init__(self):
        super().__init__()
        self._token = None
        self._reader: Optional[StreamReader] = None
        self._writer: Optional[StreamWriter] = None
        self.language_id = 1

    async def _write(self, data: bytes):
        self._writer.write(pack(">i", len(data)))
        self._writer.write(data)
        await self._writer.drain()

    async def _write_str(self, data: str):
        return await self._write(data.encode("utf-8"))

    async def _write_json(self, data: dict):
        return await self._write_str(dumps(data))

    async def _recv(self, size: int) -> bytes:
        return await self._reader.read(size)

    async def _recv_int(self, size: int) -> int:
        try: return unpack(">i", await self._recv(size))[0]
        except StructError as e: raise BadResponse(e)

    async def _recv_packet_size(self) -> int:
        return await self._recv_int(4)

    async def _recv_fully(self, size: int) -> bytes:
        buffer = bytearray()
        while len(buffer) < size:
            for byte in await self._recv(1024): buffer.append(byte)
        return bytes(buffer)

    async def _recv_fully_str(self,  size: int) -> str:
        return (await self._recv_fully(size)).decode("utf-8")

    async def _connect(self):
        self._reader, self._writer = await open_connection(self.SERVER_HOST, self.SERVER_PLAINTEXT_PORT)

    async def _close(self):
        self._writer.close()
        self._reader, self._writer = None, None

    def set_language(self, language_id: int):
        self.language_id = language_id

    async def send(self, request) -> dict:
        await self._connect()
        request.language_id(self.language_id)
        if self._token is not None: request.token(self._token)
        await self._write_str(request.as_json())
        try: data = loads(await self._recv_fully_str(await self._recv_packet_size()))
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
        await self._close()
        return response_data
