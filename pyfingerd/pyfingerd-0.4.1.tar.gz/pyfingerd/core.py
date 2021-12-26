#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2017-2021 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd project, which is MIT-licensed.
# *****************************************************************************
""" Main classes for the finger server, interfaces and formatters.

    These classes, which behave as base returning default data,
    are bundled with base definitions for users and sessions.
"""

import asyncio as _asyncio
import copy as _copy
import multiprocessing as _multip
import signal as _signal
import socket as _socket
import string as _string

from collections.abc import Sequence as _Sequence
from datetime import datetime as _dt, timedelta as _td, tzinfo as _tzinfo
from enum import Enum as _Enum
from errno import errorcode as _errorcode
from typing import Optional as _Optional

from croniter import croniter as _croniter
from pytz import utc as _utc

from .errors import (
    HostnameError as _HostnameError,
    InvalidBindError as _InvalidBindError,
    MalformedQueryError as _MalformedQueryError,
    NoBindsError as _NoBindsError,
)
from .utils import (
    access_logger as _access_logger,
    error_logger as _error_logger,
    logger as _logger,
)

__all__ = [
    'FingerFormatter', 'FingerInterface',
    'FingerServer', 'FingerSession', 'FingerUser', 'cron',
]

# ---
# Decorators.
# ---


def cron(spec: str):
    """ Add a cron specification to the callable.

        This decorator adds the ``__cron__`` member on the callable,
        as a ``croniter`` instance using the given specification.

        This makes the callable identifiable by the finger server when
        starting a server with an interface with such a callable,
        by checking if the attribute exists and starting a dedicated
        coroutine for running it periodically using the given specification.
    """

    spec = _croniter(spec)

    def decorator(func):
        func.__cron__ = spec
        return func

    return decorator


# ---
# Basic representations.
# ---


class FingerSession:
    """ Representation of an active session for a given user on the system.

        :param time: The start time of the given session;
                     by default, the current datetime.
    """

    __slots__ = ('_start', '_line', '_host', '_idle')

    def __init__(self, *_, time: _Optional[_dt] = None):
        self._start = _dt.now()
        self._idle = None
        self._line = None
        self._host = None

        self.start = time
        self._idle = self._start

    def __repr__(self):
        p = ('start', 'idle', 'line', 'orig')
        p = (
            f'{x}={getattr(self, x)!r}'
            for x in p if getattr(self, x) is not None)
        return f"{self._class__.__name__}({', '.join(p)})"

    @property
    def start(self) -> _dt:
        """ The timestamp at which the session has started.

            Note that when set, if no timezone is present,
            the datetime is considered UTC.
        """

        return self._start

    @start.setter
    def start(self, value):
        value = value if isinstance(value, _dt) else _dt(value)
        if value.tzinfo is None:
            value = value.replace(tzinfo=_utc)

        self._start = value

    @property
    def idle(self) -> _dt:
        """ The timestamp since which the user is idle on the session.

            Note that when set, if no timezone is present,
            the datetime is considered UTC; also, if the provided
            datetime is before the session start timestamp, it is
            set to it.
        """

        return self._idle

    @idle.setter
    def idle(self, value):
        value = value if isinstance(value, _dt) else _dt(value)
        if value.tzinfo is None:
            value = value.replace(tzinfo=_utc)

        if value < self._start:
            value = self._start

        self._idle = value

    @property
    def line(self) -> _Optional[str]:
        """ The line on which the user is. """

        return self._line

    @line.setter
    def line(self, value):
        self._line = None if value is None else str(value)

    @property
    def host(self) -> _Optional[str]:
        """ The host from which the user is connected. """

        return self._host

    @host.setter
    def host(self, value):
        self._host = None if value is None else str(value)


