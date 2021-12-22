"""
А.О. Блинов,КИ21-16/1Б, вариант 10
"""
import click
from knight_game_module import second_main


@click.command()
@click.argument('func', type=str)
@click.argument('first_c', nargs=2)
@click.argument('second_c', nargs=2)
def main(func, first_c, second_c):
    """
    Главная функция(?)
    """
    second_main(func, first_c, second_c)


if __name__ == '__main__':
    main()
