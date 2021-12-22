from functools import wraps
import logging
import logging.config
import os
import sys
import time

from infi.caching import cached_function

DEFAULT_IBA_LOGDIR = '/var/log/iba'


def in_unit_test():
    import inspect
    current_stack = inspect.stack()
    if 'IGNORE_BEING_IN_UNITTEST' in os.environ:
        return False
    return any("unittest" in stack_frame.filename
               for stack_frame in current_stack)


def _get_logging_config(logfilename, parent_logger_name, handler_names):
    cfg = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'class': 'logging.Formatter',
                'format': '%(asctime)-25s %(levelname)-8s %(name)-50s %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S %z',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'formatter': 'default',
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            parent_logger_name: {
                'handlers': handler_names,
                'level': 'DEBUG',
                'propagate': False,
            },
            'tests': {
                'handlers': ['console', ],
                'level': 'DEBUG',
                'propagate': False,
            }
        }
    }

    if not in_unit_test():
        cfg['handlers']['file'] = {
                'level': 'DEBUG',
                'formatter': 'default',
                'class': 'logging.FileHandler',
                'filename': logfilename,
                'mode': 'a',
            }
        cfg['loggers'].update({'': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'paramiko': {
                'handlers': ['file'],
                'level': 'WARNING',
                'propagate': False,
            }})
        del cfg['loggers']['tests']
    return cfg


class debug_program:

    def __init__(self, logger_name, logfile_suffix=None, failure_result=1, logdir=DEFAULT_IBA_LOGDIR):
        self._failure_result = failure_result
        executable_name = os.path.basename(sys.argv[0])
        program_name = executable_name.replace('_', '-')

        os.makedirs(logdir, exist_ok=True)
        suffix = f'-{logfile_suffix}' if logfile_suffix else ''
        self._latestlog_link = os.path.join(logdir, f'{program_name}{suffix}.latest')
        self.log_path = os.path.join(
            logdir,
            f'{program_name}{suffix}-{time.strftime("%Y%m%d-%H%M%S")}.log')

        root_logger_name = logger_name.split('.')[0]
        self._dict_config = _get_logging_config(self.log_path, root_logger_name,
                                                self.get_handler_names())

    @staticmethod
    def get_handler_names():
        if in_unit_test():
            handlers = ['console']
        elif os.environ.get('IGUARD_VERBOSE'):
            handlers = ['file', 'console']
        else:
            handlers = ['file']

        return handlers

    def __call__(self, func):
        @wraps(func)
        def logging_wrapper(*args, **kwargs):
            from traceback import format_exception_only
            from infi.traceback import traceback_context
            from infi.exceptools import exceptools_context
            from infiniguard_core.utils.display import print_general_error_message
            self._redirect_logbook()
            self._setup_logging()
            self._silence_third_party_packages()

            logger = logging.getLogger(__name__)
            logger.info('Logging started')
            logger.info('Command line arguments: {!r}'.format(sys.argv))
            with exceptools_context():
                try:
                    return func(*args, **kwargs)
                except SystemExit:
                    pass
                except Exception:
                    formatted_exception = format_exception_only(*sys.exc_info()[0:2])[0].strip()
                    msg = '{0}, see log file {1}'.format(formatted_exception, self.log_path)
                    print_general_error_message(msg)
                    logger.exception(msg)
                finally:
                    logger.info("Logging ended")
                    self._update_latest_symlink()
            return self._failure_result
        return logging_wrapper

    def _redirect_logbook(self):
        """
        Send logbook messages to the standard python logging (needed for infinisdk).
        """
        from logbook.compat import LoggingHandler
        LoggingHandler().push_application()

    def _setup_logging(self):
        logging.config.dictConfig(self._dict_config)

    def _silence_third_party_packages(self):
        # Disable verbose urllib3 warnings suggesting certificate verification
        import requests
        import urllib3
        import warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings()  # @UndefinedVariable
        # Disable 'deprecated' warnings from paramiko < 2.5
        warnings.filterwarnings(action='ignore', module='.*paramiko.*')
        logging.getLogger('paramiko').setLevel(logging.WARNING)
        logging.getLogger('fabric').setLevel(logging.WARNING)
        logging.getLogger('invoke').setLevel(logging.WARNING)
        logging.getLogger('infi.storagemodel').setLevel(logging.WARNING)
        logging.getLogger('infi.multipathtools').setLevel(logging.WARNING)

    def _remove_old_symbolic_link_if_exists(self, dst):
        if os.path.exists(dst):
            os.remove(dst)

    def _update_latest_symlink(self):
        src = self.log_path
        dst = self._latestlog_link
        try:
            os.path.exists(dst) and os.remove(dst)
            self._remove_old_symbolic_link_if_exists(dst)
            os.symlink(src, dst)
        except (OSError, IOError):
            pass
