from aiohttp import web
from global_models.error import Error
from global_models.service_response import ServiceResponse

from exceptions.service_exception_base import ServiceExceptionBase
from logger import log
from services.request_parser import parse_request_data


def controller_middleware(fn):
    async def wrapper(request: web.Request):
        service_response = ServiceResponse()
        try:
            query_data, headers_data, json_data = await parse_request_data(request)
            log.info(f"[controller_middleware].{fn.__name__}: request: {query_data}, {headers_data}, {json_data}")
            service_response = await fn(query_data, headers_data, json_data, request)
        except ServiceExceptionBase as ex:
            log.error(ex)
            payload = Error(message=ex.error_message, code=ex.error_code)
            service_response = ServiceResponse(status_code=ex.response_status_code,
                                               payload=payload)
        except Exception as ex:
            log.critical(ex)
            payload = Error(message="Internal Error", code="Internal Error")
            service_response = ServiceResponse(payload=payload)
        finally:
            service_response_text = service_response.to_json()
            log.info(f"[controller_middleware].{fn.__name__}: response: {service_response_text}")
            return web.Response(status=service_response.status_code,
                                content_type=service_response.content_type,
                                text=service_response_text)
    return wrapper
