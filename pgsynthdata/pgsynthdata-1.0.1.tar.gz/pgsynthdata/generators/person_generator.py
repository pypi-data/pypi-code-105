import os

from dotenv import load_dotenv
from faker import Faker

from ..datagenerator import ColumnPgInfo, Constraints, Statistics, generator

load_dotenv()
faker_local = os.getenv("FAKER_LOCAL", "de-CH")

STRING_TYPES = {"text", "character varying", "character"}


@generator(STRING_TYPES, comment_identifier="PERSON_FIRST_NAME")
def person_firstname_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    fake = Faker([faker_local])
    if constraints.is_unique:
        return [fake.unique.first_name() for _ in range(rows_to_gen)]
    return [fake.first_name() for _ in range(rows_to_gen)]


@generator(STRING_TYPES, comment_identifier="PERSON_LAST_NAME")
def person_lastname_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    fake = Faker([faker_local])
    if constraints.is_unique:
        return [fake.unique.last_name() for _ in range(rows_to_gen)]
    return [fake.last_name() for _ in range(rows_to_gen)]


@generator(STRING_TYPES, comment_identifier="PERSON_NAME")
def person_name_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    fake = Faker([faker_local])
    if constraints.is_unique:
        return [fake.unique.name() for _ in range(rows_to_gen)]
    return [fake.name() for _ in range(rows_to_gen)]


@generator(STRING_TYPES, comment_identifier="PERSON_PREFIX")
def person_prefix_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    fake = Faker([faker_local])
    if constraints.is_unique:
        return [fake.unique.prefix() for _ in range(rows_to_gen)]
    return [fake.prefix() for _ in range(rows_to_gen)]


@generator(STRING_TYPES, comment_identifier="PERSON_SUFFIX")
def person_suffix_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    fake = Faker([faker_local])
    if constraints.is_unique:
        return [fake.unique.suffix() for _ in range(rows_to_gen)]
    return [fake.suffix() for _ in range(rows_to_gen)]
