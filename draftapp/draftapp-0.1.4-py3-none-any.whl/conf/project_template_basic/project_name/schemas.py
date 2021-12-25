# -*- coding: utf-8 -*-
"""Schemas for app backend views"""
from marshmallow import ValidationError, fields, schema


class BytesField(fields.Field):
    """Bytes Field class"""

    def _validate(self, value):
        """Validates input"""
        # pylint: disable=unidiomatic-typecheck
        if type(value) is not bytes:
            raise ValidationError("Invalid input type.")

        if value is None or value == b"":
            raise ValidationError("Invalid value")


# pylint: disable=too-few-public-methods
class SchemaMixin:
    """Schema mixin class"""

    id = fields.Str()
