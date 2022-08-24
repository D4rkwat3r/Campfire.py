from .api_exception import APIException


class LoginIsNotDefault(APIException):
    def __init__(self, *args):
        super().__init__(*args)
