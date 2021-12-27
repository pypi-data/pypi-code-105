import json
from typing import Optional, List, Dict, Union

from opentelemetry import trace
from opentelemetry.propagate import inject
from opentelemetry.propagators.textmap import Setter
from opentelemetry.semconv.trace import SpanAttributes

from helios.instrumentation.base_http_instrumentor import HeliosBaseHttpInstrumentor


class ASGISetter(Setter):

    def set(self, carrier: dict, key: str, value: str) -> None:
        """Setter implementation to add a HTTP header value to the ASGI
        scope.

        Args:
            carrier: ASGI scope object
            key: header name in scope
            value: header value
        """
        # asgi header keys are in lower case
        key = key.lower()
        headers = carrier.get("headers", [])
        carrier["headers"] = [(key.encode('utf-8'), value.encode('utf-8'))] + headers


asgi_setter = ASGISetter()


class HeliosAsgiMiddleware:

    def __init__(self, app, tracer=None, get_span_details=None):
        self.app = app
        self.tracer = tracer
        self.get_span_details = get_span_details or self.get_default_span_details

    @staticmethod
    def get_default_span_details(scope: Dict):
        span_name = scope.get("path", "").strip() or "HTTP {}".format(
            scope.get("method", "").strip()
        )

        return span_name, {}

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        span_name, attributes = self.get_span_details(scope)

        self.set_url(attributes, scope)
        self.set_method(attributes, scope)

        request_headers = self.extract_headers(scope.get('headers'))
        attributes[HeliosBaseHttpInstrumentor.HTTP_REQUEST_HEADERS_ATTRIBUTE_NAME] = json.dumps(request_headers)

        with self.tracer.start_as_current_span(
            f"{span_name}", kind=trace.SpanKind.SERVER,
        ) as span:
            span.set_attributes(attributes)

            async def wrapped_send(message):
                if 'headers' in message:
                    response_headers = HeliosAsgiMiddleware.extract_headers(message.get('headers'))
                    span.set_attribute(
                        HeliosBaseHttpInstrumentor.HTTP_RESPONSE_HEADERS_ATTRIBUTE_NAME,
                        json.dumps(response_headers))

                if 'body' in message:
                    span.set_attribute(
                        HeliosBaseHttpInstrumentor.HTTP_RESPONSE_BODY_ATTRIBUTE_NAME, message.get('body'))

                return await send(message)

            async def wrapped_receive():
                message = await receive()
                if 'body' in message:
                    span.set_attribute(
                        HeliosBaseHttpInstrumentor.HTTP_REQUEST_BODY_ATTRIBUTE_NAME, message.get('body'))
                return message

            inject(scope, setter=asgi_setter)
            return await self.app(scope, wrapped_receive, wrapped_send)

    @staticmethod
    def extract_headers(headers: Optional[List]) -> Optional[Dict]:
        if headers is None:
            return None
        return {
            HeliosAsgiMiddleware.bytes_to_str(key): HeliosAsgiMiddleware.bytes_to_str(value)
            for (key, value) in headers
        }

    @staticmethod
    def bytes_to_str(str_or_bytes: Union[str, bytes]) -> str:
        return str_or_bytes.decode() if isinstance(str_or_bytes, bytes) else str_or_bytes

    @staticmethod
    def set_url(attributes, scope):
        url = ''
        try:
            protocol = scope.get('type')
            host, port = scope.get('server')
            root_path = scope.get('root_path')
            path = scope.get('path')
            port = '' if port in [80, 443] else f':{port}'

            url = f'{protocol}://{host}{port}{root_path}{path}'
        except Exception:
            pass
        finally:
            attributes[SpanAttributes.HTTP_URL] = url

    @staticmethod
    def set_method(attributes, scope):
        method = ''
        try:
            method = scope.get('method', '').strip()
        except Exception:
            pass
        finally:
            attributes[SpanAttributes.HTTP_METHOD] = method
