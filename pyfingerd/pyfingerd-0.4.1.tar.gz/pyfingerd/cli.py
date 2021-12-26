#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2021 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd project, which is MIT-licensed.
# *****************************************************************************
""" pyfingerd CLI interface. """

from datetime import datetime as _datetime
from platform import (
    python_implementation as _python_impl,
    python_version as _python_version,
)
from sys import stderr as _stderr

import click as _click
import coloredlogs as _coloredlogs

from . core import (
    FingerInterface as _FingerInterface,
    FingerServer as _FingerServer,
)
from .fiction import (
    FingerScenario as _FingerScenario,
    FingerScenarioInterface as _FingerScenarioInterface,
)
from .native import FingerNativeInterface as _FingerNativeInterface
from .utils import logger as _logger
from .version import version as _version

__all__ = ['cli']


@_click.command(
    context_settings={
        'help_option_names': ['-h', '--help'],
    },
)
@_click.version_option(
    version=_version,
    message=(
        f'pyfingerd version {_version}, '
        f'running on {_python_impl()} {_python_version()}'
    ),
)
@_click.option(
    '-b', '--binds',
    default='localhost:79', envvar=('BIND', 'BINDS'),
    show_default=True,
    help='Addresses and ports on which to listen to, comma-separated.',
)
@_click.option(
    '-H', '--hostname',
    default='LOCALHOST', envvar=('FINGER_HOST',),
    show_default=True,
    help='Hostname to display to finger clients.',
)
@_click.option(
    '-t', '--type', 'type_',
    default='native', envvar=('FINGER_TYPE',),
    show_default=True,
    help='Interface type for gathering user and session data.',
)
@_click.option(
    '-s', '--scenario',
    default='actions.toml',
    envvar=('FINGER_SCENARIO', 'FINGER_ACTIONS'),
    help="Path to the scenario, if the selected type is 'scenario'.",
)
@_click.option(
    '-S', '--start', 'scenario_start',
    type=_click.DateTime(),
    default=_datetime.now(),
    envvar=('FINGER_START',),
    help=(
        'Date and time at which the scenario starts or has started '
        "as an ISO date, if the selected type is 'scenario'."
    ),
)
@_click.option(
    '-l', '--loglevel', 'log_level',
    default='info', envvar=('FINGER_LOGLEVEL',),
    help='Log level for the displayed messages.',
)
def cli(binds, hostname, type_, scenario, scenario_start, log_level):
    """ Start a finger (RFC 1288) server.

        Find out more at <https://pyfingerd.touhey.pro/>.
    """

    # Set the log level.

    _coloredlogs.install(
        fmt='\r%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        level=log_level.upper(),
    )

    # Do everything.

    hostname = hostname.upper()
    type_ = type_.casefold()

    if type_ == 'native':
        iface = _FingerNativeInterface()
    elif type_ in ('actions', 'scenario'):
        try:
            fic = _FingerScenario.load(scenario)
            iface = _FingerScenarioInterface(fic, scenario_start)
        except (FileNotFoundError, PermissionError) as exc:
            _logger.error(str(exc))
            return 1
        except ValueError as exc:
            exc = str(exc)
            _logger.error('Error loading the scenario:')
            _logger.error(f'{exc[0].upper()}{exc[1:]}.')
            return 1
    elif type_ != 'dummy':
        print(
            'warning: unknown interface type, falling back on dummy',
            file=_stderr,
        )
    else:
        iface = _FingerInterface()

    server = _FingerServer(
        binds=binds, hostname=hostname, interface=iface,
    )
    server.serve_forever()

# End of file.
