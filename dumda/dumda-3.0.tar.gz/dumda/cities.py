"""
Name: Oliver Gaither
Date: Dec 27, 2021
Purpose: provide functions for easily generated
cities to be used as dummy data for testing code and
potentially building systems
"""
import random
import os
import csv


def __get_cities():
    # TODO: redownload a new cities csv as only current state of city names
    # TODO: is not very diverse
    path = os.path.join(os.path.dirname(__file__), "world_cities.csv")
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        return list(reader)


def get_cities():
    """
    get complete list of available
    city names
    """
    return [x[0] for x in __get_cities()]


def __get_countries_obj():
    c = __get_cities()

    def create_obj(obj, keys):
        if len(keys) == 0:
            return obj
        else:
            obj[keys[0]] = []
            return create_obj(obj, keys[1:])

    countries = []
    for var in c:
        if var[1] not in countries:
            countries.append(var[1])

    o = create_obj({}, countries)
    for var in c:
        o[var[1]].append(var[0])

    return o


def get_random_city(country=None):
    """
    return a random city, optionally
    pass a specific country
    :country: chosen country
    :return: a random city
    """
    if country is not None:
        return random.choice(__get_countries_obj()[country])
    else:
        return random.choice(get_cities())


def get_random_cities(n, country=None):
    """
    returns a list of random cities
    optionally pass a country
    :n: number of cities
    :country: chosen country
    :return: list of cities
    """
    if n == 0:
        return []
    else:
        return [get_random_city(country)] + get_random_cities(n - 1, country)

