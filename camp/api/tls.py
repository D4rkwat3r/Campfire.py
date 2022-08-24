from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from typing import Optional


class TLS:

    CERT_FILE = "campfire_cert"
    CERT_FILE_PASSWORD = "campfire_cert_password"

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def _read_cert(self) -> Optional[tuple]:
        try:
            with open(self.CERT_FILE, "rb") as file: cert = file.read()
            with open(self.CERT_FILE_PASSWORD, "rb") as file: pwd = file.read()
        except FileNotFoundError: return None
        return cert, pwd

    def _write_cert(self, data: tuple):
        with open(self.CERT_FILE, "wb") as file: file.write(data[0])
        with open(self.CERT_FILE_PASSWORD, "wb") as file: file.write(data[1])

    def get_cert(self) -> tuple:
        cert_data = self._read_cert()
        if cert_data is None:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((self.host, self.port))
            data = s.recv(1024), s.recv(1024)
            s.close()
            self._write_cert(data)
        else: return cert_data
        return self._read_cert()
