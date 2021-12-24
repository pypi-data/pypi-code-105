import os
import argparse
import pytest

from polska.calculator import polska
from polska import __path__ as path


def main():
    parser = argparse.ArgumentParser(description='Преобразование выражения в польскую запись ')
    parser.add_argument('-v', '--variant', dest='variant', default='gui',
                        help='Вариант работы программы, '
                             'где gui - запуск программы, '
                             'pytest - Вывод результатов тестов pytest,'
                             'doctest - Вывод результатов теста doctest')
    args = parser.parse_args()
    if args.variant == 'pytest':
        pytest.main(['-v'])
    elif args.variant == 'doctest':
        print(os.system(f'python -m doctest -v {path[0]}\\calculator.py'))
    elif args.variant == 'gui':
        while (
                expr := input(
                    'Введите выражения для преобразования '
                    'в польскую запись или "end" для выхода:\n')) != 'end':
            try:
                print(polska(expr))
            except ValueError as e:
                print(f'Ошибка в введенных данных: {e}')


if __name__ == '__main__':
    main()
