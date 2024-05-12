import os
import types
import json
import allure
import logging
import datetime
from utils import resource
from curlify import to_curl
from requests import Response


def humanify(name: str):
    import re
    return ' '.join(re.split('_+', name))


def write_log_to_file(data: str):
    log_file = os.getenv('LOG_FILE')
    file_name = (resource.path_log_file(log_file) + ".log")
    with open(file_name, 'a', encoding='utf=8') as logger_file:
        logger_file.write(data + '\n')


def step(fn):
    def fn_with_logging(*args, **kwargs):
        is_method = (
                args
                and isinstance(args[0], object)
                and isinstance(getattr(args[0], fn.__name__), types.MethodType)
        )

        args_to_log = args[1:] if is_method else args
        args_and_kwargs_to_log_as_strings = [
            *map(str, args_to_log),
            *[f'{key}={value}' for key, value in kwargs.items()]
        ]
        args_and_kwargs_string = (
            (': ' + ', '.join(map(str, args_and_kwargs_to_log_as_strings)))
            if args_and_kwargs_to_log_as_strings
            else ''
        )

        write_log_to_file(
            f"\n-----\n"
            + f"Start time: {str(datetime.datetime.now())}\n"
            + '\n'
            + (f'[{args[0].__class__.__name__}] ' if is_method else '')
            + humanify(fn.__name__)
            + args_and_kwargs_string
        )

        return fn(*args, **kwargs)

    return fn_with_logging


def response_logging(response: Response):
    curl = to_curl(response.request)
    logging.info(to_curl(response.request))
    logging.info("Request: " + response.request.url)
    logging.info("Request headers: " + str(response.request.headers))
    logging.info("Status code: " + str(response.status_code))
    logging.info("Response: " + response.text)
    logging.debug(to_curl(response.request))
    allure.attach(body=curl, name="curl", attachment_type=allure.attachment_type.TEXT, extension='txt')
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True),
                  name="response",
                  attachment_type=allure.attachment_type.JSON,
                  extension='json')