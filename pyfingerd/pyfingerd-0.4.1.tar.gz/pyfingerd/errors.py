#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2017-2021 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd project, which is MIT-licensed.
# *****************************************************************************
""" This file defines the exceptions used throughout the module. """

__all__ = [
    'BindError', 'ConfigurationError', 'HostnameError',
    'InvalidBindError', 'MalformedQueryError', 'NoBindsError',
]

# ---
# Configuration-related errors.
# ---


class ConfigurationError(Exception):
    """ Raised when an invalid configuration option is set. """

    pass


class HostnameError(ConfigurationError):
    """ Raised when a host name is invalid. """

    def __init__(self, hostname):
        super().__init__('invalid host name {}.'.format(repr(hostname)))


class BindError(ConfigurationError):
    """ Raised when an error has occurred with the provided binds. """

    def __init__(self, msg):
        super().__init__(
            f'an error has occurred with the provided binds: {msg}')


class NoBindsError(BindError):
    """ Raised when no binds were provided. """

    def __init__(self):
        super().__init__('no valid bind')


class InvalidBindError(BindError):
    """ Raised when one of the provided binds came out erroneous. """

    def __init__(self, bind, msg=None):
        super().__init__(
            f'one of the provided bind ({bind!r}) '
            f'was invalid{": " + msg if msg else ""}',
        )


class MalformedQueryError(Exception):
    """ Raised when a malformed query is received. """

    def __init__(self, query, msg=None):
        self.query = query
        self.msg = msg

        super().__init__(
            msg + (f': {query!r}' if query else '') + '.',
        )

# End of file.
