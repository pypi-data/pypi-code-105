import math
from typing import Any, List

import numpy as np

from pgsynthdata.datagenerator import Statistics


def generate_array_lengths(stats: Statistics, rows_to_gen: int) -> List[int]:
    count_histogram = stats.pg_stats.elem_count_histogram[:-1]
    factor = rows_to_gen / len(count_histogram)
    result = []
    for l in set(count_histogram):
        # HINT: math.ceil guarantees that there are never less than rows_to_gen
        p = count_histogram.count(l)
        result += [int(l)] * int(math.ceil(p * factor))

    np.random.shuffle(result)
    return result[:rows_to_gen]


def elements_to_arrays(
    array_lengths: List[int], elements: List[Any]
) -> List[List[Any]]:
    result = []
    it = iter(elements)
    for l in array_lengths:
        result.append([next(it) for _ in range(l)])
    return result
