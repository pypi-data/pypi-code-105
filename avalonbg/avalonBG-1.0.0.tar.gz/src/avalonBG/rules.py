import json

import importlib.resources as pkg_resources

from avalonBG.exception import AvalonBGError

from . import resources


def get_rules():

    filename = "rules.json"

    try:
        with pkg_resources.path(resources, filename) as rules_path:
            with open(rules_path, "r") as infile:
                rules = json.load(infile)
    except FileNotFoundError:
        raise AvalonBGError("File '{}' doesn't exist!".format(filename))
    except json.decoder.JSONDecodeError:
        raise AvalonBGError("File '{}' can't be decoded!".format(filename))

    return rules