class FingerUser:
    """ Representation of a user on the system.

        Returned by subclasses of :py:class:`FingerInterface`,
        and used by subclasses of :py:class:`FingerFormatter`.

        :param login: The login of the user.
        :param name: The display name of the user.
        :param home: The path to the home of the user.
        :param shell: The path to the user's default shell.
    """

    __slots__ = (
        '_login', '_name', '_home', '_shell', '_office',
        '_plan', '_last_login', '_sessions',
    )

    def __init__(
        self, *_,
        login: _Optional[str] = None,
        name: _Optional[str] = None,
        home: _Optional[str] = None,
        shell: _Optional[str] = None,
    ):
        self._login = None
        self._name = ''
        self._home = None
        self._shell = None
        self._office = None
        self._plan = None
        self._last_login = None
        self._sessions = _FingerSessionManager()

        self.login = login
        self.name = name
        self.home = home
        self.shell = shell

    def __repr__(self):
        p = (
            'login', 'name', 'home', 'shell', 'office',
            'last_login', 'sessions')
        p = (
            f'{x}={getattr(self, x)!r}'
            for x in p if getattr(self, x) is not None)
        return f"{self._class__.__name__}({', '.join(p)})"

    @property
    def login(self) -> _Optional[str]:
        """ The login name of the user, e.g. 'cake' or 'gaben'. """

        return self._login

    @login.setter
    def login(self, value: _Optional[str]) -> None:
        self._login = value

    @property
    def name(self) -> _Optional[str]:
        """ The display name of the user, e.g. 'Jean Dupont'. """

        return self._name

    @name.setter
    def name(self, value: _Optional[str]) -> None:
        self._name = value

    @property
    def last_login(self) -> _Optional[str]:
        """ The last login date for the user.

            Is None if not known.
        """

        return self._last_login

    @last_login.setter
    def last_login(self, value: _Optional[str]) -> None:
        self._last_login = None if value is None else \
            value if isinstance(value, _dt) else _dt(value)

    @property
    def home(self) -> _Optional[str]:
        """ The path to the user's home on the given system.

            Is None if not known or defined.
        """

        return self._home

    @home.setter
    def home(self, value: _Optional[str]) -> None:
        self._home = None if value is None else str(value)

    @property
    def shell(self) -> _Optional[str]:
        """ The path to the user's shell on the given system.

            Is None if not known or defined.
        """

        return self._shell

    @shell.setter
    def shell(self, value: _Optional[str]) -> None:
        self._shell = None if value is None else str(value)

    @property
    def office(self) -> _Optional[str]:
        """ The display name of the user's office.

            Is None if not known or defined.
        """

        return self._office

    @office.setter
    def office(self, value: _Optional[str]) -> None:
        self._office = None if value is None else str(value)

    @property
    def plan(self) -> _Optional[str]:
        """ The plan of the user.

            Usually the content of the ``.plan`` file in the user's home
            on real (and kind of obsolete) UNIX-like systems.
        """

        return self._plan

    @plan.setter
    def plan(self, value: _Optional[str]) -> None:
        if value is None:
            self._plan = None
        else:
            value = str(value)
            self._plan = '\n'.join(value.splitlines())

    @property
    def sessions(self) -> _Sequence[FingerSession]:
        """ The current sessions array for the user, always defined. """

        return self._sessions


class _FingerSessionManager:
    """ Session manager. """

    __slots__ = ('_sessions',)

    def __init__(self):
        self._sessions = []

    def __repr__(self):
        return repr(self._sessions)

    def __bool__(self):
        return bool(self._sessions)

    def __iter__(self):
        return iter(self._sessions[::-1])

    def __len__(self):
        return len(self._sessions)

    def __delitem__(self, key):
        if key is None:
            self._sessions.pop(0)
        else:
            for i in ([
                i for i, x in enumerate(self._sessions)
                if key == x.name
            ][::-1]):
                self._sessions.pop(i)

    def __getitem__(self, key):
        if key is None:
            try:
                return self._sessions[0]
            except IndexError:
                raise KeyError('could not get latest session') from None

        if type(key) is int:
            try:
                return self._sessions[key]
            except IndexError:
                msg = f'could not get session #{key!r}'
                raise IndexError(msg) from None

        try:
            return next(x for x in self._sessions if key == x.name)
        except StopIteration:
            raise KeyError(f'could not get session {key!r}') from None

    def __setitem__(self, key, value):
        if not isinstance(value, FingerSession):
            raise TypeError('can only add sessions into a session manager')
        value = _copy.deepcopy(value)

        if key is None:
            # Check if except the first session, the key of the session,
            # if any, does not override another key.

            if value.name is not None:
                try:
                    next(
                        i for i, x in self._sessions[1:]
                        if value.name == x.name)
                except StopIteration:
                    pass
                else:
                    msg = "value.name overrides another session's key"
                    raise ValueError(msg) from None

            try:
                self._sessions[0] = value
                return
            except IndexError:
                raise KeyError('could not set latest session') from None

        if type(key) is int:
            # Check if except the key-th session, the key of the session,
            # if any, does not override another key.

            if value.name is not None:
                try:
                    next(
                        i for i, x in self._sessions
                        if i != key and value.name == x.name)
                except StopIteration:
                    pass
                else:
                    msg = "value.name overrides another session's key"
                    raise ValueError(msg) from None

            try:
                self._sessions[key] = value
                return
            except IndexError:
                msg = f'could not set session #{key!r}'
                raise IndexError(msg) from None

        value.name = key

        try:
            i = next(
                i for i, x in enumerate(self._sessions)
                if key == x.name)
        except StopIteration:
            raise KeyError(f'could not set session {key!r}') from None

        self._sessions[i] = value

    def add(self, session):
        """ Add a session. """

        if not isinstance(session, FingerSession):
            raise TypeError(
                'can only insert sessions into a session manager',
            )

        self._sessions.insert(0, session)

