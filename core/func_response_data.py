from tenacity import *  # noqa
import requests
import json  # noqa
from core import settings as core_settings


def is_server_error(error):
    retry_again = False
    if error.status_code in core_settings.SERVER_SIDE_ERROR_CODES:
        retry_again = True
    return retry_again


@retry(  # noqa
    wait=wait_random_exponential(multiplier=1, max=30),  # noqa
    stop=stop_after_attempt(3),  # noqa
    retry=(retry_if_result(is_server_error))  # noqa
)
def response_data(
        url_path,
        http_method=core_settings.HTTP_GET_METHOD,
        new_headers=core_settings.HEADERS,
        new_params=core_settings.QUERY_STRING):
    url = core_settings.API_URL + url_path
    response = requests.request(
        http_method,
        url,
        headers=new_headers,
        params=new_params
    )
    return response
