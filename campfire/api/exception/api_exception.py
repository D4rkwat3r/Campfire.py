class APIException(Exception):
    def __init__(self, code: str, message: str, params: list):
        self.code = code
        self.message = message
        self.params = params
        super().__init__(self.message)
