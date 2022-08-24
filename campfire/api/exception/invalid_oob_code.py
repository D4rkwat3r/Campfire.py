from .api_exception import APIException


class InvalidOOBCode(APIException):
    def __init__(self, *args):
        super().__init__(*args)
