# Copyright 2021 UC Davis Plant AI and Biophysics Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

import numpy as np


# Represents an empty object, but allows passing `None`
# as an independent object in certain cases.
NoArgument = object()


def placeholder(obj):
    """Equivalent of lambda x: x, but enables pickling."""
    return obj


def to_camel_case(s):
    """Converts a given string `s` to camel case."""
    s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "") # noqa
    return ''.join(s)


def resolve_list_value(val):
    """Determines whether a list contains one or multiple values."""
    if len(val) == 1:
        return val[0]
    return val


def resolve_tuple_values(*inputs, custom_error = None):
    """Determines whether `inputs[0]` contains two values or
    they are distributed amongst the values in `inputs`. """
    if isinstance(inputs[0], (list, tuple)) and all(c is None for c in inputs[1:]):
        if len(inputs[0]) != len(inputs):
            # special case for COCO JSON
            if len(inputs) == 3 and len(inputs[0]) == 2 and isinstance(inputs[0][1], dict):
                return inputs[0][0], inputs[0][1]['bbox'], inputs[0][1]['category_id']
            if custom_error is not None:
                raise ValueError(custom_error)
            else:
                raise ValueError(
                    f"Expected either a tuple with {len(inputs)} values "
                    f"or {len(inputs)} values across two arguments.")
        else:
            return inputs[0]
    return inputs


def resolve_tuple(sequence):
    """Resolves a sequence to a tuple."""
    if isinstance(sequence, np.ndarray):
        sequence = sequence.tolist()
    return tuple(i for i in sequence)


def has_nested_dicts(obj):
    """Returns whether a dictionary contains nested dicts."""
    return any(isinstance(i, dict) for i in obj.values())


def as_scalar(inp):
    """Converts an input value to a scalar."""
    if isinstance(inp, (int, float)):
        return inp
    if np.isscalar(inp):
        return inp.item()
    if isinstance(inp, np.ndarray):
        return inp.item()
    from agml.backend.tftorch import torch
    if isinstance(inp, torch.Tensor):
        return inp.item()
    from agml.backend.tftorch import tf
    if isinstance(inp, tf.Tensor):
        return inp.numpy()
    raise TypeError(f"Unsupported variable type {type(inp)}.")


def scalar_unpack(inp):
    """Unpacks a 1-d array into a list of scalars."""
    return [as_scalar(item) for item in inp]


def is_array_like(inp):
    """Determines if an input is a np.ndarray, torch.Tensor, or tf.Tensor."""
    if isinstance(inp, np.ndarray):
        return True
    from agml.backend.tftorch import torch
    if isinstance(inp, torch.Tensor):
        return True
    from agml.backend.tftorch import tf
    if isinstance(inp, tf.Tensor):
        return True
    return False


class seed_context(object):
    """Creates a context with a custom random seed, then resets it.

    This allows for setting a custom seed (for reproducibility) in a
    context, then resetting the original state after exiting, to
    prevent interfering with the program execution.
    """

    def __init__(self, seed):
        self._seed = seed
        self._prev_state = None

    def __enter__(self):
        self._prev_state = np.random.get_state()
        np.random.seed(self._seed)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        np.random.set_state(self._prev_state)
        self._prev_state = None

    def reset(self):
        np.random.seed(self._seed)



