import logging
import logging.handlers
import argparse

_logging_format = logging.Formatter(
    '(%(asctime)s)[%(levelname)8s] %(name)s || %(message)s',
    '%Y-%m-%d %H:%M:%S')


def add_verbosity_flag(parser: argparse.ArgumentParser):
    """Add a --verbose/-v flag to an argparse.ArgumentParser.

    Args:
        parser (argparse.ArgumentParser): The argument parser to be updated.

    Example:
        This should be invoked like the following:
        >>> import uologging
        >>> import argparse
        >>> parser = argparse.ArgumentParser()
        >>> uologging.add_verbosity_flag(parser)

        When parsing args, the verbosity_flag will be set if --verbose/-v is passed!
        >>> args = parser.parse_args(['-vv'])
        >>> args.verbosity_flag
        2

        The verbosity_flag is intended to be used as input for set_logging_verbosity().
    """
    parser.add_argument(
        '-v', '--verbose',
        dest='verbosity_flag',
        action='count',
        default=0,
        help='Logging verbosity. "-vv" results in maximum logging.'
    )


def get_default_parser():
    """Provides an argparse ArgumentParser configured to take --verbose/-v flag.

    Returns:
        argparse.ArgumentParser: Provides a --verbose/-v flag. Should be used as a 'parent parser.'

    Example:
        This should be invoked like the following:
        >>> import uologging
        >>> import argparse
        >>> parser = argparse.ArgumentParser(parents=[uologging.get_default_parser()])

        The parser has been configured with the uologging default_parser as a parent parser.
        When parsing args, the verbosity_flag will be set if --verbose/-v is passed!
        >>> args = parser.parse_args(['-vv'])
        >>> args.verbosity_flag
        2

        The verbosity_flag is intended to be used as input for set_logging_verbosity().
    """
    parser = argparse.ArgumentParser(add_help=False)
    add_verbosity_flag(parser)
    return parser


def init_syslog_logging(package):
    """Setup logging to be output to syslog (via /dev/log).

    Args:
        package (str): The package you are interested in tracing.

    Example:
        Call this method with your package's name as the parameter.
        >>> import uologging
        >>> uologging.init_syslog_logging('examplepkg')

        Then use the Python logging package in each of your package's modules.
        >>> import logging
        >>> logger = logging.getLogger(__name__)

        We use a hardcoded str here to enable this doctest:
        >>> logger = logging.getLogger('examplepkg.just.testing')
        >>> logger.critical('Just kidding, this is a test!')    
    """
    syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
    _add_root_log_handler(package, syslog_handler)

def init_console_logging(package):
    """Setup logging to be output to the console.

    Args:
        package (str): The package you are interested in tracing.

    Example:
        Call this method with your package's name as the parameter.
        >>> import uologging
        >>> uologging.init_console_logging('examplepkg')

        Then use the Python logging package in each of your package's modules.
        >>> import logging
        >>> logger = logging.getLogger(__name__)

        We use a hardcoded str here to enable doctest:
        >>> logger = logging.getLogger('examplepkg.just.testing')
        >>> logger.critical('Just kidding, this is a test!')
    """
    console_handler = logging.StreamHandler()
    _add_root_log_handler(package, console_handler)


def set_logging_verbosity(package, verbosity_flag: int):
    """Set the logging verbosity for your entire package.

    This leverages the 'root logger' paradigm provided by Python logging.

    Args:
        package (str): The name of the package you are interested in tracing.
        verbosity_flag (int): Higher number means more logging. Choices are [0,2]. 
            Default is 0. Default will captures WARNING, ERROR, and CRITICAL logs.
            Provide 1 to also capture INFO logs. Provide 2 to also capture DEBUG logs.
    """
    root_logger = _get_root_logger(package)
    if verbosity_flag == 1:
        root_logger.setLevel(logging.INFO)
    elif verbosity_flag >= 2:
        root_logger.setLevel(logging.DEBUG)
    else:  # Default to WARNING, following Python logging standards
        root_logger.setLevel(logging.WARNING)


def _add_root_log_handler(package, handler: logging.Handler):
    """Add a handler to a the root logger for package.

    Args:
        package (str|module): The package.
        handler (logging.Handler): A logging handler.
    """
    handler.setFormatter(_logging_format)
    root_logger = _get_root_logger(package)
    root_logger.addHandler(handler)


def _get_root_logger(package):
    """Get the 'root' logger for the provided package.

    Args:
        package (module|str): The package to get the root logger for.

    Raises:
        TypeError: If argument is not type module or str.

    Returns:
        logging.Logger: The root logger for 'package'.
    """
    try:
        package_name = package.__name__
    except AttributeError:
        if isinstance(package, str):
            package_name = package
        else:
            raise TypeError('Must provide str (or module).')
    return logging.getLogger(package_name)
