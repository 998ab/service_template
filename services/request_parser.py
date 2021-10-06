from aiohttp import web


async def parse_request_data(request: web.Request) -> (dict, dict, dict):
    query_data = parse_query(request)
    headers_data = parse_headers(request)
    json_data = await parse_json(request)
    return query_data, headers_data, json_data


def parse_headers(request: web.Request) -> dict:
    headers_raw = request.headers
    result = dict(headers_raw)

    return result


def parse_query(request: web.Request) -> dict:
    query_raw = request.query
    result = dict(query_raw)
    return result


async def parse_json(request: web.Request) -> dict:
    request_text = ''

    if request.body_exists:
        request_text = await request.json()
        # json_response = json.loads(request_text)

    result = dict(request_text)
    return result


__all__ = [
    "parse_request_data",
    "parse_headers",
    "parse_query",
    "parse_json",
]