# ---
# Formatter base class.
# ---


class FingerFormatter:
    """ Formatter for :py:class:`FingerServer`.

        Provides text-formatted (as strings limited to ASCII)
        answers for given queries with given results as objects.

        This class must be subclassed by other formatters.
        Only methods not starting with an underscore are called by
        instances of :py:class:`FingerServer`; others are utilities
        called by these.

        Unless methods are overridden to have a different behaviour,
        this formatter aims at RFC 1288 compliance.

        :param tzinfo: Timezone used for formatting dates and times.
    """

    def __init__(self, tzinfo: _Optional[_tzinfo] = None):
        if tzinfo is None:
            tzinfo = _dt.now().astimezone().tzinfo
        self._tzinfo = tzinfo

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    # ---
    # Internal formatting utilities.
    # ---

    def _format_idle(self, idle: _td) -> str:
        """ Format an idle time delta. """

        def _iter_idle(idle):
            days = int(idle.days)
            hours = int(idle.seconds / 3600)
            mins = int(idle.seconds % 3600 / 60)
            secs = int(idle.seconds % 60)

            if days:
                yield f'{days} day{("", "s")[days > 1]}'
            if hours:
                yield f'{hours} hour{("", "s")[hours > 1]}'
            if mins:
                yield f'{mins} minute{("", "s")[mins > 1]}'
            if secs:
                yield f'{secs} second{("", "s")[secs > 1]}'

        return f'{" ".join(_iter_idle(idle))} idle'

    def _format_time(self, d: _td) -> str:
        """ Format a date and time. """

        if d < _td():
            return ''

        days = int(d.days)
        hours = int(d.seconds / 3600)
        mins = int(d.seconds % 3600 / 60)

        if days:
            return f'{days}d'
        elif hours or mins:
            return f'{hours:02}:{mins:02}'

        return ''

    def _format_when(self, d: _dt) -> str:
        """ Format a date and time for 'when'. """

        return d.astimezone(self._tzinfo).strftime('%a %H:%M')

    def _format_header(self, hostname: str, raw_query: str) -> str:
        """ Return the header of the formatted answer.

            This header is used for every request,
            except when an error has occurred in the user's query.

            :param hostname: The hostname configured for the server.
            :param raw_query: The raw query given by the user.
            :return: The header of the formatted answer as text.
        """

        if raw_query:
            raw_query = ' ' + raw_query

        return (
            f'Site: {hostname}\r\n'
            f'Command line:{raw_query}\r\n'
            '\r\n'
        )

    def _format_footer(self) -> str:
        """ Return the footer of the formatted answer.

            This footer is used for every request,
            except when an error has occurred in the user's query.

            :return: The footer of the formatted answer as text.
        """

        return ''

    # ---
    # Used formatting functions.
    # ---

    def format_query_error(self, hostname: str, raw_query: str) -> str:
        """ Return the formatted answr for when an error has occurred.

            :param hostname: The hostname configured for the server.
            :param raw_query: The raw query given by the user.
            :return: The formatted answer as text.
        """

        return (
            f'Site: {hostname}\r\n'
            'You have made a mistake in your query!\r\n'
        )

    def format_short(
        self,
        hostname: str,
        raw_query: str,
        users: _Sequence[FingerUser],
    ) -> str:
        """ Return the formatted answer for a user list in the 'short' format.

            :param hostname: The hostname configured for the server.
            :param raw_query: The raw query given by the user.
            :param users: The user list.
            :return: The formatted answer as text.
        """

        if not users:
            return 'No user list available.\r\n'

        now = _dt.now().astimezone()

        lst = []
        for user in users:
            if not user.sessions:
                lst.append((user, None))
            for session in user.sessions:
                lst.append((user, session))

        def _login(u, s):
            return u.login

        def _name(u, s):
            return u.name

        def _line(u, s):
            return s.line if s and s.line else ''

        def _idle(u, s):
            return self._format_time(now - s.idle) if s else ''

        def _logt(u, s):
            return self._format_when(s.start) if s else ''

        def _offic(u, s):
            return (
                f'({s.host})' if s.host
                else u.office if u.office else '')

        columns = (
            ('Login',) + tuple(_login(u, s) for u, s in lst),
            ('Name',) + tuple(_name(u, s) for u, s in lst),
            ('TTY',) + tuple(_line(u, s) for u, s in lst),
            ('Idle',) + tuple(_idle(u, s) for u, s in lst),
            ('When',) + tuple(_logt(u, s) for u, s in lst),
            ('Office',) + tuple(_offic(u, s) for u, s in lst))

        sizes = tuple(max(map(len, c)) + 1 for i, c in enumerate(columns))
        align = ('<', '<', '<', '^', '^', '<')

        lines = []
        for line in range(len(columns[0])):
            lines.append(' '.join(
                f'{columns[i][line][:sizes[i]]:{align[i]}{sizes[i]}}'
                for i in range(len(columns))
            ))

        return (
            self._format_header(hostname, raw_query)
            + '\r\n'.join(lines) + '\r\n'
            + self._format_footer()
        )

    def format_long(
        self,
        hostname: str,
        raw_query: str,
        users: _Sequence[FingerUser],
    ) -> str:
        """ Return the formatted answer for a user list in the 'long' format.

            :param hostname: The hostname configured for the server.
            :param raw_query: The raw query given by the user.
            :param users: The user list.
            :return: The formatted answer as text.
        """

        if not users:
            return 'No user list available.\r\n'

        now = _dt.now().astimezone()
        res = ''

        for user in users:
            res += (
                f'Login name: {user.login[:27]:<27} '
                f'Name: {user.name if user.name else user.login}\r\n'
                f'Directory: {user.home[:28] if user.home else "":<28} '
                f'Shell: {user.shell if user.shell else ""}\r\n'
            )
            if user.office:
                res += f"Office: {user.office if user.office else ''}\r\n"

            if user.sessions:
                # List current sessions.

                for se in user.sessions:
                    since = (
                        se.start.astimezone(self._tzinfo)
                        .strftime('%a %b %e %R')
                    )
                    tz = self._tzinfo
                    res += f'On since {since} ({tz})'
                    if se.line is not None:
                        res += f' on {se.line}'
                    if se.host is not None:
                        res += f' from {se.host}'
                    res += '\r\n'

                    idle = now - se.idle
                    if idle >= _td(seconds=4):
                        res += f'   {self._format_idle(idle)}\r\n'
            elif user.last_login is not None:
                # Show last login.

                date = (
                    user.last_login.astimezone(self._tzinfo)
                    .strftime('%a %b %e %R'))
                tz = self._tzinfo
                res += f'Last login {date} ({tz}) on console\r\n'
            else:
                res += 'Never logged in.\r\n'

            if user.plan is None:
                res += 'No plan.\r\n'
            else:
                res += 'Plan:\r\n'
                res += '\r\n'.join(user.plan.splitlines())
                res += '\r\n'

            res += '\r\n'

        return (
            self._format_header(hostname, raw_query)
            + res + self._format_footer()
        )

