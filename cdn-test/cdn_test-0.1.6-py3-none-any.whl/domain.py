import os
import json
import csv
import pydantic
import requests
from pathlib import Path
import logging
from time import sleep
from datetime import (
    datetime,
    timedelta
)

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(message)s'
)


class ResponseStatus(pydantic.BaseModel):
    cached: bool
    date_time: datetime
    elapsed_time: timedelta
    url: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class InputOptions(pydantic.BaseModel):
    url: str
    output_file: Path = Path('/tmp/cdn-report.csv')
    time_step: str = '1m'
    http_verb: str = 'GET'
    timeout: int = 60
    header_name = 'x-cache'


def append_record(response_status: ResponseStatus, record_file: Path):
    record_path = record_file.expanduser()
    record_path.parent.mkdir(parents=True, exist_ok=True)

    record_row = json.loads(response_status.json())

    with record_path.open('a') as csvfile:
        fieldnames = list(sorted(record_row.keys()))
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(record_row)


def check_endpoint_aws_cloudfront(headers: dict, header_name='x-cache') -> bool:
    headers_lower_case = {key.lower(): value for key, value in headers.items()}
    cache_header_value = headers_lower_case.get(header_name)

    if not cache_header_value:
        raise KeyError(f'{header_name} not found in response headers')

    if cache_header_value.lower() == 'hit from cloudfront':
        status = True
    else:
        status = False

    return status


def request_endpoint(url: str, timeout_seconds=60, http_verb='GET') -> (dict, float):
    response = requests.request(http_verb, url=url, timeout=timeout_seconds, allow_redirects=False)
    headers = response.headers.copy()
    elapsed_time = response.elapsed

    return headers, elapsed_time


def parse_time_step(time_step: str) -> timedelta:
    unit_character = time_step[-1].lower()
    time_numbers = time_step[:-1]

    abbreviation = {
        's': 'seconds',
        'm': 'minutes',
        'd': 'days'
    }

    if not unit_character.isalpha():
        unit_character = 's'

    if not time_numbers.isnumeric():
        raise ValueError(f'value {time_numbers} is not number')

    unit_arg = abbreviation[unit_character]

    return timedelta(**{unit_arg: int(time_numbers)})


def main_routine(input_parameters: InputOptions):
    step_time_delta = parse_time_step(input_parameters.time_step)

    while True:
        headers, elapsed_time = request_endpoint(
            url=input_parameters.url,
            timeout_seconds=input_parameters.timeout,
            http_verb=input_parameters.http_verb
        )
        requests_time = datetime.now()
        request_status = check_endpoint_aws_cloudfront(headers, input_parameters.header_name)

        try:
            response_status = ResponseStatus(
                date_time=requests_time,
                elapsed_time=elapsed_time,
                cached=request_status,
                url=input_parameters.url
            )
        except requests.RequestException as e:
            logging.error(f'requests error {e}')
            sleep(5)
            continue

        append_record(response_status, input_parameters.output_file)
        logging.info(response_status.json())

        sleep(step_time_delta.seconds)


def main(input_parameters: InputOptions):
    try:
        main_routine(input_parameters)
    except KeyboardInterrupt:
        pass
