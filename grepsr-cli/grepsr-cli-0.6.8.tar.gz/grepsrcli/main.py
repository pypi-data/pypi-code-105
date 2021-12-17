from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import GrepsrCliError
from .controllers.base import Base
from .controllers.crawler import Crawler, CrawlerBase
from .controllers.report import Report, ReportBase
from .controllers.generate import Generate, GenerateBase

# configuration defaults
CONFIG = init_defaults('grepsrcli')


class GrepsrCli(App):
    """Grepsr Cli primary application."""

    class Meta:
        label = 'gcli'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            CrawlerBase,
            Crawler,
            ReportBase,
            Report,
            GenerateBase,
            Generate
        ]


class GrepsrCliTest(TestApp, GrepsrCli):
    """A sub-class of GrepsrCli that is better suited for testing."""

    class Meta:
        label = 'grepsrcli'


def main():
    with GrepsrCli() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except GrepsrCliError as e:
            print('GrepsrCliError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