# ---
# Interface (dummy) base class.
# ---


class FingerInterface:
    """ Data source for :py:class:`FingerServer`.

        Provides users and answers for the various queries received
        from the clients by the server.

        This class must be subclassed by other interfaces.
        Only methods not starting with an underscore are called by
        instances of :py:class:`FingerServer`; others are utilities
        called by these.

        By default, it behaves like a dummy interface.
    """

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def transmit_query(
        self,
        query: _Optional[str],
        host: str,
        verbose: bool,
    ) -> str:
        """ Transmit a user query to a foreign host.

            This function returns the answer formatted by it.

            If used directly (not overridden by subclasses), this
            method will refuse to transmit finger queries.

            :param query: The user query, set to None in case of
                          no query provided by the client.
            :param host: The distant host to which to transmit the
                         query.
            :param verbose: Whether the verbose flag (``/W``, long format)
                            has been passed by the current client
                            or not.
            :return: The answer formatted by the distant server.
        """

        return "This server won't transmit finger queries.\r\n"

    def search_users(
        self,
        query: _Optional[str],
        active: _Optional[bool],
    ) -> _Sequence[FingerUser]:
        """ Search for users on the current host using the given query.

            :param query: The user query, set to None in case of no
                          query provided by the client.
            :param active: Whether to get active users (True),
                           inactive users (False), or all users (None).
            :return: The list of users found using the query provided
                     by the client.
        """

        return []


