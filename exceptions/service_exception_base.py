class ServiceExceptionBase(Exception):
    def __init__(self, error_code: str = None, error_message: str = None, response_status_code: int = None):
        if error_code is not None:
            self.error_code = error_code
        if error_message is not None:
            self.error_message = error_message
        if response_status_code is not None:
            self.response_status_code = response_status_code

    error_message: str = str()
    error_code: str = str()
    response_status_code: int = 500
