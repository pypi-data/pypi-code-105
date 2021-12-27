from . import domain
import argparse
import sys


__version__ = '0.1.6'


def get_input_options_from_cli() -> domain.InputOptions:
    """
    example use:
        cdn-test --url=https://aws.amazon.com/pt/cloudfront/ --http-verb=GET --time-step=10s --output-file=
    """
    parser = argparse.ArgumentParser()

    if len(sys.argv) < 2:
        parser.print_help()
        parser.exit(status=1)

    parser.add_argument(
        '--url', '-u', type=str,
        help='URL to verified cache in cloudfront'
    )
    parser.add_argument(
        '--time-step', '-s', default='1m', nargs='?',
        help='time interval between requests'
    )
    parser.add_argument(
        '--http-verb', '-x', default='GET', nargs='?',
        help='HTTP verb utilized for requests to URL'
    )
    parser.add_argument(
        '--header-name', default='x-cache', nargs='?',
        help='response header name that contains "Miss from cloudfront" or "Hit from cloudfront"',
    )
    parser.add_argument(
        '--output-file', '-f', default='/tmp/cdn-test.json', nargs='?',
        help='file path to save records',
    )
    parser.add_argument(
        '--version', '-v', action='version', version=f'{__version__}\n',
        help='show cdn-test version'
    )

    args_namespace = parser.parse_args()
    args = vars(args_namespace)
    input_options = domain.InputOptions(**args)

    return input_options


def entrypoint():
    input_parameters = get_input_options_from_cli()
    domain.main(input_parameters)


if __name__ == '__main__':
    entrypoint()
