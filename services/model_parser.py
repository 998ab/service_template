from global_models.service_template.book import BookCreate, BookUpdatePrice
from global_models.service_template.client import Client
from global_models.service_template.req_append_book import ReqAppendBook
from pydantic import ValidationError

from exceptions.service_exception_base import ServiceExceptionBase


class ModelParserException(ServiceExceptionBase):
    def __init__(self, *, error_code: str = None, error_message: str = None, response_status_code: int = None):
        super().__init__(error_code, error_message, response_status_code)

    def __str__(self):
        return "ModelParserException"


def parse_client(data: dict) -> Client:
    result = _parse_model(Client, data)
    return result


def parse_book_create(data: dict) -> BookCreate:
    result = _parse_model(BookCreate, data)
    return result


def parse_book_update_price(data: dict) -> BookUpdatePrice:
    result = _parse_model(BookUpdatePrice, data)
    return result


def parse_req_append_book(data: dict) -> ReqAppendBook:
    result = _parse_model(ReqAppendBook, data)
    return result


def _parse_model(obj, data):
    try:
        new_client = obj.parse_obj(data)
        return new_client
    except ValidationError as ex:
        error = ex.errors()[0]
        error_message = str()

        if error.get('type').startswith("type_error"):
            error_message = f"Value is not valid: '{str(error.get('loc')[0])}'"
        elif error.get('type').startswith("value_error"):
            error_message = f"Missing field: '{str(error.get('loc')[0])}'"

        raise ModelParserException(error_code="Parses error",
                                   error_message=error_message,
                                   response_status_code=200)