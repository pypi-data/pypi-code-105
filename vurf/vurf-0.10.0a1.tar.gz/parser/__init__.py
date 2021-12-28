from io import TextIOWrapper
import sys
from typing import cast
from parser.stand_alone import Lark_StandAlone, ParseError
from parser.transformer import VurfTransformer, Root
from parser.indenter import PythonesqueIndenter
from vurf.nodes import Root


def parse(file: TextIOWrapper) -> Root:
    parser = Lark_StandAlone(
        postlex=PythonesqueIndenter(),
        transformer=VurfTransformer(),
        )
    try:
        # Add extra newline in case there is none
        return cast(Root, parser.parse(file.read() + '\n'))
    except ParseError as e:
        sys.stderr.write(" ".join(e.args) + "\n")
        sys.exit(1)
