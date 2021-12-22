import flask
from typing import Callable
from chestnut.http import Request, Response
from .framework import framework_layer


def response_to_gcp(response: Response) -> flask.Response:
	"""
	Converts a chestnut.http.Response to flask.Response
	"""
	if response.is_stream():
		r = flask.Response(flask.stream_with_context(response._body), mimetype=response.mimetype)
	else:
		r = flask.Response(response.body, status=response.status, mimetype=response.mimetype)
	r.headers = {**r.headers, **response.headers}
	return r


def gcp_to_request(req: flask.Request) -> Request:
	"""
	Converts flask.Request to chestnut.http.Request
	"""
	return Request(
		method=req.method,
		path=req.path,
		headers=req.headers,
		route=req.view_args,
		query={key: req.args.getlist(key) for key in list(req.args)},
		body=req.stream.read()
	)


def gcp_layer(handler: Callable, req: flask.Request) -> flask.Response:
	return framework_layer(gcp_to_request, response_to_gcp, handler, req)
