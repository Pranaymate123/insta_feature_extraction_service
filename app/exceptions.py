class InvalidUrlException(Exception):
    def __init__(self, code: int, message: str, details: str = None):
        self.code = code
        self.message = message
        self.details = details or "No additional details provided"
