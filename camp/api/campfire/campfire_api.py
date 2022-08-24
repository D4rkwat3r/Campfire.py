from abc import ABC


class CampfireAPI(ABC):

    API_VERSION = "1.290"
    CAMPFIRE = "Campfire"
    SERVER_HOST = "46.254.16.245"
    SERVER_TLS_PORT = 4026
    SERVER_CERTIFICATE_PORT = 4027
    SERVER_PLAINTEXT_PORT = 4028
    SERVER_STREAM_PORT = 4200

    # CERT, CERT_PASSWORD = TLS(SERVER_HOST, SERVER_CERTIFICATE_PORT).get_cert()

    async def send(self, request) -> dict:
        ...