# ---
# Bind-related configuration.
# ---


class _BindAddress:
    """ Bind address for pyfingerd. """

    class Type(_Enum):
        """ Bind address type. """

        """ TCP on IPv4 bind. """
        TCP_IPv4 = 1

        """ TCP on IPv6 bind. """
        TCP_IPv6 = 2

    def __init__(self, family):
        self._family = self.Type(family)

    def __repr__(self):
        return f'{self._class__.__name__}(family={self._family!r})'

    @property
    def family(self):
        """ Family as one of the `BindAddress.Type` enumeration values. """

        return self._family


class _TCP4Address(_BindAddress):
    """ IPv4 TCP Address. """

    def __init__(self, address, port):
        super().__init__(_BindAddress.Type.TCP_IPv4)

        try:
            self._addr = _socket.inet_pton(_socket.AF_INET, address)
        except Exception:
            self._addr = address

        self._port = port

    @property
    def runserver_params(self):
        """ Return the data as `_runserver` parameters. """

        return (
            _socket.AF_INET,
            _socket.inet_ntop(_socket.AF_INET, self._addr),
            self._port)


class _TCP6Address(_BindAddress):
    """ IPv6 TCP Address. """

    def __init__(self, address, port):
        super().__init__(_BindAddress.Type.TCP_IPv6)

        try:
            self._addr = _socket.inet_pton(_socket.AF_INET6, address)
        except Exception:
            self._addr = address

        self._port = port

    @property
    def runserver_params(self):
        """ Return the data as `_runserver` parameters. """

        return (
            _socket.AF_INET6,
            _socket.inet_ntop(_socket.AF_INET6, self._addr),
            self._port,
        )


