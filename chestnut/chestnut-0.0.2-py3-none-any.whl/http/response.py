from types import GeneratorType
from typing import Union, Generator
from json import dumps, loads
from fir import http


class Response(http.Response):

	__slots__ = ["status", "_body"]
	
	JSON_ENCODER = None

	def __init__(self, *args, status = None, mimetype = None, **kwargs):
		status_code = kwargs.pop("status_code", None)
		if status is not None:
			status_code = status
		super().__init__(*args, **kwargs, status_code=status_code)
		self.status = status_code
		if self.is_json:
			self.headers["Content-Type"] = "application/json"
		if mimetype is not None:
			self.headers["Content-Type"] = mimetype

	def is_stream(self) -> bool:
		return isinstance(self._body, GeneratorType)

	def is_json(self) -> bool:
		return isinstance(self._body, (dict, list))
	
	@property
	def body(self) -> bytes:
		if self.is_json():
			return dumps(self._body, separators=(',', ':'), cls=self.JSON_ENCODER).encode()
		elif self.is_stream():
			return ("".join(self._body)).encode()
		elif isinstance(self._body, str):
			return self._body.encode()
		else:
			return self._body

	@body.setter
	def body(self, value: Union[bytes, str, dict, list, Generator[str, None, str]]):
		self._body = value

	@property
	def text(self) -> str:
		return self.body.decode()

	@property
	def mimetype(self) -> str:
		return self.headers.get("Content-Type", "*")

	def json(self):
		if self.is_json():
			return self._body
		else:
			return loads(self.body.decode())
