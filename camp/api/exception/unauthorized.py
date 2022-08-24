from .api_exception import APIException


class Unauthorized(APIException):
    def __init__(self, *args):
        super().__init__(*args)
