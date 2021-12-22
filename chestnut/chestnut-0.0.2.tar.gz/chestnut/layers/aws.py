from typing import Callable
from chestnut.http import Request, Response
from .framework import framework_layer


def response_to_aws(response: Response) -> dict:
	"""
	Converts chestnut.http.Response to a AWS lambda output.
	"""
	return {
		"statusCode": response.status,
		"headers": response.headers,
		"body": response.body.decode()
	}


def aws_to_request(event: dict) -> Request:
	"""
	Converts AWS lambda event into a chestnut.http.Request.
	"""
	return Request(
		method=event.get("httpMethod"),
		path=event.get("resource"),
		headers=event.get("multiValueHeaders"),
		route=event.get("pathParameters"),
		query=event.get("multiValueQueryStringParameters"),
		body=event.get("body")
	)


def aws_layer(handler: Callable, req: dict) -> dict:
	return framework_layer(aws_to_request, response_to_aws, handler, req)