class _BindsDecoder:
    """ Binds decoder for pyfingerd.

        Takes a raw string and the protocol name, either 'finger' (the base
        protocol managed by the class) or 'pyfingerd-control' (the protocol
        used for controlling the live pyfingerd interface).
    """

    def __init__(self, raw, proto='finger'):
        proto = proto.casefold()
        if proto not in ('finger',):
            raise ValueError(f'unsupported protocol {proto}')

        self._binds = set()

        for x in map(lambda x: x.strip(), raw.split(',')):
            addr = x

            # Try to find a scheme.

            scheme, *rest = x.split(':/')
            if not rest:
                # No scheme found, let's just guess the scheme based on
                # the situation.

                x = scheme
                scheme = {'finger': 'tcp'}[proto]
            else:
                # just don't add the ':' of ':/' again
                x = '/' + ':/'.join(rest)

            if (
                (proto == 'finger' and scheme != 'tcp')
                or scheme not in ('tcp',)
            ):
                raise _InvalidBindError(
                    addr,
                    f'Unsupported scheme {scheme!r} for protocol {proto!r}',
                )

            # Decode the address data.

            if scheme == 'tcp':
                self._binds.update(self._decode_tcp_host(x))

        self._binds = tuple(self._binds)

    def __iter__(self):
        return iter(self._binds)

    def __repr__(self):
        return f'{self._class__.__name__}(binds={self._binds})'

    def _decode_tcp_host(self, x):
        """ Decode suitable hosts for a TCP bind. """

        addrs = ()
        addr = x

        # TODO: manage the '*' case.

        # Get the host part first, we'll decode it later.

        if x[0] == '[':
            # The host part is an IPv6, look for the closing ']' and
            # decode it later.

            to = x.find(']')
            if to < 0:
                raise _InvalidBindError(
                    addr, "Expected closing ']'")

            host = x[1:to]
            x = x[to + 1:]

            is_ipv6 = True
        else:
            # The host part is either an IPv4 or a host name, look for
            # the ':' and decode it later.

            host, *x = x.split(':')
            x = ':' + ':'.join(x)

            is_ipv6 = False

        # Decode the port part.

        if x == '':
            port = 79
        elif x[0] == ':':
            try:
                port = int(x[1:])
            except ValueError:
                try:
                    if x[1:] != '':
                        raise AssertionError('Expected a port number')
                    port = _socket.getservbyname(x[1:])
                except Exception:
                    raise _InvalidBindError(
                        addr,
                        'Expected a valid port number or name '
                        f'(got {x[1:]!r})',
                    ) from None
        else:
            raise _InvalidBindError(
                addr, 'Garbage found after the host',
            )

        # Decode the host part and get the addresses.

        addrs = ()
        if is_ipv6:
            # Decode the IPv6 address (validate it using `_socket.inet_pton`).

            ip6 = host
            _socket.inet_pton(_socket.AF_INET6, host)
            addrs += (_TCP6Address(ip6, port),)
        else:
            # Decode the host (try IPv4, otherwise, resolve domain).

            try:
                ip = host.split('.')
                if len(ip) < 2 or len(ip) > 4:
                    raise AssertionError('2 <= len(ip) <= 4')

                ip = list(map(int, ip))
                if not all(lambda x: 0 <= x < 256, ip):
                    raise AssertionError('non-8-bit component')

                if len(ip) == 2:
                    ip = [ip[0], 0, 0, ip[1]]
                elif len(ip) == 3:
                    ip = [ip[0], 0, ip[1], ip[2]]

                addrs += (_TCP4Address(ip, port),)
            except Exception:
                entries = _socket.getaddrinfo(
                    host, port,
                    proto=_socket.IPPROTO_TCP,
                    type=_socket.SOCK_STREAM)

                for ent in entries:
                    if (
                        ent[0] not in (_socket.AF_INET, _socket.AF_INET6)
                        or ent[1] not in (_socket.SOCK_STREAM,)
                    ):
                        continue

                    if ent[0] == _socket.AF_INET:
                        ip = ent[4][0]
                        _socket.inet_pton(_socket.AF_INET, ent[4][0])
                        addrs += (_TCP4Address(ip, port),)
                    else:
                        ip6 = ent[4][0]
                        _socket.inet_pton(_socket.AF_INET6, ent[4][0])
                        addrs += (_TCP6Address(ip6, port),)

        return addrs


# ---
# Finger/TCP server implementation.
# ---


