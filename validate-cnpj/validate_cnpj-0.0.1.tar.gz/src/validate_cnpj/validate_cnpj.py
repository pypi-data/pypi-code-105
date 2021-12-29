import re
from typing import List


def _clean(cnpj: str) -> str:
    return re.sub(r'\D', '', cnpj)


def _has_correct_length(cnpj: str) -> bool:
    CNPJ_VALID_SIZE = 14
    return len(cnpj) == CNPJ_VALID_SIZE


def _is_allowed(cnpj: str) -> bool:
    first_digit = cnpj[0]
    return not all(first_digit == digit for digit in cnpj)


def _get_factories(is_first_digit: bool) -> List[int]:
    if is_first_digit:
        return [6, 7, 8, 9, 2, 3, 4, 5, 6, 7, 8, 9]
    return [5, 6, 7, 8, 9, 2, 3, 4, 5, 6, 7, 8, 9]


def _caculate_digit(cnpj: str, is_first_digit: bool = True) -> bool:
    FACTORIES = _get_factories(is_first_digit)
    result_sum = 0
    for index, factory in enumerate(FACTORIES):
        result_sum += factory * int(cnpj[index])
    REST = result_sum % 11  # Número magico
    if REST >= 10:
        return 0
    return REST


def is_valid(cnpj: str) -> bool:
    cnpj: str = _clean(cnpj)
    if not _has_correct_length(cnpj):
        return False
    if not _is_allowed(cnpj):
        return False
    first_verification_digit: int = _caculate_digit(cnpj)
    last_verification_digit: int = _caculate_digit(cnpj, is_first_digit=False)
    return cnpj[-2:] == f'{first_verification_digit}{last_verification_digit}'
