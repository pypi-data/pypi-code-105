"""
Name: Oliver Gaither
Date: Dec 27, 2021
Purpose: provide functions for easily generated
names to be used as dummy data for testing code and
potentially building systems
"""
import csv
import random
import os


def get_names():
    """
    returns a two dimensional list of rows from a csv
    file containing the most popular names from 1980
    :return: list of rows in csv of names
    """
    PATH = os.path.join(os.path.dirname(__file__), "names.csv")
    with open(PATH, "r") as file:
        reader = csv.reader(file)
        fields = next(reader)
        return list(reader)


def get_random_name(sex=None):
    """
    returns a random first name, can take
    optional parameters such as sex and seed
    :sex: sex of the name to be returned
    :seed: optional random seed
    :return: a name
    """
    if sex is None:
        return random.choice([x[1] for x in get_names()])
    elif (sex.lower() == "boy") or (sex.lower() == "girl"):
        return random.choice([x[1] for x in get_names() if x[3] == sex.lower()])
    else:
        print("Invalid sex: {}".format(sex))
        return -1


def get_names_by_letter(char, n, idx=0):
    """
    get a given amount of names
    based on the first letter
    :char: letter
    :n: amount of names
    """
    if n < 999:
        if n == 0:
            return []
        else:
            names = [x[1] for x in get_names() if x[1][0].lower() == char.lower()]
            if n > len(names):
                print("there are less names that start with {} than you queried for".format(char))
                return None
            else:
                return [names[idx]] + get_names_by_letter(char, n - 1, idx + 1)


def __get_last_names():
    path = os.path.join(os.path.dirname(__file__), "last-names.txt")
    with open(path, 'r', encoding='utf-8') as f:
        return list(map(lambda x: x.rstrip(), f.readlines()))


def get_full_name(sex=None):
    """
    returns a typical full name of a
    single given name and a family surname
    :sex: optional sex of the given name
    :return: full name
    """
    return "{} {}".format(get_random_name(sex), random.choice(__get_last_names()))


def get_full_names(n, sex=None):
    """
    returns a list of full names
    :n: number of names
    :sex: optional sex of the names
    :return: list of full names
    """
    if n < 999:
        if n == 0:
            return []
        else:
            return [get_full_name(sex)] + get_full_names(n - 1, sex)


def get_random_names(n, sex=None):
    """
    returns a list of given size of random names,
    can optionally set the sex of all the names to
    be in the list
    :n: number of names
    :sex: sex of the names
    :return: list of names
    """
    if n == 0:
        return []
    else:
        return [get_random_name(sex)] + get_random_names(n - 1, sex)


