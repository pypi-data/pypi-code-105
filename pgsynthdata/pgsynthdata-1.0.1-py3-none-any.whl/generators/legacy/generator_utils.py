import random
import string
from bisect import bisect_left
from typing import Any, List, Optional, Sequence, Tuple, Union

import numpy
import radar


def fulfill_histogram_properties(histogram, rows_to_gen, data_type=float):
    if histogram is None:
        return False

    max_nr_of_rows_from_bounds = (
        data_type(histogram[len(histogram) - 1]) - data_type(histogram[0]) + 1
    )

    if max_nr_of_rows_from_bounds < rows_to_gen:
        return True

    return False


def take_closest(myList: List[any], myNumber: int):
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before


def random_word(average_length: int, value: str = None) -> str:
    average_length = round(average_length - 1)
    if value:
        if str(value).isdigit():
            word = gen_random_word(average_length, numeric=True)
        elif str(value).isupper():
            word = gen_random_word(average_length).upper()
        elif str(value) and str(value)[0].isupper():
            word = gen_random_word(average_length).capitalize()
        else:
            word = gen_random_word(average_length)
    else:
        word = gen_random_word(average_length)

    return word


def gen_random_word(length: int, numeric: bool = False) -> str:
    if length == 0:
        length += 1
    letters = string.ascii_lowercase
    numbers = string.digits

    if numeric:
        return "".join(random.choice(numbers) for i in range(length))
    else:
        return "".join(random.choice(letters) for i in range(length))


def gen_random_number(start: Any, end: Any, uniform: bool = False) -> Union[int, float]:

    start = int(start)
    end = int(end)

    if uniform:
        return random.uniform(start, end)
    else:
        return random.randint(start, end)


def random_number(
    numeric_precision: int = None,
    numeric_precision_radix: int = None,
    numeric_scale: int = None,
    min_value: Any = None,
    max_value: Any = None,
) -> Union[int, float]:

    if numeric_precision:
        if numeric_scale and numeric_scale != 0:
            number = round(
                gen_random_number(
                    min_value or 0,
                    max_value
                    or (
                        (
                            numeric_precision_radix
                            ** (numeric_precision - numeric_scale - 1)
                        )
                        / 1.5
                    ),
                    uniform=True,
                ),
                numeric_scale,
            )
        else:
            number = gen_random_number(
                min_value or 0,
                max_value
                or ((numeric_precision_radix ** (numeric_precision - 1)) / 1.5),
            )
    else:
        number = gen_random_number(0, 50000)

    return number


def random_date(start_date, end_date, time=False):
    if time:
        return radar.random_datetime(start=start_date, stop=end_date)
    else:
        return radar.random_date(start=start_date, stop=end_date)


def random_boolean(postgres: bool = True) -> Union[str, bool]:

    random_boolean = random.choice([True, False])
    if not postgres:
        return random_boolean
    else:
        if random_boolean:
            return "true"
        else:
            return "false"


def random_choices(
    list: List[Any], weights: Optional[Sequence[float]], k: int = 1
) -> Any:
    if k == 1:
        return random.choices(list, weights=weights, k=k)[0]
    else:
        return random.choices(list, weights=weights, k=k)


# HINT TE extracted from legacy model_generator.py
def determine_frequency(
    number_of_rows: int,
    total_rows: int,
    most_common_values: List[str] = None,
    most_common_freqs: List[float] = None,
    n_distinct: float = None,
) -> Tuple[float, int]:

    if most_common_values and most_common_freqs:

        if n_distinct > 0:
            distinct_no = n_distinct
        else:
            distinct_no = -n_distinct * number_of_rows
        distinct_no = round(distinct_no)
        leftover_freq = 1 - sum(most_common_freqs)
        generated_freqs = most_common_freqs

        # The dirichlet function that generates random floating numbers to fill
        # The left-over frequencies
        # Generated_freqs indicates the probability for a value to get picked
        generated_freqs += (
            numpy.random.dirichlet(numpy.ones(distinct_no - len(most_common_freqs)))
            * leftover_freq
        ).tolist()

        # Rows_to_gen has to be equal as distinct values
        rows_to_gen = len(generated_freqs)

    # No mcv means that no values seem to be more common than any others (all unique)
    else:
        # Rows_to_gen has to be equal as rows_to_gen since all unique
        generated_freqs = False
        rows_to_gen = total_rows

    return generated_freqs, rows_to_gen


# HINT TE extract for legacy 'query_generator.py' to avoid DRY in generators
def select_generator_mode(generated_vals, generated_freqs, null_frac, rows_to_gen):
    column_values = []
    for i in range(rows_to_gen):
        # Columns containing MCV
        # HINT TE null_frac ist nur bei vielen Daten genau
        if generated_vals and generated_freqs:
            random_frac = random.random()
            if null_frac and random_frac <= null_frac:
                column_values.append(None)
            else:
                # HINT Random choice gemäss freqs
                column_values.append(random_choices(generated_vals, generated_freqs))
        # All distinct columns # HINT TE Fall wo Daten *generiert* wurden
        elif generated_vals:
            column_values.append(generated_vals[i])
    return column_values
