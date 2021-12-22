from typing import Callable
from chestnut.http import Request, Response
import azure.functions as func
from .framework import framework_layer


def response_to_azure(response: Response) -> func.HttpResponse:
	"""
	Converts chestnut.http.Response to azure.functions.HttpResponse
	"""
	return func.HttpResponse(
		response.body,
		status_code=response.status,
		headers=response.headers
	)


def azure_to_request(req: func.HttpRequest) -> Request:
	"""
	Converts azure.functions.HttpRequest to chestnut.http.Request
	"""
	return Request(
		method=req.method,
		uri=req.url,
		headers=req.headers,
		route=req.route_params,
		body=req.get_body()
	)


def azure_layer(handler: Callable, req: func.HttpRequest) -> func.HttpResponse:
	return framework_layer(azure_to_request, response_to_azure, handler, req)
