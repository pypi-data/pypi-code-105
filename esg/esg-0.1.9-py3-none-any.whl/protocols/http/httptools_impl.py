import asyncio
import http
import logging
import re
try:
    import uvloop
except ImportError:
    uvloop = None
from collections import deque
from functools import partial
from typing import Callable
from urllib.parse import unquote
from socket import IPPROTO_TCP, TCP_NODELAY

from httptools import HttpParserError, HttpParserUpgrade, HttpRequestParser, parse_url

from esg.logging import TRACE_LOG_LEVEL
from esg.protocols.http.flow_control import (
    CLOSE_HEADER,
    HIGH_WATER_LIMIT,
    FlowControl,
    service_unavailable,
)
from esg.protocols.utils import (  # is_valid_header_name,; is_valid_header_value,
    get_client_addr,
    get_local_addr,
    get_path_with_query_string,
    get_remote_addr,
    is_ssl,
)

HEADER_RE = re.compile(b'[\x00-\x1F\x7F()<>@,;:[]={} \t\\"]')
HEADER_VALUE_RE = re.compile(b"[\x00-\x1F\x7F]")


def _get_status_line(status_code):
    try:
        phrase = http.HTTPStatus(status_code).phrase.encode()
    except ValueError:
        phrase = b""
    return b"".join([b"HTTP/1.1 ", str(status_code).encode(), b" ", phrase, b"\r\n"])


STATUS_LINE = {
    status_code: _get_status_line(status_code) for status_code in range(100, 600)
}


