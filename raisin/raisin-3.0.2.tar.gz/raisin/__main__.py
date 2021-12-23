#!/usr/bin/env python3

"""
** Allows to use *raisin* in command line. **
---------------------------------------------

- Launch the server: ``python3 -m raisin server``
"""


import argparse
import sys

from raisin.communication.server import Server
from raisin.application import PORT


def parse():
    """
    ** Does the parsing of the arguments. **
    """
    parser = argparse.ArgumentParser(description='simple raisin API')
    subparsers = parser.add_subparsers(dest='parser_name')
    parser.add_argument(
        '-R',
        '--raise',
        action='store_true',
        default=False,
        help='raises exceptions instead of transforming them into error code',
    )

    subparsers.add_parser('server', help='launch tasks in background')

    return parser


def catch_error(func):
    """
    ** Decorator that transforms python output to bash output. **

    - If the function raises an exception, returns a non-zero
        integer that corresponds the error code.
    - If the function does not raise an exception, the decorated function returns 0.
    - Only catches errors derived from *Exception*, not *BaseException*.
    - If the function returns something other than None,
        the output is intercepted and displayed in the stdout.

    Parameters
    ----------
    func : callable
        The function to decorate.

    Returns
    -------
    decorated_func : callable
        The decorate function which performs the same thing but can
        handle exceptions and output value differently.
    """

    def fonc_dec(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as err:
            sys.stderr.write(f'{err.__class__.__name__}: {err}\n')
            return 1
        else:
            if res is not None:
                print(res)
            return 0

    return fonc_dec


def _start_server():
    with Server(PORT) as server:
        server.serve_forever()


def main(args_list=None):
    """
    ** Interprets the commands. **

    Allows you to use *raisin* on the command line.

    Parameters
    ----------
    args : list
        The list of arguments provided.

    Returns
    -------
    func_out
        The output of the called functions.
    """

    def run(args):
        if args.parser_name == 'server':
            return _start_server()
        raise SyntaxError(
            f"invalid argument, for more information enter '{sys.executable} -m raisin --help'"
        )

    @catch_error
    def run_e(*args, **kwargs):
        return run(*args, **kwargs)

    # arguments parsing
    parser = parse()
    if args_list is not None:
        args = parser.parse_args(args_list)
    else:
        args = parser.parse_args()

    if getattr(args, 'raise'):
        return run(args)
    return run_e(args)


if __name__ == '__main__':
    main()
