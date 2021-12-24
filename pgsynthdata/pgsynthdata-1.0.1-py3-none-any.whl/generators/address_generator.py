import os

from dotenv import load_dotenv
from faker import Faker

from ..datagenerator import ColumnPgInfo, Constraints, Statistics, generator

load_dotenv()
faker_local = os.getenv("FAKER_LOCAL", "de-CH")

STRING_TYPES = {"text", "character varying", "character"}
STRING_INTEGER_TYPES = {"integer", "text", "character varying", "character"}


@generator(STRING_INTEGER_TYPES, comment_identifier="ADDRESS_ZIP")
def address_zip_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    fake = Faker([faker_local])
    if constraints.is_unique:
        return [fake.unique.postcode() for _ in range(rows_to_gen)]
    return [fake.postcode() for _ in range(rows_to_gen)]


@generator(STRING_TYPES, comment_identifier="ADDRESS_STREET")
def address_street_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    fake = Faker([faker_local])
    if constraints.is_unique:
        return [fake.unique.street_name() for _ in range(rows_to_gen)]
    return [fake.street_name() for _ in range(rows_to_gen)]


@generator(STRING_INTEGER_TYPES, comment_identifier="ADDRESS_BUILDING_NR")
def address_building_nr_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    fake = Faker([faker_local])
    if constraints.is_unique:
        return [fake.unique.building_nr() for _ in range(rows_to_gen)]
    return [fake.building_nr() for _ in range(rows_to_gen)]


@generator(STRING_TYPES, comment_identifier="ADDRESS_CITY")
def address_city_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    fake = Faker([faker_local])
    if constraints.is_unique:
        return [fake.unique.city() for _ in range(rows_to_gen)]
    return [fake.city() for _ in range(rows_to_gen)]


@generator(STRING_TYPES, comment_identifier="ADDRESS_STREET_ADDRESS")
def address_street_address_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    fake = Faker([faker_local])
    if constraints.is_unique:
        return [fake.unique.street_address() for _ in range(rows_to_gen)]
    return [fake.street_address() for _ in range(rows_to_gen)]


@generator(STRING_TYPES, comment_identifier="ADDRESS_COUNTRY")
def address_country_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    fake = Faker([faker_local])
    if constraints.is_unique:
        return [fake.unique.country() for _ in range(rows_to_gen)]
    return [fake.country() for _ in range(rows_to_gen)]


@generator(STRING_TYPES, comment_identifier="ADDRESS_COUNTRY_CODE")
def address_country_code_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    fake = Faker([faker_local])
    if constraints.is_unique:
        return [fake.unique.country() for _ in range(rows_to_gen)]
    return [fake.country() for _ in range(rows_to_gen)]
