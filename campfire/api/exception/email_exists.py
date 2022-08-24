from .api_exception import APIException


class EmailExists(APIException):
    def __init__(self, *args):
        super().__init__(*args)
