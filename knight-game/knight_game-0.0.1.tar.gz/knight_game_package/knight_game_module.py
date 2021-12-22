"""
click - для работы с модулем через cmd
itertools - для перебора вариантов хода
Tuple - для ограничения входных данных некоторых функций
"""
import itertools
from typing import Tuple


def defence_knight_move(f_1, f_2, s_1, s_2):
    """
    Программа для проверки входных данных функции knight_move
    f_1, f_2 - координаты начальной клетки
    s_1, s_2 - координаты конечной клетки
    """
    limit = range(1, 9)
    if f_1 not in limit or f_2 not in limit or s_1 not in limit or s_2 not in limit:
        raise ValueError('Координаты введены не верно')


def knight_move(start: Tuple[int, int], finish: Tuple[int, int]) -> int:
    """
    Программа возвращается кол-во ходов, необходимое коню
    для того, чтобы дойти из (f_1,f_2) в (s_1,s_2)
    f_1, f_2 - координаты начальной клетки
    s_1, s_2 - координаты конечной клетки
    """
    n = -1
    all_sc = list(range(1, 9))
    attempt = 1
    f_1, f_2 = start
    t_1, t_2 = f_1, f_2
    s_1, s_2 = finish
    defence_knight_move(f_1, f_2, s_1, s_2)
    while attempt:
        n += 1
        variants_temp = itertools.product(all_sc, repeat=n)
        for i in variants_temp:
            second_temp = []
            for j in i:
                second_temp.append((t_1, t_2))
                if j == 1 and (t_1 + 1) in all_sc and (t_2 + 2) in all_sc:
                    t_1 += 1
                    t_2 += 2
                if j == 2 and (t_1 - 1) in all_sc and (t_2 + 2) in all_sc:
                    t_1 -= 1
                    t_2 += 2
                if j == 3 and (t_1 + 2) in all_sc and (t_2 + 1) in all_sc:
                    t_1 += 2
                    t_2 += 1
                if j == 4 and (t_1 + 2) in all_sc and (t_2 - 1) in all_sc:
                    t_1 += 2
                    t_2 -= 1
                if j == 5 and (t_1 - 2) in all_sc and (t_2 - 1) in all_sc:
                    t_1 -= 2
                    t_2 -= 1
                if j == 6 and (t_1 - 2) in all_sc and (t_2 + 1) in all_sc:
                    t_1 -= 2
                    t_2 += 1
                if j == 7 and (t_1 - 1) in all_sc and (t_2 - 2) in all_sc:
                    t_1 -= 1
                    t_2 -= 2
                if j == 8 and (t_1 + 1) in all_sc and (t_2 - 2) in all_sc:
                    t_1 += 1
                    t_2 -= 2
            if (t_1, t_2) == (s_1, s_2):
                second_temp.append((s_1, s_2))
                second_temp.pop(0)
                return n
            else:
                t_1, t_2 = f_1, f_2


def knights_collision(first: Tuple[int, int], second: Tuple[int, int]) -> int:
    """
    Функция возвращает минимальное кол-во ходов, через которое
    конь из (f_1,f_2) будет стоят в зоне атаки коня из (s_1,s_2)
    f_1, f_2 - координаты одного коня
    s_1, s_2 - координаты другого коня
    """
    moves = knight_move(first, second)
    if moves % 2 == 0:
        answer = moves // 2
    else:
        answer = (moves - 1) // 2
    return answer


# @click.command()
# @click.argument('func', type=str)
# @click.argument('first_c', nargs=2)
# @click.argument('second_c', nargs=2)
def second_main(func, first_c, second_c):
    """
    Основная функция, проводящая перноначальную обработку входных данных
    func - число от 1 до 2, обозначающее в какую функцию пользователь хочет отправить данные
    1 - knight_move
    2 - knight_collision
    first_c - координаты начальной(первой) клетки
    second_c - координаты конечной(второй) клетки
    """
    first_c, second_c = list(first_c), list(second_c)
    first_c_1 = first_c[0].upper()
    second_c_1 = second_c[0].upper()
    first_c_2 = first_c[1]
    second_c_2 = second_c[1]
    if second_c_2.isdigit():
        second_c_2 = int(second_c_2)
    if first_c_2.isdigit():
        first_c_2 = int(first_c_2)
    letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}
    first_c_1 = letters[first_c_1]
    second_c_1 = letters[second_c_1]
    first_c_2, second_c_2 = int(first_c_2), int(second_c_2)
    moves = knight_move((first_c_1, first_c_2), (second_c_1, second_c_2))
    if func == 'k_m':
        print(moves)
        return moves
    if func == 'k_c':
        result = knights_collision((first_c_1, first_c_2), (second_c_1, second_c_2))
        print(result)
        return result

