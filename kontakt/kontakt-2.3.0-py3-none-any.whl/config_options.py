"""Support for defining configurable options and building default configs from them.

There are two related ideas here. The first is of a *configurable options*, a description of
a single option in a *configuration*. A configuration, then, is just a tree - modeled as
dicts-of-dicts - where the leaf values are the options. So an option describes a path through
the tree to a leaf, a description of the option, and a default value for the leaf.
"""

import copy
from typing import Mapping
from dendrodict import DeepDict


class Option:
    """Description of a single configurable option.

    Args:
        path: Path to the option in the config.
        description: Description of the option.
        default: Default value of the option.
    """

    def __init__(self, path, description, default):
        if len(path) < 1:
            raise ValueError("Path must have at least one element")

        self._description = description
        self._default = default
        self._path = tuple(path)

    @property
    def name(self):
        "The name of the option."
        return self.path[-1]

    @property
    def description(self):
        "The description of the option."
        return self._description

    @property
    def default(self):
        "The default value of the option."
        return self._default

    @property
    def path(self):
        "Path to the option in the config."
        return self._path

    def __repr__(self):
        return f"Option(path={self.path}, description='{self.description}', default={self.default})"

    def __str__(self):
        return f"{self.path}: {self.description} [default={self.default}]"


def build_default_config(options) -> dict:
    """Build a default config from an iterable of options."""
    return DeepDict({option.path: option.default for option in options}).to_dict()


def merge_configs(dest, src):
    """Merge two config dicts.

    Merging can't happen if the dictionaries are incompatible. This happens when the same path in `src` exists in `dest`
    and one points to a `dict` while another points to a non-`dict`.

    Returns: A new `dict` with the contents of `src` merged into `dest`.

    Raises:
        ValueError: If the two dicts are incompatible.
    """
    dest = copy.deepcopy(dest)

    for src_name, src_val in src.items():
        if isinstance(src_val, Mapping):
            dest_val = dest.get(src_name, {})
            if not isinstance(dest_val, Mapping):
                raise ValueError("Incompatible config structures")

            dest[src_name] = merge_configs(dest_val, src_val)
        else:
            try:
                if isinstance(dest[src_name], Mapping):
                    raise ValueError("Incompatible config structures")
            except KeyError:
                pass
            dest[src_name] = src_val

    return dest