class HttpToolsProtocol(asyncio.Protocol):
    # __slots__ = [
    #     "config",
    #     "app",
    #     "on_connection_lost",
    #     "loop",
    #     "logger",
    #     "access_logger",
    #     "access_log",
    #     "parser",
    #     "ws_protocol_class",
    #     "root_path",
    #     "limit_concurrency",
    #     "timeout_keep_alive_task",
    #     "timeout_keep_alive",
    #     "server_state",
    #     "connections",
    #     "tasks",
    #     "default_headers",
    #     "transport",
    #     "flow",
    #     "server",
    #     "client",
    #     "scheme",
    #     "pipeline",
    #     "url",
    #     "scope",
    #     "headers",
    #     "expect_100_continue",
    #     "cycle",
    #     "cycle_partial",
    #     "connection_scope",
    # ]

    def __init__(
        self, config, server_state, on_connection_lost: Callable = None, _loop=None
    ):
        if not config.loaded:
            config.load()

        self.config = config
        self.app = config.loaded_app
        self.on_connection_lost = on_connection_lost
        self.loop = _loop or asyncio.get_event_loop()
        self.logger = logging.getLogger("esg.error")
        self.access_logger = logging.getLogger("esg.access")
        self.access_log = self.access_logger.hasHandlers()
        self.parser = HttpRequestParser(self)
        self.feed_data = self.parser.feed_data
        self.ws_protocol_class = config.ws_protocol_class
        self.root_path = config.root_path
        self.limit_concurrency = config.limit_concurrency

        # Timeouts
        self.timeout_keep_alive_task = None
        self.timeout_keep_alive = config.timeout_keep_alive

        # Global state
        self.server_state = server_state
        self.connections = server_state.connections
        self.tasks = server_state.tasks
        self.task_add = self.tasks.add
        self.task_discard = self.tasks.discard
        self.default_headers = server_state.default_headers

        # Per-connection state
        self.transport = None
        self.flow = None
        self.server = None
        self.client = None
        self.scheme = None
        self.connection_scope = None
        self.disconnected = None

        # Per-request state
        self.url = None
        self.scope = None
        self.headers = None
        self.expect_100_continue = False

        # Request state
        self.body = b""
        self.more_body = True

        # Response state
        self.response_complete = False
        self.response_started = False
        self._send_generator = None
        message_event = asyncio.Event()
        self.set_message_event = message_event.set
        self.wait_message_event = message_event.wait
        self.clear_message_event = message_event.clear
        self.run_asgi_event = asyncio.Event()
        self.worker = self.loop.create_task(self.run_asgi())
        self._send_generator_args = {}

    # Protocol interface
    def connection_made(self, transport):
        if True: # with self.server_state.measure("connection_made"):
            # if uvloop is not None and isinstance(loop, uvloop.Loop):
            sock = transport.get_extra_info('socket')
            try:
                sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
            except (OSError, NameError):
                pass

            self.connections.add(self)

            self.transport = transport
            self.flow = FlowControl(transport)
            self.server = get_local_addr(transport)
            self.client = get_remote_addr(transport)
            self.scheme = "https" if is_ssl(transport) else "http"

            kwargs = {
                "transport_write": transport.write,
                "default_headers":self.default_headers,
                "on_response": self.on_response_complete
            }

            self._send_generator_func = partial(self._send, **kwargs)

            if self.logger.level <= TRACE_LOG_LEVEL:
                prefix = "%s:%d - " % tuple(self.client) if self.client else ""
                self.logger.log(TRACE_LOG_LEVEL, "%sHTTP connection made", prefix)

            self.connection_scope = {
                # Per connection - state
                "type": "http",
                "asgi": {"version": self.config.asgi_version, "spec_version": "2.1"},
                "http_version": "1.1",
                "server": self.server,
                "client": self.client,
                "scheme": self.scheme,
                "root_path": self.root_path,
            }
            self.disconnected = False

    def connection_lost(self, exc):
        if True: # with self.server_state.measure("connection_lost"):
            self.connections.discard(self)

            if self.logger.level <= TRACE_LOG_LEVEL:
                prefix = "%s:%d - " % tuple(self.client) if self.client else ""
                self.logger.log(TRACE_LOG_LEVEL, "%sHTTP connection lost", prefix)

            if not self.response_complete:
                self.disconnected = True
            self.set_message_event()
            if flow := self.flow:
                flow.resume_writing()
            if exc is None:
                self.transport.close()

            if on_connection_lost := self.on_connection_lost:
                on_connection_lost()

        # self.server_state.stats
        self.worker.cancel()

    def eof_received(self):
        pass

    def _unset_keepalive_if_required(self):
        if True: # with self.server_state.measure("_unset_keepalive_if_required"):
            if timeout_keep_alive_task := self.timeout_keep_alive_task:
                timeout_keep_alive_task.cancel()
                self.timeout_keep_alive_task = None

    def data_received(self, data):
        if True: # with self.server_state.measure("data_received"):
            if timeout_keep_alive_task := self.timeout_keep_alive_task:
                timeout_keep_alive_task.cancel()
                self.timeout_keep_alive_task = None

            try:
                self.feed_data(data)
            except HttpParserError as exc:
                msg = "Invalid HTTP request received."
                self.logger.warning(msg, exc_info=exc)
                self.transport.close()
            except HttpParserUpgrade:
                self.handle_upgrade()

    def handle_upgrade(self):
        if True: # with self.server_state.measure("handle_upgrade"):
            upgrade_value = None
            for name, value in self.headers:
                if name == b"upgrade":
                    upgrade_value = value.lower()

            if upgrade_value != b"websocket" or self.ws_protocol_class is None:
                msg = "Unsupported upgrade request."
                self.logger.warning(msg)

                from esg.protocols.websockets.auto import AutoWebSocketsProtocol

                if AutoWebSocketsProtocol is None:
                    msg = "No supported WebSocket library detected. Please use 'pip install esg[standard]', or install 'websockets' or 'wsproto' manually."  # noqa: E501
                    self.logger.warning(msg)

                content = [STATUS_LINE[400]]
                for name, value in self.default_headers:
                    content.extend([name, b": ", value, b"\r\n"])
                content.extend(
                    [
                        b"content-type: text/plain; charset=utf-8\r\n",
                        b"content-length: " + str(len(msg)).encode("ascii") + b"\r\n",
                        b"connection: close\r\n",
                        b"\r\n",
                        msg.encode("ascii"),
                    ]
                )
                self.transport.write(bytearray().join(content))
                self.transport.close()
                return

            if self.logger.level <= TRACE_LOG_LEVEL:
                prefix = "%s:%d - " % tuple(self.client) if self.client else ""
                self.logger.log(TRACE_LOG_LEVEL, "%sUpgrading to WebSocket", prefix)

            self.connections.discard(self)
            method = self.scope["method"].encode()
            output = [method, b" ", self.url, b" HTTP/1.1\r\n"]
            for name, value in self.scope["headers"]:
                output += [name, b": ", value, b"\r\n"]
            output.append(b"\r\n")
            protocol = self.ws_protocol_class(
                config=self.config,
                server_state=self.server_state,
                on_connection_lost=self.on_connection_lost,
            )
            protocol.connection_made(self.transport)
            protocol.data_received(b"".join(output))
            self.transport.set_protocol(protocol)

    # Parser callbacks
    def on_url(self, url):
        if True: # with self.server_state.measure("on_url"):
            method = self.parser.get_method()
            parsed_url = parse_url(url)
            raw_path = parsed_url.path
            path = raw_path.decode("ascii")
            if "%" in path:
                path = unquote(path)
            self.url = url
            self.expect_100_continue = False
            self.headers = headers = []
        # if True: # with self.server_state.measure("on_url_2"):
            self.scope = {
                # Per-request state
                "method": method.decode(),
                "path": path,
                "raw_path": raw_path,
                "query_string": parsed_url.query or b"",
                "headers": headers,
                # Extract per-connection state
                **self.connection_scope,
            }
            self.body = b""

    def on_header(self, name: bytes, value: bytes):
        if True: # with self.server_state.measure("on_header"):
            name = name.lower()
            if name == b"expect" and value.lower() == b"100-continue":
                self.expect_100_continue = True
            self.headers.append((name, value))

    def on_headers_complete(self):
        if True: # with self.server_state.measure("on_headers_complete_1"):
            parser = self.parser
            http_version = parser.get_http_version()
            if http_version != "1.1":
                self.scope["http_version"] = http_version

            if parser.should_upgrade():
                return

            # # Handle 503 responses when 'limit_concurrency' is exceeded.
            # if self.limit_concurrency is not None and (
            #     len(self.connections) >= self.limit_concurrency
            #     or len(self.tasks) >= self.limit_concurrency
            # ):
            #     app = service_unavailable
            #     message = "Exceeded concurrency limit."
            #     self.logger.warning(message)
            # else:
            #     app = self.app

            self.response_started = self.response_complete = False

            if self._send_generator is None:
                _send_generator = self._send_generator_func(keep_alive = http_version != "1.0")
                _send_generator.send(None)
                self._send_generator = _send_generator

            self.run_asgi_event.set()
            # t = self.run_asgi(app)
            # task = self.loop.create_task(self.run_asgi())
            # task.add_done_callback(self.task_discard)
            # self.task_add(task)

    def on_body(self, body: bytes):
        if True: # with self.server_state.measure("on_body"):
            if self.parser.should_upgrade() or self.response_complete:
                return
            self.body += body
            if len(self.body) > HIGH_WATER_LIMIT:
                self.flow.pause_reading()
            self.set_message_event()

    def on_message_complete(self):
        if True: # with self.server_state.measure("on_message_complete"):
            if self.parser.should_upgrade() or self.response_complete:
                return
            self.more_body = False
            self.set_message_event()

    def on_response_complete(self):
        if True: # with self.server_state.measure("on_response_complete"):
            # Callback for pipelined HTTP requests to be started.
            self.server_state.total_requests += 1

            if self.transport.is_closing():
                return

            # Set a short Keep-Alive timeout.
            if timeout_keep_alive_task := self.timeout_keep_alive_task:
                timeout_keep_alive_task.cancel()

            self.timeout_keep_alive_task = self.loop.call_later(
                self.timeout_keep_alive, self.timeout_keep_alive_handler
            )

            # Unpause data reads if needed.
            self.flow.resume_reading()

    def shutdown(self):
        """
        Called by the server to commence a graceful shutdown.
        """
        if True: # with self.server_state.measure("shutdown"):
            if self.response_complete:
                self.transport.close()
            else:
                self.keep_alive = False

    def pause_writing(self):
        """
        Called by the transport when the write buffer exceeds the high water mark.
        """
        if True: # with self.server_state.measure("pause_writing"):
            self.flow.pause_writing()

    def resume_writing(self):
        """
        Called by the transport when the write buffer drops below the low water mark.
        """
        if True: # with self.server_state.measure("resume_writing"):
            self.flow.resume_writing()

    def timeout_keep_alive_handler(self):
        """
        Called on a keep-alive connection if no new data is received after a short
        delay.
        """
        if True: # with self.server_state.measure("timeout_keep_alive_handler"):
            if not self.transport.is_closing():
                self.transport.close()

    # ASGI exception wrapper
    async def run_asgi(self):
        while True:
            await self.run_asgi_event.wait()
            self.run_asgi_event.clear()
            try:
                result = await self.app(self.scope, self.receive, self.send)
            except BaseException as exc:
                msg = "Exception in ASGI application\n"
                self.logger.error(msg, exc_info=exc)
                if not self.response_started:
                    await self.send_500_response()
                else:
                    self.transport.close()
            else:
                if result is not None:
                    msg = "ASGI callable should return None, but returned '%s'."
                    self.logger.error(msg, result)
                    self.transport.close()
                # elif not self.response_started and not self.disconnected:
                #     msg = "ASGI callable returned without starting response."
                #     self.logger.error(msg)
                #     await self.send_500_response()
                elif not self.response_complete and not self.disconnected:
                    msg = "ASGI callable returned without completing response."
                    self.logger.error(msg)
                    self.transport.close()
            finally:
                pass
                # self.on_response = None

    async def send_500_response(self):
        await self.send(
            {
                "type": "http.response.start",
                "status": 500,
                "headers": [
                    (b"content-type", b"text/plain; charset=utf-8"),
                    (b"connection", b"close"),
                ],
            }
        )
        await self.send(
            {"type": "http.response.body", "body": b"Internal Server Error"}
        )

    def _send(self, transport_write, default_headers, keep_alive, on_response):
        while True:
            scope = self.scope
            chunked_encoding = None
            expected_content_length = 0

            message = yield
            method = scope["method"]

            if True: # with self.server_state.measure("_send_start"):

                # Sending response status line and headers
                if message["type"] != "http.response.start":
                    msg = "Expected ASGI message 'http.response.start', but got '%s'."
                    raise RuntimeError(msg % message["type"])

                self.waiting_for_100_continue = False

                status_code = message["status"]
                headers = list(message.get("headers", []))
                headers += default_headers

                if CLOSE_HEADER in scope["headers"] and CLOSE_HEADER not in headers:
                    headers += [CLOSE_HEADER]

                # if self.access_log:
                #     self.access_logger.info(
                #         '%s - "%s %s HTTP/%s" %d',
                #         get_client_addr(scope),
                #         scope["method"],
                #         get_path_with_query_string(scope),
                #         scope["http_version"],
                #         status_code,
                #     )

                transport_write(STATUS_LINE[status_code])
                for name, value in headers:
                    # if HEADER_RE.search(name):
                    #     raise RuntimeError("Invalid HTTP header name.")
                    # if HEADER_VALUE_RE.search(value):
                    #     raise RuntimeError("Invalid HTTP header value.")

                    name = name.lower()
                    if name == b"content-length" and chunked_encoding is None:
                        expected_content_length = int(value)
                        chunked_encoding = False
                    elif name == b"transfer-encoding" and value.lower() == b"chunked":
                        expected_content_length = 0
                        chunked_encoding = True
                    elif name == b"connection" and value.lower() == b"close":
                        keep_alive = False
                    self.transport.writelines((name, b": ", value, b"\r\n"))

                if (
                    chunked_encoding is None
                    and method != "HEAD"
                    and status_code not in (204, 304)
                ):
                    # Neither content-length nor transfer-encoding specified
                    chunked_encoding = True
                    transport_write(b"transfer-encoding: chunked\r\n\r\n")
                else:
                    transport_write(b"\r\n")

            while True:
                message = yield
                if True: # with self.server_state.measure("_send_after_start"):
                    message_type = message["type"]

                    if not self.response_complete:
                        # Sending response body
                        if message_type != "http.response.body":
                            msg = "Expected ASGI message 'http.response.body', but got '%s'."
                            raise RuntimeError(msg % message_type)

                        body = message.get("body", b"")
                        more_body = message.get("more_body", False)

                        # Write response body
                        if method == "HEAD":
                            expected_content_length = 0
                        elif chunked_encoding:
                            if body:
                                content = [b"%x\r\n" % len(body), body, b"\r\n"]
                            else:
                                content = []
                            if not more_body:
                                content.append(b"0\r\n\r\n")
                            transport_write(bytearray().join(content))
                        else:
                            num_bytes = len(body)
                            if num_bytes > expected_content_length:
                                raise RuntimeError("Response content longer than Content-Length")
                            else:
                                expected_content_length -= num_bytes
                            transport_write(body)

                        # Handle response completion
                        if not more_body:
                            if expected_content_length != 0:
                                raise RuntimeError("Response content shorter than Content-Length")
                            self.response_complete = True
                            self.set_message_event()
                            if not keep_alive:
                                self.transport.close()
                            loop = asyncio.get_event_loop()
                            loop.call_soon(on_response)
                            # on_response()
                            break
                    else:
                        # Response already sent
                        msg = "Unexpected ASGI message '%s' sent, after response already completed."
                        raise RuntimeError(msg % message_type)

    # ASGI interface
    async def send(self, message):

        if self.flow.write_paused and not self.disconnected:
            await self.flow.drain()

        if self.disconnected:
            return

        try:
            self._send_generator.send(message)
        except StopIteration:
            pass

    async def receive(self):
        if True: # with self.server_state.measure("receive"):
            if self.waiting_for_100_continue and not self.transport.is_closing():
                self.transport.write(b"HTTP/1.1 100 Continue\r\n\r\n")
                self.waiting_for_100_continue = False

            if not self.disconnected and not self.response_complete:
                self.flow.resume_reading()
                await self.wait_message_event()
                self.clear_message_event()

            if self.disconnected or self.response_complete:
                message = {"type": "http.disconnect"}
            else:
                message = {
                    "type": "http.request",
                    "body": self.body,
                    "more_body": self.more_body,
                }
                self.body = b""

            return message
