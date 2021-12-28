# Copyright (c) 2022 Ansys, Inc. and its affiliates. Unauthorised use, distribution or duplication is prohibited
# LICENSE file is in the root directory of this source tree.
import os
import sys
from .ProjectGenerator import *
import argparse

__version__ = '0.0.8'


def cli():
    if '--version' in sys.argv[1:]:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--Name", help="Set the project name")
    parser.add_argument("-t", "--Template", help="Set the project template")
    args = parser.parse_args()

    generate_project_folder(os.getcwd(), args.Name, args.Template)

    exit(0)


if __name__ == '__main__':
    cli()