class _FingerQuery:
    """ A finger query.

        Requests information about connected or specific users on a
        remote server.

        There are three types of requests recognized by RFC 1288:

         * {C} is a request for a list of all online users.
         * {Q1} is a request for a local user.
         * {Q2} is a request for a distant user (with hostname).

        /W means the RUIP (program answering the query) should be more
        verbose (this token can be ignored).
    """

    __slots__ = ('line', 'host', 'username', 'verbose')

    # "By default, this program SHOULD filter any unprintable data,
    #  leaving only printable 7-bit characters (ASCII 32 through
    #  ASCII 126), tabs (ASCII 9) and CRLFs."

    allowed_chars = (
        "\t !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        + _string.ascii_letters + _string.digits)

    def __init__(self, raw):
        """ Initialize the query object by decoding the data. """

        # Get a character string out of the query.

        raw = raw.decode('ascii', errors='ignore')
        raw = ''.join(c for c in raw if c in self.allowed_chars)
        self.line = raw

        # Get elements.

        self.host = None
        self.username = None
        self.verbose = False
        for element in raw.split():
            if element[0] == '/':
                if not element[1:]:
                    raise _MalformedQueryError(
                        raw, "missing feature flags after '/'",
                    )
                for letter in element[1:]:
                    if letter == 'W':
                        self.verbose = True
                    else:
                        raise _MalformedQueryError(
                            raw,
                            f'unknown feature flag {letter!r}',
                        )
                continue
            elif self.username is not None:
                raise _MalformedQueryError(raw, 'multiple query arguments')
            self.username = element

        if self.username is not None and '@' in self.username:
            self.host, *self.username = self.username.split('@')[::-1]
            self.username = '@'.join(self.username[::-1])


class FingerServer:
    """ The main finger server class.

        :param binds: The hosts and ports on which the server should
                      listen to and answer finger requests.
        :param hostname: The hostname to be included in answers sent
                         to clients.
        :param interface: The interface to use for querying
                          users and sessions.
        :param formatter: The formatter to use for formatting
                          answers sent to clients.
    """

    def __init__(
        self,
        binds: str = 'localhost:79',
        hostname: str = 'LOCALHOST',
        interface: FingerInterface = FingerInterface(),
        formatter: FingerFormatter = FingerFormatter(),
    ):
        # Check the host name, which should be simple LDH, i.e.
        # Letters, Digits, Hyphens.

        try:
            hostname = hostname.upper()
            if not all(
                c in _string.ascii_letters + _string.digits + '.-'
                for c in hostname
            ):
                raise AssertionError('Non-LDH hostname')
        except Exception:
            raise _HostnameError(hostname)

        # Check the interface and formatter classes.

        if not isinstance(interface, FingerInterface):
            raise TypeError(
                'Please base your interface '
                'on the base class provided by the pyfingerd module',
            )

        if not isinstance(formatter, FingerFormatter):
            raise TypeError(
                'Please base your formatter '
                'on the base class provided by the pyfingerd module',
            )

        # Keep the parameters.

        self._host = hostname
        self._interface = interface
        self._formatter = formatter

        # Check the binds.

        self._binds = [b for b in _BindsDecoder(binds)]
        if not self._binds:
            raise _NoBindsError()

        # Initialize multi-process related.

        self._p = None

    @property
    def hostname(self):
        """ The hostname configured for this server. """

        return self._host

    @property
    def interface(self):
        """ The interface configured for this server. """

        return self._interface

    @property
    def formatter(self):
        """ The formatter configured for this server. """

        return self._formatter

    def _serve(self):
        """ Start servers and serve on the current process. """

        async def handle_connection(inp, outp):
            """ Handle a new incoming connection. """

            src, *_ = inp._transport.get_extra_info('peername')

            # Gather the request line.

            try:
                line = await inp.readline()
            except ConnectionResetError:
                _error_logger.info(
                    f'{src} submitted no query. (possible scan)',
                )
                outp.close()
                return

            # Decode the request.

            ans = ''

            try:
                query = _FingerQuery(line)
            except _MalformedQueryError as e:
                _error_logger.info(
                    f'{src} made a bad request: {e.msg} in {e.query!r}.',
                )
                ans = self.formatter.format_query_error(
                    self.hostname, line,
                )
            else:
                if query.host is not None:
                    if query.username:
                        _access_logger.info(
                            f'{src} requested transmitting user query for '
                            f'{query.username!r} at {query.host!r}.',
                        )
                    else:
                        _access_logger.info(
                            f'{src} requested transmitting user query '
                            f'to {query.host!r}.',
                        )

                    ans = self.interface.transmit_query(
                        query.host, query.username, query.verbose)
                else:
                    if query.username:
                        users = self.interface.search_users(
                            query.username, None)
                        _access_logger.info(
                            f'{src} requested user {query.username!r}: found '
                            + (
                                {0: 'no user', 1: '1 user'}
                                .get(len(users), f'{len(users)} users')
                            )
                            + '.',
                        )
                    else:
                        users = self.interface.search_users(None, True)
                        _access_logger.info(
                            f'{src} requested connected users: found '
                            + (
                                {0: 'no user', 1: '1 user'}
                                .get(len(users), f'{len(users)} users')
                            )
                            + '.',
                        )

                    if query.username or query.verbose:
                        ans = self.formatter.format_long(
                            self.hostname, query.line, users)
                    else:
                        ans = self.formatter.format_short(
                            self.hostname, query.line, users)

            # Write the output.

            ans = '\r\n'.join(ans.splitlines()) + '\r\n'
            outp.write(ans.encode('ascii', errors='ignore'))
            outp.close()
            await outp.wait_closed()

        async def start_server(bind):
            """ Start a given server. """

            family, host, port = bind.runserver_params

            try:
                server = await _asyncio.start_server(
                    handle_connection,
                    host=host, port=port, family=family,
                    reuse_address=True,
                )
            except (OSError, PermissionError) as exc:
                if isinstance(exc, PermissionError):
                    name = 'EACCES'
                else:
                    name = _errorcode[exc.errno]

                if name == 'EADDRINUSE':
                    _logger.error(
                        f'Could not bind to [{host}]:{port}: '
                        'address already in use.',
                    )
                    return
                elif name == 'EACCES':
                    _logger.error(
                        f'Could not bind to [{host}]:{port}: '
                        f'port {port} privileged port and process '
                        'is unprivileged.',
                    )
                else:
                    raise
            else:
                _logger.info(
                    f'Starting pyfingerd on [{host}]:{port}.',
                )

                try:
                    await server.serve_forever()
                except _asyncio.CancelledError:
                    pass

                _logger.info(
                    f'Stopping pyfingerd on [{host}]:{port}.',
                )

        async def cron_call(func, spec):
            """ Call a function periodically using a cron specification. """

            spec.set_current(_dt.now())

            while True:
                try:
                    func()
                except SystemExit:
                    return

                while True:
                    seconds = (
                        spec.get_next(_dt) - _dt.now()
                    ).total_seconds()
                    if seconds >= 0:
                        break

                await _asyncio.sleep(seconds)  # TODO

        async def start_servers():
            """ Start the servers. """

            def get_coroutines():
                """ Tasks iterator. """

                for bind in self._binds:
                    yield start_server(bind)

                for key in dir(self.interface):
                    member = getattr(self.interface, key)
                    if not callable(member):
                        continue

                    try:
                        spec = member.__cron__
                    except AttributeError:
                        continue

                    if not isinstance(spec, _croniter):
                        continue

                    yield cron_call(member, spec)

            tasks = [_asyncio.create_task(co) for co in get_coroutines()]
            await _asyncio.wait(
                tasks, return_when=_asyncio.FIRST_COMPLETED)

            # If any task has set an exception, we try to catch it.

            exc = None
            for task in tasks:
                if exc is None:
                    try:
                        exc = task.exception()
                    except _asyncio.exceptions.InvalidStateError:
                        exc = None

                task.cancel()

            if exc is not None:
                raise exc

        try:
            _asyncio.run(start_servers())
        except KeyboardInterrupt:
            pass

    def start(self) -> None:
        """ Start all underlying server processes and bind all ports. """

        if self._p is not None and self._p.is_alive():
            return

        self._p = _multip.Process(target=self._serve)
        self._p.start()

    def stop(self) -> None:
        """ Stop all underlying server processes and unbind all ports. """

        if self._p is None or not self._p.is_alive():
            return

        self._p.kill()
        self._p.join()
        self._p = None

    def serve_forever(self) -> None:
        """ Start all servers and serve in a synchronous fashion.

            It starts all servers :py:meth:`FingerServer.start`, waits for
            an interrupt signal, and stops all servers using
            :py:meth:`FingerServer.stop`.
        """

        if self._p is not None:
            self.start()

            try:
                while True:
                    _signal.pause()
            except KeyboardInterrupt:
                pass

            self.stop()
        else:
            # If the server hasn't been started on another process
            # using ``.start()``, we can just start is on this process.

            self._serve()

    def shutdown(self):
        """ Shutdown the server, alias to `.stop()`. """

        self.stop()

# End of file.
