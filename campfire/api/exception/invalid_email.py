from .api_exception import APIException


class InvalidEmail(APIException):
    def __init__(self, *args):
        super().__init__(*args)
