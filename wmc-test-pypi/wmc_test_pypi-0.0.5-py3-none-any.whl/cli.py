import sys

from wmc_test_pypi import __version__


def hello():
    print("hello")


def hello_world():
    print("hello world")


def main(*argv):
    if not argv:
        argv = list(sys.argv)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--say_hello_world", default=False, help="say hello world")
    parser.add_argument("-v", "--version", action="version", version=("wmc_test_pypi %s" % __version__))
    args = parser.parse_args(argv[1:])

    if args.say_hello_world:
        hello_world()
    else:
        hello()


if __name__ == "__main__":
    main(*sys.argv)
