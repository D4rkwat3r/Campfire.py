from .api_exception import APIException


class BadResponse(APIException):
    def __init__(self, caused_by: Exception):
        self.caused_by = caused_by
        super().__init__("-1", "Unable to process response from Campfire API", [])
