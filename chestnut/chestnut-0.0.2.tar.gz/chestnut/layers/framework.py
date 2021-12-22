from typing import Callable
from chestnut.http import Request


def framework_layer(
	request_converter: Callable,
	response_converter: Callable,
	handler: Callable,
	req: Request
):
	return response_converter(handler(request_converter(req)))

